#!-*- coding:utf8 -*-
import random

from src.accountResourceTools import getAdminFloatNetId
from src.accountResourceTools import getDefaultSecGroupId
from src.accountResourceTools import getFlavorId
from src.accountResourceTools import getTestImageId
from src.accountResourceTools import getVolumeTypeId
from src.clients.cinderClient import CinderClient
from src.clients.novaClient import NovaClient
from src.clients.openstackClient import OpenstackClient
from src.common.fileTool import FileTool
from src.common.strTool import StrTool
from src.init import Init
from src.loggers import Loggers
from src.pojo.Compute import Compute
from src.pojo.FloatIp import FloatIp
from src.pojo.NET import Net
from src.pojo.Router import Router
from src.pojo.Volume import Volume
from src.readConfig import ReadConfig


class InitFioResource:
    def __init__(self):
        self._readConfig=ReadConfig()
        self._loggers=Loggers()

        self._os_tenant_name = self._readConfig.accounts.stability_fio_os_tenant_name
        self._os_project_name = self._readConfig.accounts.stability_fio_os_project_name
        self._os_username = self._readConfig.accounts.stability_fio_os_username
        self._os_password = self._readConfig.accounts.stability_fio_os_password

        self._init = Init(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password,self._loggers.stabilityFioLogger)
        self._accountResource = self._init.initAccountResource()

        self._router_name = 'basebench_stablity_fio_router'
        self._user_data_path = 'userdata/user_data'
        self._fio_net_name = 'basebench_fio_stable_net'
        self._fio_subnet_cidr = '192.168.50.0/24'

        self._loggers.stabilityFioLogger.info('===初始化fio稳定性测试资源===')
        self._initResource()

    def _initResource(self):
        """
        初始化fio资源
        公共资源初始化
        :return:
        """
        self._loggers.stabilityFioLogger.info('初始化命令行客户端')
        self._openstackClient = OpenstackClient(self._os_tenant_name, self._os_project_name, self._os_username,self._os_password)
        self._novaClient = NovaClient(self._os_project_name, self._os_username,self._os_password)
        self._cinderClient = CinderClient(self._os_tenant_name, self._os_project_name, self._os_username,self._os_password)

        self._loggers.stabilityFioLogger.info('初始化默认安全组、外部网络、测试镜像')
        self._default_secgroup_id = getDefaultSecGroupId(self._accountResource.get_secgroups(), self._readConfig.base.default_secgroup_name)
        self._admin_float_net_id = getAdminFloatNetId(self._accountResource.get_adminNets(), self._readConfig.base.admin_float_net_name)
        self._test_image_id = getTestImageId(self._accountResource.get_images(), self._readConfig.base.test_image_name)

        self._zone_names=self._readConfig.base.zone_names.split('||')

        if self._readConfig.executeTest.is_stability_test_fio.lower()=='true':
            self._loggers.stabilityFioLogger.info('===开始初始化fio稳定性测试资源===')
            self._initFio()

        self._loggers.stabilityFioLogger.info('将测试初始化资源写入到文件dbs/stabilityFioTestAccountResource.dbs')
        FileTool.writeObjectIntoFile(self._accountResource, 'dbs/stabilityFioTestAccountResource.dbs')

    def _initFio(self):
        """
        根据fio测试需要，设置要测试的网络/云主机名/云硬盘名
        :return:
        """
        self._loggers.stabilityFioLogger.info('初始化fio测试的云主机规格')
        self._test_fio_flavor_id = getFlavorId(self._accountResource.get_flavors(), self._readConfig.executeTest.stability_test_fio_flavor)

        self._loggers.stabilityFioLogger.info('初始化fio网络资源，创建名为' + self._fio_net_name + '的网络')
        fio_test_net =Net()
        fio_test_net.name = StrTool.addUUID(self._fio_net_name)
        fio_test_net.cidr = self._fio_subnet_cidr
        try:
            fio_test_net.id = self._openstackClient.createNetwork(fio_test_net.name,fio_test_net.cidr)
        except Exception as e:
            self._loggers.stabilityFioLogger.error('创建网络'+fio_test_net.name+'失败!'+'\r\n'+e.args.__str__())
        self._fio_net_id = fio_test_net.id

        self._loggers.stabilityFioLogger.info('初始化一个路由器资源，创建名为' + self._router_name + '的路由')
        test_router = Router()
        test_router.name = StrTool.addUUID(self._router_name)
        try:
            test_router.id = self._openstackClient.createRouter(test_router.name, self._admin_float_net_id)
        except Exception as e:
            self._loggers.stabilityFioLogger.error('创建路由器' + test_router.name + '失败!' + '\r\n' +e.args.__str__())
        self._router_id = test_router.id
        self._loggers.stabilityFioLogger.info('将fio网络' + self._fio_net_name + '绑定到路由器' + self._router_name)
        try:
            fio_subnet_id = self._openstackClient.getSubNetId(self._fio_net_id)
            self._openstackClient.addRouterInterface(self._router_id,fio_subnet_id)
            test_router.add_subnet_id(fio_subnet_id)
            fio_test_net.add_subnet_id(fio_subnet_id)
        except Exception as e:
            self._loggers.stabilityFioLogger.error('将fio网络' + self._fio_net_name+ '绑定到路由器' + self._router_name+'失败!'+'\r\n'+e.args.__str__())
        self._accountResource.add_net(fio_test_net)
        self._accountResource.add_router(test_router)

        self._loggers.stabilityFioLogger.info('初始化fio测试的云主机')
        volume_types_and_num=self._readConfig.executeTest.stability_test_fio_volume_types_and_num.split('||')
        test_fio_types=self._readConfig.executeTest.stability_test_fio_types.split('||')
        for volume_type_and_num_str in volume_types_and_num:
            volume_type_and_num=volume_type_and_num_str.split('&')
            volumeType_id = getVolumeTypeId(self._accountResource.get_volumeTypes(),volume_type_and_num[0])
            num=int(volume_type_and_num[1])
            while num >0:
                num = num - 1
                for test_fio_type in test_fio_types:
                    volumeName = StrTool.addUUID('basebench_fio_' + test_fio_type + volume_type_and_num[0])
                    computeName = StrTool.addUUID('basebench_fio_' + test_fio_type + volume_type_and_num[0] + '_'+str(num))

                    #创建云硬盘
                    test_volume = Volume()
                    try:
                        test_volume.name = volumeName
                        test_volume.type = volume_type_and_num[0]
                        test_volume.size = self._readConfig.executeTest.stability_test_fio_volume_size
                        test_volume.id = self._cinderClient.createVolume(test_volume.name,volumeType_id,test_volume.size)
                    except Exception as e:
                        self._loggers.stabilityFioLogger.error('创建云硬盘'+ volumeName +'失败'+'\r\n'+e.args.__str__())
                    self._accountResource.add_volume(test_volume)

                    #申请浮动IP
                    test_floatip = FloatIp()
                    try:
                        test_floatip.ip = self._openstackClient.getFloatIp(self._admin_float_net_id)
                        test_floatip.id = self._openstackClient.getFloatId(test_floatip.ip)
                    except Exception as e:
                        self._loggers.stabilityFioLogger.error('申请浮动ip失败!'+'\r\n'+e.args.__str__())
                    self._accountResource.add_floatIp(test_floatip)

                    #启动云主机
                    test_compute = Compute()
                    test_compute.name = computeName
                    test_compute.testType=test_fio_type
                    try:
                        test_compute.id = self._novaClient.bootCompute(test_compute.name,
                                                                       self._test_fio_flavor_id,
                                                                       self._test_image_id,
                                                                       self._fio_net_id,
                                                                       self._default_secgroup_id,
                                                                       random.choice(self._zone_names),
                                                                       self._user_data_path)
                    except Exception as e:
                        self._loggers.stabilityFioLogger.error('启动云主机'+test_compute.name+'失败!'+'\r\n'+e.args.__str__())

                    # 绑定浮动IP
                    try:
                        is_add_succ = self._novaClient.addFloatForCompute(test_compute.id,test_floatip.ip)
                        if is_add_succ:
                            test_compute.float_ip = test_floatip.ip
                    except Exception as e:
                        self._loggers.stabilityFioLogger.error('为云主机'+test_compute.name+'绑定浮动ip:'+test_floatip.ip+'失败!'+'\r\n'+e.args.__str__())

                    # 挂载云硬盘
                    try:
                        is_attach_succ = self._novaClient.attachVolume(test_compute.id,test_volume.id,'/dev/vdb')
                        if is_attach_succ:
                            test_compute.volumeId = test_volume.id
                            test_compute.volumeName = test_volume.name
                    except Exception as e:
                        self._loggers.stabilityFioLogger.error('挂载云硬盘失败！'+'\r\n'+e.args.__str__())

                    self._accountResource.add_fioCompute(test_compute)
                    self._accountResource.add_compute(test_compute)

    def getStabilityFioAccountResource(self):
        return self._accountResource



#!-*- coding:utf8 -*-

from src.clients.neutronClient import NeutronClient
from src.clients.cinderClient import CinderClient
from src.clients.novaClient import NovaClient
from config.config import DEFAULT_SECGROUP_NAME
from config.config import TEST_IMAGE_NAME
from config.config import ADMIN_FLOAT_NET_NAME
from config.config import ZONE_NAMES
from config.config import STABILITY_TEST_FIO_WHAT
from config.config import STABILITY_TEST_FIO_VOLUME_TYPE
from config.config import STABILITY_TEST_FIO_FLAVOR
from config.config import STABILITY_TEST_FIO_VOLUME_SIZE
from config.config import FLOAT_IP_QOS
from config.config import STABILITY_FIO_ACCOUNT_OS_TENANT_NAME
from config.config import STABILITY_FIO_ACCOUNT_OS_PROJECT_NAME
from config.config import STABILITY_FIO_ACCOUNT_OS_USERNAME
from config.config import STABILITY_FIO_ACCOUNT_OS_PASSWORD
from config.config import IS_STABILITY_TEST_FIO
from src.logger import stabilityFioLogger
from src.common import addUUID
from src.common import writeObjectIntoFile
from src.pojo.Compute import Compute
from src.pojo.NET import Net
from src.pojo.Router import Router
from src.pojo.Volume import Volume
from src.pojo.FloatIp import FloatIp
from src.init import Init
from src.accountResourceTools import getDefaultSecGroupId
from src.accountResourceTools import getAdminFloatNetId
from src.accountResourceTools import getTestImageId
from src.accountResourceTools import getFlavorId
from src.accountResourceTools import getVolumeTypeId
import random

class InitFioResource():
    def __init__(self):
        self._os_tenant_name = STABILITY_FIO_ACCOUNT_OS_TENANT_NAME
        self._os_project_name = STABILITY_FIO_ACCOUNT_OS_PROJECT_NAME
        self._os_username = STABILITY_FIO_ACCOUNT_OS_USERNAME
        self._os_password = STABILITY_FIO_ACCOUNT_OS_PASSWORD

        self._init = Init(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password,stabilityFioLogger)
        self._accountResource = self._init.initAccountResource()

        self._router_name = 'stablity_fio_router'
        self._user_data_path = 'userdata/user_data'
        self._fio_net_name = 'fio_stable_net'
        self._fio_subnet_cidr = '192.168.50.0/24'

        stabilityFioLogger.info('===初始化fio稳定性测试资源===')
        self._initResource()

    def _initResource(self):
        """
        初始化fio资源
        公共资源初始化
        :return:
        """
        stabilityFioLogger.info('初始化命令行客户端')
        self._neutronClient = NeutronClient(self._os_tenant_name, self._os_project_name, self._os_username,self._os_password)
        self._novaClient = NovaClient(self._os_tenant_name, self._os_project_name, self._os_username,self._os_password)
        self._cinderClient = CinderClient(self._os_tenant_name, self._os_project_name, self._os_username,self._os_password)

        stabilityFioLogger.info('初始化默认安全组、外部网络、测试镜像')
        self._default_secgroup_id = getDefaultSecGroupId(self._accountResource.get_secgroups(), DEFAULT_SECGROUP_NAME)
        self._admin_float_net_id = getAdminFloatNetId(self._accountResource.get_adminNets(), ADMIN_FLOAT_NET_NAME)
        self._test_image_id = getTestImageId(self._accountResource.get_images(), TEST_IMAGE_NAME)

        stabilityFioLogger.info('初始化一个路由器资源，创建名为' + self._router_name + '的路由')
        test_router = Router()
        test_router.name = addUUID(self._router_name)
        try:
           test_router.id = self._neutronClient.createRouter(test_router.name, self._admin_float_net_id)
        except Exception,e:
           stabilityFioLogger.error('创建路由器'+test_router.name+'失败!'+'\r\n'+e.message)
        self._router_id = test_router.id
        self._accountResource.add_router(test_router)

        if IS_STABILITY_TEST_FIO:
           stabilityFioLogger.info('===开始初始化fio稳定性测试资源===')
           self._initFio()

        stabilityFioLogger.info('将测试初始化资源写入到文件dbs/stabilityFioTestAccountResource.dbs')
        writeObjectIntoFile(self._accountResource, 'dbs/stabilityFioTestAccountResource.dbs')

    def _initFio(self):
        """
        根据fio测试需要，设置要测试的网络/云主机名/云硬盘名
        :return:
        """
        stabilityFioLogger.info('初始化fio测试的云主机规格')
        self._test_fio_flavor_id = getFlavorId(self._accountResource.get_flavors(), STABILITY_TEST_FIO_FLAVOR)

        stabilityFioLogger.info('初始化fio网络资源，创建名为' + self._fio_net_name + '的网络')
        fio_test_net =Net()
        fio_test_net.name = addUUID(self._fio_net_name)
        fio_test_net.cidr = self._fio_subnet_cidr
        try:
            fio_test_net.id = self._neutronClient.createNetwork(fio_test_net.name,fio_test_net.cidr)
        except Exception,e:
            stabilityFioLogger.error('创建网络'+fio_test_net.name+'失败!'+'\r\n'+e.message)
        self._fio_net_id = fio_test_net.id
        self._accountResource.add_net(fio_test_net)

        stabilityFioLogger.info('将fio网络' + self._fio_net_name + '绑定到路由器' + self._router_name)
        try:
            self._fio_subnet_id = self._neutronClient.getSubNetId(self._fio_net_id)
            self._neutronClient.addRouterInterface(self._router_id,self._fio_subnet_id)
        except Exception,e:
            stabilityFioLogger.error('将fio网络' + self._oss_net_name+ '绑定到路由器' + self._router_name+'失败!'++'\r\n'+e.message)

        stabilityFioLogger.info('初始化fio测试的云主机')
        for volumetype,num in STABILITY_TEST_FIO_VOLUME_TYPE.items():
            volumeType_id = getVolumeTypeId(self._accountResource.get_volumeTypes(),volumetype)
            num=int(num)
            while num >0:
                num = num - 1
                for test_fio_type in STABILITY_TEST_FIO_WHAT:
                    volumeName = addUUID('fio_' + test_fio_type + volumetype)
                    computeName = addUUID('fio_' + test_fio_type + volumetype + '_'+str(num))

                    #创建云硬盘
                    test_volume = Volume()
                    try:
                        test_volume.name = volumeName
                        test_volume.type = volumetype
                        test_volume.size = STABILITY_TEST_FIO_VOLUME_SIZE
                        test_volume.id = self._cinderClient.createVolume(test_volume.name,volumeType_id,test_volume.size)
                    except Exception,e:
                        stabilityFioLogger.error('创建云硬盘'+ volumeName +'失败'+'\r\n'+e.message)
                    self._accountResource.add_volume(test_volume)

                    #申请浮动IP
                    test_floatip = FloatIp()
                    try:
                        test_floatip.ip = self._neutronClient.getFloatIp(self._admin_float_net_id,FLOAT_IP_QOS)
                        test_floatip.id = self._neutronClient.getFloatId(test_floatip.ip)
                    except Exception,e:
                        stabilityFioLogger.error('申请浮动ip失败!'+'\r\n'+e.message)
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
                                                                       random.choice(ZONE_NAMES),
                                                                       self._user_data_path)
                    except Exception,e:
                        stabilityFioLogger.error('启动云主机'+test_compute.name+'失败!'+'\r\n'+e.message)

                    # 绑定浮动IP
                    try:
                        is_add_succ = self._novaClient.addFloatForCompute(test_compute.id,test_floatip.ip)
                        if is_add_succ:
                            test_compute.float_ip = test_floatip.ip
                    except Exception,e:
                        stabilityFioLogger.error('为云主机'+test_compute.name+'绑定浮动ip:'+test_floatip.ip+'失败!'+'\r\n'+e.message)

                    # 挂载云硬盘
                    try:
                        is_attach_succ = self._novaClient.attachVolume(test_compute.id,test_volume.id,'/dev/vdb')
                        if is_attach_succ:
                            test_compute.volumeId = test_volume.id
                            test_compute.volumeName = test_volume.name
                    except Exception,e:
                        stabilityFioLogger.error('挂载云硬盘失败！'+'\r\n'+e.message)

                    self._accountResource.add_fioCompute(test_compute)
                    self._accountResource.add_compute(test_compute)

    def getStabilityPerformanceAccountResource(self):
        return self._accountResource



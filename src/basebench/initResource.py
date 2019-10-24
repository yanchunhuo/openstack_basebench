#!-*- coding:utf8 -*-
from src.clients.openstackClient import OpenstackClient
from src.clients.cinderClient import CinderClient
from src.clients.novaClient import NovaClient
from src.loggers import Loggers
from src.readConfig import ReadConfig
from src.common.fileTool import FileTool
from src.common.strTool import StrTool
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

class InitResource:
    def __init__(self):
        self._readConfig=ReadConfig()
        self._loggers=Loggers()

        self._os_tenant_name=self._readConfig.accounts.basebench_os_tenant_name
        self._os_project_name=self._readConfig.accounts.basebench_os_project_name
        self._os_username =self._readConfig.accounts.basebench_os_username
        self._os_password=self._readConfig.accounts.basebench_os_password

        self._init=Init(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password,self._loggers.basebenchLogger)
        self._accountResource = self._init.initAccountResource()

        self._test_fio_router_name='basebench_fio_router'
        self._test_iperf_router_name = 'basebench_iperf_router'
        self._test_unixbench_router_name = 'basebench_unixbench_router'
        self._user_data_path='userdata/user_data'

        self._test_fio_net_name='basebench_fio_net'
        self._test_fio_subnet_cidr='192.168.50.0/24'

        self._test_iperf_net1_name='basebench_iperf_net1'
        self._test_iperf_subnet1_cidr='192.168.70.0/24'
        self._test_iperf_net2_name='basebench_iperf_net2'
        self._test_iperf_subnet2_cidr = '192.168.80.0/24'

        self._test_unixbench_net_name = 'basebench_unixbench_net'
        self._test_unixbench_subnet_cidr = '192.168.60.0/24'

        self._loggers.basebenchLogger.info('===初始化基准测试基础资源===')
        self._initResource()

    def _initResource(self):
        """
        公共资源初始化
        :return:
        """
        self._loggers.basebenchLogger.info('初始化命令行客户端')
        self._openstackClient=OpenstackClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._novaClient=NovaClient(self._os_project_name,self._os_username,self._os_password)
        self._cinderClient=CinderClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)

        self._loggers.basebenchLogger.info('初始化默认安全组、测试镜像、测试镜像')
        self._default_secgroup_id=getDefaultSecGroupId(self._accountResource.get_secgroups(),self._readConfig.base.default_secgroup_name)
        self._admin_float_net_id=getAdminFloatNetId(self._accountResource.get_adminNets(),self._readConfig.base.admin_float_net_name)
        self._test_image_id=getTestImageId(self._accountResource.get_images(),self._readConfig.base.test_image_name)

        self._loggers.basebenchLogger.info('初始化可用域'+self._readConfig.base.zone_names)
        self._zone_names=self._readConfig.base.zone_names.split('||')

        #判断需要测试的类型
        if self._readConfig.executeTest.is_basebench_test_fio.lower()=='true':
            self._loggers.basebenchLogger.info('===开始初始化fio资源===')
            self._initFio()
        if self._readConfig.executeTest.is_basebench_test_unixbench.lower()=='true':
            self._loggers.basebenchLogger.info('===开始初始化unixbench资源===')
            self._initUnixbench()
        if self._readConfig.executeTest.is_basebench_test_iperf.lower()=='true':
            self._loggers.basebenchLogger.info('===开始初始化iperf资源===')
            self._initIperf()

            self._loggers.basebenchLogger.info('将测试初始化资源写入到文件dbs/basebenchTestAccountResource.dbs')
        FileTool.writeObjectIntoFile(self._accountResource,'dbs/basebenchTestAccountResource.dbs')

    def _initFio(self):
        """
        根据fio所需要测试，设置要测试的网络/云主机名/云硬盘名
        :return:
        """
        self._loggers.basebenchLogger.info('初始化fio测试的云主机规格')
        self._test_fio_flavor_id = getFlavorId(self._accountResource.get_flavors(), self._readConfig.executeTest.basebench_test_fio_flavor)

        self._loggers.basebenchLogger.info('初始化fio网络资源，创建名为' + self._test_fio_net_name + '的网络')
        test_fio_net = Net()
        test_fio_net.name = StrTool.addUUID(self._test_fio_net_name)
        test_fio_net.cidr = self._test_fio_subnet_cidr
        try:
            test_fio_net.id = self._openstackClient.createNetwork(test_fio_net.name, test_fio_net.cidr)
        except Exception as e:
            self._loggers.basebenchLogger.error('创建网络'+test_fio_net.name+'失败!'+'\r\n'+e.args.__str__())
        self._test_fio_net_id = test_fio_net.id

        self._loggers.basebenchLogger.info('初始化fio路由器资源，创建名为' + self._test_fio_router_name + '的路由器')
        test_fio_router=Router()
        test_fio_router.name=StrTool.addUUID(self._test_fio_router_name)
        try:
            test_fio_router.id=self._openstackClient.createRouter(test_fio_router.name,self._admin_float_net_id)
        except Exception as e:
            self._loggers.basebenchLogger.error('初始化fio路由器'+test_fio_router.name+'失败!'+'\r\n'+e.args.__str__())
        self._loggers.basebenchLogger.info('将fio网络' + test_fio_net.name + '绑定到路由器' + test_fio_router.name)
        try:
            test_fio_net_subnet_id = self._openstackClient.getSubNetId(self._test_fio_net_id)
            self._openstackClient.addRouterInterface(test_fio_router.id, test_fio_net_subnet_id)
            test_fio_net.add_subnet_id(test_fio_net_subnet_id)
            test_fio_router.add_subnet_id(test_fio_net_subnet_id)
        except Exception as e:
            self._loggers.basebenchLogger.error('将fio网络' + test_fio_net.name + '绑定到路由器' + test_fio_router.name +'失败'+'\r\n'+e.args.__str__())
        self._accountResource.add_net(test_fio_net)
        self._accountResource.add_router(test_fio_router)

        self._loggers.basebenchLogger.info('初始化fio测试的云主机')
        test_fio_volume_types=self._readConfig.executeTest.basebench_test_fio_volume_types.split('||')
        test_fio_types = self._readConfig.executeTest.basebench_test_fio_types.split('||')
        for test_fio_volume_type in test_fio_volume_types:
            volumeType_id = getVolumeTypeId(self._accountResource.get_volumeTypes(), test_fio_volume_type)
            for test_fio_type in test_fio_types:
                volumeName = StrTool.addUUID('basebench_fio_' + test_fio_type + test_fio_volume_type)
                computeName = StrTool.addUUID('basebench_fio_' + test_fio_type + test_fio_volume_type)
                testType = test_fio_type + test_fio_volume_type
                # 创建云硬盘
                test_volume = Volume()
                test_volume.name = volumeName
                test_volume.size = self._readConfig.executeTest.basebench_test_fio_volume_size
                test_volume.type = test_fio_volume_type
                self._loggers.basebenchLogger.info('创建云硬盘'+test_volume.name)
                try:
                    test_volume.id = self._cinderClient.createVolume(volumeName, volumeType_id, test_volume.size)
                except Exception as e:
                    self._loggers.basebenchLogger.error('创建云硬盘'+test_volume.name+'失败!'+'\r\n'+e.args.__str__())
                self._accountResource.add_volume(test_volume)

                # 申请一个浮动ip
                self._loggers.basebenchLogger.info('申请一个浮动ip')
                test_floatIp = FloatIp()
                try:
                    test_floatIp.ip = self._openstackClient.getFloatIp(self._admin_float_net_id)
                    test_floatIp.id = self._openstackClient.getFloatId(test_floatIp.ip)
                    self._loggers.basebenchLogger.info('申请到一个浮动ip:' + test_floatIp.ip)
                except Exception as e:
                    self._loggers.basebenchLogger.error('申请浮动ip失败!'+'\r\n'+e.args.__str__())
                self._accountResource.add_floatIp(test_floatIp)

                # 启动云主机
                test_compute = Compute()
                test_compute.name = computeName
                test_compute.testType = testType
                self._loggers.basebenchLogger.info('启动云主机'+test_compute.name)
                try:
                    test_compute.id = self._novaClient.bootCompute(computeName,
                                                                   self._test_fio_flavor_id,
                                                                   self._test_image_id,
                                                                   self._test_fio_net_id,
                                                                   self._default_secgroup_id,
                                                                   random.choice(self._zone_names),
                                                                   self._user_data_path)
                except Exception as e:
                    self._loggers.basebenchLogger.error('启动云主机'+test_compute.name+'失败!'+'\r\n'+e.args.__str__())

                # 绑定浮动ip
                self._loggers.basebenchLogger.info('为云主机'+test_compute.name+'绑定浮动ip:'+test_floatIp.ip)
                try:
                    is_add_succ = self._novaClient.addFloatForCompute(test_compute.id, test_floatIp.ip)
                    if is_add_succ:
                        test_compute.float_ip = test_floatIp.ip
                except Exception as e:
                    self._loggers.basebenchLogger.error('为云主机'+test_compute.name+'绑定浮动ip:'+test_floatIp.ip+'失败!'+'\r\n'+e.args.__str__())

                # 挂载云硬盘
                self._loggers.basebenchLogger.info('为云主机'+test_compute.name+'挂载云硬盘'+test_volume.name)
                try:
                    is_add_succ = self._novaClient.attachVolume(test_compute.id, test_volume.id, '/dev/vdc')
                    if is_add_succ:
                        test_compute.volumeName = test_volume.name
                        test_compute.volumeId = test_volume.id
                except Exception as e:
                    self._loggers.basebenchLogger.error('为云主机'+test_compute.name+'挂载云硬盘'+test_volume.name+'失败!'+'\r\n'+e.args.__str__())
                self._accountResource.add_fioCompute(test_compute)
                self._accountResource.add_compute(test_compute)

    def _initUnixbench(self):
        """
        根据unixbench所需要测试，设置要测试的网络/云主机名
        :return:
        """
        self._loggers.basebenchLogger.info('初始化unixbench的网络资源，创建名为' + self._test_unixbench_net_name + '的网络')
        test_unixbench_net = Net()
        test_unixbench_net.name = StrTool.addUUID(self._test_unixbench_net_name)
        test_unixbench_net.cidr = self._test_unixbench_subnet_cidr
        try:
            test_unixbench_net.id = self._openstackClient.createNetwork(test_unixbench_net.name, test_unixbench_net.cidr)
        except Exception as e:
            self._loggers.basebenchLogger.error('创网络' + self._test_unixbench_net_name + '失败!'+'\r\n'+e.args.__str__())
        self._unixbench_net_id = test_unixbench_net.id

        self._loggers.basebenchLogger.info('初始化unixbench路由器资源，创建名为' + self._test_unixbench_router_name + '的路由器')
        test_unixbench_router = Router()
        test_unixbench_router.name = StrTool.addUUID(self._test_unixbench_router_name)
        try:
            test_unixbench_router.id = self._openstackClient.createRouter(test_unixbench_router.name, self._admin_float_net_id)
        except Exception as e:
            self._loggers.basebenchLogger.error('初始化unixbench路由器' + test_unixbench_router.name + '失败!' + '\r\n' + e.args.__str__())
        self._loggers.basebenchLogger.info('将unixbench网络' + test_unixbench_net.name + '绑定到路由器' + test_unixbench_router.name)
        try:
            test_unixbench_net_subnet_id = self._openstackClient.getSubNetId(self._unixbench_net_id)
            self._openstackClient.addRouterInterface(test_unixbench_router.id, test_unixbench_net_subnet_id)
            test_unixbench_router.add_subnet_id(test_unixbench_net_subnet_id)
            test_unixbench_net.add_subnet_id(test_unixbench_net_subnet_id)
        except Exception as e:
            self._loggers.basebenchLogger.error('将unixbench网络' + test_unixbench_net.name + '绑定到路由器' + test_unixbench_router.name + '失败' + '\r\n' + e.args.__str__())
        self._accountResource.add_net(test_unixbench_net)
        self._accountResource.add_router(test_unixbench_router)

        self._loggers.basebenchLogger.info('初始化unixbench测试的云主机')
        test_unixbench_flavor_types=self._readConfig.executeTest.basebench_test_unixbench_flavors.split('||')
        for test_unixbench_flavor_type in test_unixbench_flavor_types:
            self._loggers.basebenchLogger.info('初始化unixbench测试的云主机规格')
            self._test_unixbench_flavor_id = getFlavorId(self._accountResource.get_flavors(), test_unixbench_flavor_type)
            computeName = StrTool.addUUID('basebench_unixbench_' + test_unixbench_flavor_type)
            testType = 'basebench_unixbench_' + test_unixbench_flavor_type
            # 申请一个浮动ip
            test_unixbench_floatIp = FloatIp()
            self._loggers.basebenchLogger.info('申请一个浮动ip')
            try:
                test_unixbench_floatIp.ip = self._openstackClient.getFloatIp(self._admin_float_net_id)
                test_unixbench_floatIp.id = self._openstackClient.getFloatId(test_unixbench_floatIp.ip)
                self._loggers.basebenchLogger.info('申请到一个浮动ip:' + test_unixbench_floatIp.ip)
            except Exception as e:
                self._loggers.basebenchLogger.error('申请浮动ip失败'+'\r\n'+e.args.__str__())
            self._accountResource.add_floatIp(test_unixbench_floatIp)

            # 启动云主机
            test_unixbench_compute = Compute()
            test_unixbench_compute.name = computeName
            test_unixbench_compute.testType = testType
            self._loggers.basebenchLogger.info('启动云主机' + test_unixbench_compute.name)
            try:
                test_unixbench_compute.id = self._novaClient.bootCompute(computeName,
                                                               self._test_unixbench_flavor_id,
                                                               self._test_image_id,
                                                               self._unixbench_net_id,
                                                               self._default_secgroup_id,
                                                               random.choice(self._zone_names),
                                                               self._user_data_path)
            except Exception as e:
                self._loggers.basebenchLogger.error('启动云主机'+test_unixbench_compute.name+'失败!'+'\r\n'+e.args.__str__())

            # 绑定浮动ip
            self._loggers.basebenchLogger.info('为云主机' + test_unixbench_compute.name + '绑定浮动ip:' + test_unixbench_floatIp.ip)
            try:
                is_add_succ = self._novaClient.addFloatForCompute(test_unixbench_compute.id, test_unixbench_floatIp.ip)
                if is_add_succ:
                    test_unixbench_compute.float_ip=test_unixbench_floatIp.ip
            except Exception as e:
                self._loggers.basebenchLogger.error('为云主机' + test_unixbench_compute.name + '绑定浮动ip:' + test_unixbench_floatIp.ip+'失败!'+'\r\n'+e.args.__str__())
            self._accountResource.add_unixbenchCompute(test_unixbench_compute)
            self._accountResource.add_compute(test_unixbench_compute)


    def _initIperf(self):
        """
        初始化iperf测试必须有的资源
        :return:
        """
        self._loggers.basebenchLogger.info('初始化iperf测试的云主机规格')
        self._test_iperf_flavor_id=getFlavorId(self._accountResource.get_flavors(),self._readConfig.executeTest.basebench_test_iperf_flavor)

        self._loggers.basebenchLogger.info('初始化iperf测试的网络'+self._test_iperf_net1_name+'和'+self._test_iperf_net2_name)
        test_iperf_net1=Net()
        test_iperf_net2 = Net()
        test_iperf_net1.name=self._test_iperf_net1_name
        test_iperf_net1.cidr = self._test_iperf_subnet1_cidr
        test_iperf_net2.name=self._test_iperf_net2_name
        test_iperf_net2.cidr=self._test_iperf_subnet2_cidr
        try:
            test_iperf_net1.id=self._openstackClient.createNetwork(self._test_iperf_net1_name,self._test_iperf_subnet1_cidr)
            test_iperf_net2.id = self._openstackClient.createNetwork(self._test_iperf_net2_name, self._test_iperf_subnet2_cidr)
        except Exception as e:
            self._loggers.basebenchLogger.error('初始化iperf测试的网络'+self._test_iperf_net1_name+'和'+self._test_iperf_net2_name+'失败!'+'\r\n'+e.args.__str__())
        self._test_iperf_net1_id=test_iperf_net1.id
        self._test_iperf_net2_id=test_iperf_net2.id

        self._loggers.basebenchLogger.info('初始化iperf路由器资源，创建名为' + self._test_iperf_router_name + '的路由器')
        test_iperf_router = Router()
        test_iperf_router.name = StrTool.addUUID(self._test_iperf_router_name)
        try:
            test_iperf_router.id = self._openstackClient.createRouter(test_iperf_router.name, self._admin_float_net_id)
        except Exception as e:
            self._loggers.basebenchLogger.error('初始化iperf路由器' + test_iperf_router.name + '失败!' + '\r\n' + e.args.__str__())
        self._loggers.basebenchLogger.info('将iperf网络' + self._test_iperf_net1_name + '绑定到路由器' + test_iperf_router.name)
        try:
            test_iperf_net1_subnet_id=self._openstackClient.getSubNetId(self._test_iperf_net1_id)
            self._openstackClient.addRouterInterface(test_iperf_router.id,test_iperf_net1_subnet_id)
            test_iperf_router.add_subnet_id(test_iperf_net1_subnet_id)
            test_iperf_net1.add_subnet_id(test_iperf_net1_subnet_id)
        except Exception as e:
            self._loggers.basebenchLogger.error('将iperf网络' + self._test_iperf_net1_name + '绑定到路由器' + test_iperf_router.name +'失败!'+'\r\n'+e.args.__str__())
        self._loggers.basebenchLogger.info('将iperf网络' + self._test_iperf_net2_name + '绑定到路由器' + test_iperf_router.name)
        try:
            test_iperf_net2_subnet_id = self._openstackClient.getSubNetId(self._test_iperf_net2_id)
            self._openstackClient.addRouterInterface(test_iperf_router.id, test_iperf_net2_subnet_id)
            test_iperf_router.add_subnet_id(test_iperf_net2_subnet_id)
            test_iperf_net2.add_subnet_id(test_iperf_net2_subnet_id)
        except Exception as e:
            self._loggers.basebenchLogger.error('将iperf网络' + self._test_iperf_net2_name + '绑定到路由器' + test_iperf_router.name+'失败!'+'\r\n'+e.args.__str__())
        self._accountResource.add_net(test_iperf_net1)
        self._accountResource.add_net(test_iperf_net2)
        self._accountResource.add_router(test_iperf_router)

        self._loggers.basebenchLogger.info('初始化iperf测试的云主机')
        self._loggers.basebenchLogger.info('启动两组iperf测试云主机，同网段和不同网段')
        for i in range(2):
            #获取可用域
            if len(self._zone_names)<2:
                self._loggers.basebenchLogger.error('可用域'+self._zone_names.__str__()+'少于两个无法进行iperf测试')
                return

            # 启动2组iperf测试云主机，同网段和不同网段
            iperf_computePair=[]
            for j in range(2):
                #申请一个浮动ip
                test_floatIp = FloatIp()
                self._loggers.basebenchLogger.info('申请一个浮动ip')
                try:
                    test_floatIp.ip = self._openstackClient.getFloatIp(self._admin_float_net_id)
                    test_floatIp.id = self._openstackClient.getFloatId(test_floatIp.ip)
                    self._loggers.basebenchLogger.info('申请到一个浮动ip:' + test_floatIp.ip)
                except Exception as e:
                    self._loggers.basebenchLogger.error('申请浮动ip失败!'+'\r\n'+e.args.__str__())
                self._accountResource.add_floatIp(test_floatIp)

                # tmp_zone=None
                # tmp_net=None
                # tmp_testType=None
                # tmp_name=None
                #同网段
                if i==0 and j==0:
                    self._loggers.basebenchLogger.info('启动同网段的第一台云主机')
                    tmp_zone=self._zone_names[0]
                    tmp_net=self._test_iperf_net1_id
                    tmp_testType='basebench_iperf_one_net'
                    tmp_name=StrTool.addUUID('basebench_iperf_one_' + str(j))
                #同网段
                elif i==0 and j==1:
                    self._loggers.basebenchLogger.info('启动同网段的第二台云主机')
                    tmp_zone=self._zone_names[1]
                    tmp_net=self._test_iperf_net1_id
                    tmp_testType = 'basebench_iperf_one_net'
                    tmp_name = StrTool.addUUID('basebench_iperf_one_' + str(j))
                #不同网段
                elif i==1 and j==0:
                    self._loggers.basebenchLogger.info('启动不同网段的第一台云主机')
                    tmp_zone=self._zone_names[0]
                    tmp_net=self._test_iperf_net1_id
                    tmp_testType = 'basebench_iperf_two_net'
                    tmp_name = StrTool.addUUID('basebench_iperf_two_' + str(j))
                #不同网段
                else:
                    self._loggers.basebenchLogger.info('启动不同网段的第二台云主机')
                    tmp_zone=self._zone_names[1]
                    tmp_net = self._test_iperf_net2_id
                    tmp_testType = 'basebench_iperf_two_net'
                    tmp_name = StrTool.addUUID('basebench_iperf_two_' + str(j))
                #创建云主机
                test_compute = Compute()
                test_compute.name=tmp_name
                test_compute.testType = tmp_testType
                self._loggers.basebenchLogger.info('启动云主机' + test_compute.name)
                try:
                    test_compute.id=self._novaClient.bootCompute(test_compute.name,
                                                                 self._test_iperf_flavor_id,
                                                                 self._test_image_id,
                                                                 tmp_net,
                                                                 self._default_secgroup_id,
                                                                 tmp_zone,
                                                                 self._user_data_path)
                    test_compute.ip = self._novaClient.getComputeIp(test_compute.name)
                except Exception as e:
                    self._loggers.basebenchLogger.error('启动云主机'+test_compute.name+'失败!'+'\r\n'+e.args.__str__())

                #绑定浮动ip
                self._loggers.basebenchLogger.info('为云主机' + test_compute.name + '绑定浮动ip:' + test_floatIp.ip)
                try:
                    is_add_succ=self._novaClient.addFloatForCompute(test_compute.id,test_floatIp.ip)
                    if is_add_succ:
                        test_compute.float_ip=test_floatIp.ip
                except Exception as e:
                    self._loggers.basebenchLogger.error('为云主机' + test_compute.name + '绑定浮动ip:' + test_floatIp.ip+'失败!'+'\r\n'+e.args.__str__())
                iperf_computePair.append(test_compute)
                self._accountResource.add_compute(test_compute)
                #设置一组iperf云主机
            self._accountResource.add_iperfComputePair(iperf_computePair)

    def getBasebenchTestAccountResource(self):
        return self._accountResource


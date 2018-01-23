#!-*- coding:utf8 -*-
from src.clients.neutronClient import NeutronClient
from src.clients.cinderClient import CinderClient
from src.clients.novaClient import NovaClient
from config.config import DEFAULT_SECGROUP_NAME
from config.config import TEST_FIO_FLAVOR
from config.config import TEST_IMAGE_NAME
from config.config import ADMIN_FLOAT_NET_NAME
from config.config import ZONE_NAMES
from config.config import TEST_FIO_VOLUME_TYPE
from config.config import WHAT_FIO_TEST
from config.config import TEST_FIO_VOLUME_SIZE
from config.config import IS_TEST_FIO
from config.config import IS_TEST_UNIXBENCH
from config.config import IS_TEST_IPERF
from config.config import FLOAT_IP_QOS
from config.config import BASE_ACCOUNT_OS_TENANT_NAME
from config.config import BASE_ACCOUNT_OS_PROJECT_NAME
from config.config import BASE_ACCOUNT_OS_USERNAME
from config.config import BASE_ACCOUNT_OS_PASSWORD
from config.config import TEST_UNIXBENCH_FLAVOR
from config.config import TEST_IPERF_FLAVOR
from src.common import addUUID
from src.common import writeObjectIntoFile
from src.pojo.Compute import Compute
from src.pojo.NET import Net
from src.pojo.Router import Router
from src.pojo.Volume import Volume
from src.pojo.FloatIp import FloatIp
from src.logger import basePerformanceLogger
from src.init import Init
from src.accountResourceTools import getDefaultSecGroupId
from src.accountResourceTools import getAdminFloatNetId
from src.accountResourceTools import getTestImageId
from src.accountResourceTools import getFlavorId
from src.accountResourceTools import getVolumeTypeId
import random

class InitResource():
    def __init__(self):
        self._os_tenant_name=BASE_ACCOUNT_OS_TENANT_NAME
        self._os_project_name=BASE_ACCOUNT_OS_PROJECT_NAME
        self._os_username =BASE_ACCOUNT_OS_USERNAME
        self._os_password=BASE_ACCOUNT_OS_PASSWORD

        self._init=Init(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password,basePerformanceLogger)
        self._accountResource = self._init.initAccountResource()

        self._router_name='base_router'
        self._user_data_path='userdata/user_data'

        self._test_fio_net_name='fio_net'
        self._test_fio_subnet_cidr='192.168.50.0/24'

        self._test_iperf_net1_name='iperf_net1'
        self._test_iperf_subnet1_cidr='192.168.70.0/24'
        self._test_iperf_net2_name='iperf_net2'
        self._test_iperf_subnet2_cidr = '192.168.80.0/24'

        self._test_unixbench_net_name = 'unixbench_net'
        self._test_unixbench_subnet_cidr = '192.168.60.0/24'

        basePerformanceLogger.info('===初始化基准测试基础资源===')
        self._initResource()

    def _initResource(self):
        """
        公共资源初始化
        :return:
        """
        basePerformanceLogger.info('初始化命令行客户端')
        self._neutronClient=NeutronClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._novaClient=NovaClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._cinderClient=CinderClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)

        basePerformanceLogger.info('初始化默认安全组、测试镜像、测试镜像')
        self._default_secgroup_id=getDefaultSecGroupId(self._accountResource.get_secgroups(),DEFAULT_SECGROUP_NAME)
        self._admin_float_net_id=getAdminFloatNetId(self._accountResource.get_adminNets(),ADMIN_FLOAT_NET_NAME)
        self._test_image_id=getTestImageId(self._accountResource.get_images(),TEST_IMAGE_NAME)

        basePerformanceLogger.info('初始化一个路由器资源，创建名为' + self._router_name + '的路由')
        test_router=Router()
        test_router.name=addUUID(self._router_name)
        try:
            test_router.id=self._neutronClient.createRouter(test_router.name,self._admin_float_net_id)
        except Exception,e:
            basePerformanceLogger.error('初始化路由器'+test_router.name+'失败!'+'\r\n'+e.message)
        self._router_id = test_router.id
        self._accountResource.add_router(test_router)

        #判断需要测试的类型
        if IS_TEST_FIO:
            basePerformanceLogger.info('===开始初始化fio资源===')
            self._initFio()
        if IS_TEST_UNIXBENCH:
            basePerformanceLogger.info('===开始初始化unixbench资源===')
            self._initUnixbench()
        if IS_TEST_IPERF:
            basePerformanceLogger.info('===开始初始化iperf资源===')
            self._initIperf()

        basePerformanceLogger.info('将测试初始化资源写入到文件dbs/basePerformanceTestAccountResource.dbs')
        writeObjectIntoFile(self._accountResource,'dbs/basePerformanceTestAccountResource.dbs')

    def _initFio(self):
        """
        根据fio所需要测试，设置要测试的网络/云主机名/云硬盘名
        :return:
        """
        basePerformanceLogger.info('初始化fio测试的云主机规格')
        self._test_fio_flavor_id = getFlavorId(self._accountResource.get_flavors(), TEST_FIO_FLAVOR)

        basePerformanceLogger.info('初始化fio网络资源，创建名为' + self._test_fio_net_name + '的网络')
        test_fio_net = Net()
        test_fio_net.name = addUUID(self._test_fio_net_name)
        test_fio_net.cidr = self._test_fio_subnet_cidr
        try:
            test_fio_net.id = self._neutronClient.createNetwork(test_fio_net.name, test_fio_net.cidr)
        except Exception,e:
            basePerformanceLogger.error('创建网络'+test_fio_net.name+'失败!'+'\r\n'+e.message)
        self._test_fio_net_id = test_fio_net.id
        self._accountResource.add_net(test_fio_net)

        basePerformanceLogger.info('将fio网络' + test_fio_net.name + '绑定到路由器' + self._router_name)
        try:
            test_fio_net_subnet_id = self._neutronClient.getSubNetId(self._test_fio_net_id)
            self._neutronClient.addRouterInterface(self._router_id, test_fio_net_subnet_id)
        except Exception,e:
            basePerformanceLogger.error('将fio网络' + test_fio_net.name + '绑定到路由器' +self._router_name+'失败'+'\r\n'+e.message)

        basePerformanceLogger.info('初始化fio测试的云主机')
        for test_fio_volume_type in TEST_FIO_VOLUME_TYPE:
            volumeType_id = getVolumeTypeId(self._accountResource.get_volumeTypes(), test_fio_volume_type)
            for test_fio_type in WHAT_FIO_TEST:
                volumeName = addUUID('fio_' + test_fio_type + test_fio_volume_type)
                computeName = addUUID('fio_' + test_fio_type + test_fio_volume_type)
                testType = test_fio_type + test_fio_volume_type
                # 创建云硬盘
                test_volume = Volume()
                test_volume.name = volumeName
                test_volume.size = TEST_FIO_VOLUME_SIZE
                test_volume.type = test_fio_volume_type
                basePerformanceLogger.info('创建云硬盘'+test_volume.name)
                try:
                    test_volume.id = self._cinderClient.createVolume(volumeName, volumeType_id, TEST_FIO_VOLUME_SIZE)
                except Exception,e:
                    basePerformanceLogger.error('创建云硬盘'+test_volume.name+'失败!'+'\r\n'+e.message)
                self._accountResource.add_volume(test_volume)

                # 申请一个浮动ip
                basePerformanceLogger.info('申请一个浮动ip')
                test_floatIp = FloatIp()
                try:
                    test_floatIp.ip = self._neutronClient.getFloatIp(self._admin_float_net_id, FLOAT_IP_QOS)
                    test_floatIp.id = self._neutronClient.getFloatId(test_floatIp.ip)
                    basePerformanceLogger.info('申请到一个浮动ip:' + test_floatIp.ip)
                except Exception,e:
                    basePerformanceLogger.error('申请浮动ip失败!'+'\r\n'+e.message)
                self._accountResource.add_floatIp(test_floatIp)

                # 启动云主机
                test_compute = Compute()
                test_compute.name = computeName
                test_compute.testType = testType
                basePerformanceLogger.info('启动云主机'+test_compute.name)
                try:
                    test_compute.id = self._novaClient.bootCompute(computeName,
                                                                   self._test_fio_flavor_id,
                                                                   self._test_image_id,
                                                                   self._test_fio_net_id,
                                                                   self._default_secgroup_id,
                                                                   random.choice(ZONE_NAMES),
                                                                   self._user_data_path)
                except Exception,e:
                    basePerformanceLogger.error('启动云主机'+test_compute.name+'失败!'+'\r\n'+e.message)

                # 绑定浮动ip
                basePerformanceLogger.info('为云主机'+test_compute.name+'绑定浮动ip:'+test_floatIp.ip)
                try:
                    is_add_succ = self._novaClient.addFloatForCompute(test_compute.id, test_floatIp.ip)
                    if is_add_succ:
                        test_compute.float_ip = test_floatIp.ip
                except Exception,e:
                    basePerformanceLogger.error('为云主机'+test_compute.name+'绑定浮动ip:'+test_floatIp.ip+'失败!'+'\r\n'+e.message)

                # 挂载云硬盘
                basePerformanceLogger.info('为云主机'+test_compute.name+'挂载云硬盘'+test_volume.name)
                try:
                    is_add_succ = self._novaClient.attachVolume(test_compute.id, test_volume.id, '/dev/vdb')
                    if is_add_succ:
                        test_compute.volumeName = test_volume.name
                        test_compute.volumeId = test_volume.id
                except Exception,e:
                    basePerformanceLogger.error('为云主机'+test_compute.name+'挂载云硬盘'+test_volume.name+'失败!'+'\r\n'+e.message)
                self._accountResource.add_fioCompute(test_compute)
                self._accountResource.add_compute(test_compute)

    def _initUnixbench(self):
        """
        根据unixbench所需要测试，设置要测试的网络/云主机名
        :return:
        """
        basePerformanceLogger.info('初始化unixbench的网络资源，创建名为' + self._test_unixbench_net_name + '的网络')
        test_unixbench_net = Net()
        test_unixbench_net.name = addUUID(self._test_unixbench_net_name)
        test_unixbench_net.cidr = self._test_unixbench_subnet_cidr
        try:
            test_unixbench_net.id = self._neutronClient.createNetwork(test_unixbench_net.name, test_unixbench_net.cidr)
        except Exception,e:
            basePerformanceLogger.error('创网络' + self._test_unixbench_net_name + '失败!'+'\r\n'+e.message)
        self._unixbench_net_id = test_unixbench_net.id
        self._accountResource.add_net(test_unixbench_net)

        basePerformanceLogger.info('将unixbench的网络' + self._test_unixbench_net_name + '绑定到路由器' + self._router_name)
        try:
            unixbench_net_subnet_id = self._neutronClient.getSubNetId(self._unixbench_net_id)
            self._neutronClient.addRouterInterface(self._router_id, unixbench_net_subnet_id)
        except Exception,e:
            basePerformanceLogger.error('将络' + self._test_unixbench_net_name + '绑定到路由器' + self._router_name+'失败!'+'\r\n'+e.message)

        basePerformanceLogger.info('初始化unixbench测试的云主机')
        for test_unixbench_flavor_type in TEST_UNIXBENCH_FLAVOR:
            basePerformanceLogger.info('初始化unixbench测试的云主机规格')
            self._test_unixbench_flavor_id = getFlavorId(self._accountResource.get_flavors(), test_unixbench_flavor_type)
            computeName = addUUID('unixbench_' + test_unixbench_flavor_type)
            testType = 'unixbench_' + test_unixbench_flavor_type
            # 申请一个浮动ip
            test_unixbench_floatIp = FloatIp()
            basePerformanceLogger.info('申请一个浮动ip')
            try:
                test_unixbench_floatIp.ip = self._neutronClient.getFloatIp(self._admin_float_net_id, FLOAT_IP_QOS)
                test_unixbench_floatIp.id = self._neutronClient.getFloatId(test_unixbench_floatIp.ip)
                basePerformanceLogger.info('申请到一个浮动ip:' + test_unixbench_floatIp.ip)
            except Exception,e:
                basePerformanceLogger.error('申请浮动ip失败'+'\r\n'+e.message)
            self._accountResource.add_floatIp(test_unixbench_floatIp)

            # 启动云主机
            test_unixbench_compute = Compute()
            test_unixbench_compute.name = computeName
            test_unixbench_compute.testType = testType
            basePerformanceLogger.info('启动云主机' + test_unixbench_compute.name)
            try:
                test_unixbench_compute.id = self._novaClient.bootCompute(computeName,
                                                               self._test_unixbench_flavor_id,
                                                               self._test_image_id,
                                                               self._unixbench_net_id,
                                                               self._default_secgroup_id,
                                                               random.choice(ZONE_NAMES),
                                                               self._user_data_path)
            except Exception,e:
                basePerformanceLogger.error('启动云主机'+test_unixbench_compute.name+'失败!'+'\r\n'+e.message)

            # 绑定浮动ip
            basePerformanceLogger.info('为云主机' + test_unixbench_compute.name + '绑定浮动ip:' + test_unixbench_floatIp.ip)
            try:
                is_add_succ = self._novaClient.addFloatForCompute(test_unixbench_compute.id, test_unixbench_floatIp.ip)
                if is_add_succ:
                    test_unixbench_compute.float_ip=test_unixbench_floatIp.ip
            except Exception,e:
                basePerformanceLogger.error('为云主机' + test_unixbench_compute.name + '绑定浮动ip:' + test_unixbench_floatIp.ip+'失败!'+'\r\n'+e.message)
            self._accountResource.add_unixbenchCompute(test_unixbench_compute)
            self._accountResource.add_compute(test_unixbench_compute)


    def _initIperf(self):
        """
        初始化iperf测试必须有的资源
        :return:
        """
        basePerformanceLogger.info('初始化iperf测试的云主机规格')
        self._test_iperf_flavor_id=getFlavorId(self._accountResource.get_flavors(),TEST_IPERF_FLAVOR)

        basePerformanceLogger.info('初始化iperf测试的网络'+self._test_iperf_net1_name+'和'+self._test_iperf_net2_name)
        test_iperf_net1=Net()
        test_iperf_net2 = Net()
        test_iperf_net1.name=self._test_iperf_net1_name
        test_iperf_net1.cidr = self._test_iperf_subnet1_cidr
        test_iperf_net2.name=self._test_iperf_net2_name
        test_iperf_net2.cidr=self._test_iperf_subnet2_cidr
        try:
            test_iperf_net1.id=self._neutronClient.createNetwork(self._test_iperf_net1_name,self._test_iperf_subnet1_cidr)
            test_iperf_net2.id = self._neutronClient.createNetwork(self._test_iperf_net2_name, self._test_iperf_subnet2_cidr)
        except Exception,e:
            basePerformanceLogger.error('初始化iperf测试的网络'+self._test_iperf_net1_name+'和'+self._test_iperf_net2_name+'失败!'+'\r\n'+e.message)
        self._test_iperf_net1_id=test_iperf_net1.id
        self._test_iperf_net2_id=test_iperf_net2.id
        self._accountResource.add_net(test_iperf_net1)
        self._accountResource.add_net(test_iperf_net2)

        basePerformanceLogger.info('将iperf网络' + self._test_iperf_net1_name + '绑定到路由器' + self._router_name)
        try:
            test_iperf_net1_subnet_id=self._neutronClient.getSubNetId(self._test_iperf_net1_id)
            self._neutronClient.addRouterInterface(self._router_id,test_iperf_net1_subnet_id)
        except Exception,e:
            basePerformanceLogger.error('将iperf网络' + self._test_iperf_net1_name + '绑定到路由器' + self._router_name+'失败!'+'\r\n'+e.message)

        basePerformanceLogger.info('将iperf网络' + self._test_iperf_net2_name + '绑定到路由器' + self._router_name)
        try:
            test_iperf_net2_subnet_id = self._neutronClient.getSubNetId(self._test_iperf_net2_id)
            self._neutronClient.addRouterInterface(self._router_id, test_iperf_net2_subnet_id)
        except Exception,e:
            basePerformanceLogger.error('将iperf网络' + self._test_iperf_net2_name + '绑定到路由器' + self._router_name+'失败!'+'\r\n'+e.message)

        basePerformanceLogger.info('初始化iperf测试的云主机')
        basePerformanceLogger.info('启动两组iperf测试云主机，同网段和不同网段')
        for i in range(2):
            #获取可用域
            if len(ZONE_NAMES)<2:
                basePerformanceLogger.error('可用域'+ZONE_NAMES+'少于两个无法进行iperf测试')
                return

            # 启动2组iperf测试云主机，同网段和不同网段
            iperf_computePair=[]
            for j in range(2):
                #申请一个浮动ip
                test_floatIp = FloatIp()
                basePerformanceLogger.info('申请一个浮动ip')
                try:
                    test_floatIp.ip = self._neutronClient.getFloatIp(self._admin_float_net_id, FLOAT_IP_QOS)
                    test_floatIp.id = self._neutronClient.getFloatId(test_floatIp.ip)
                    basePerformanceLogger.info('申请到一个浮动ip:' + test_floatIp.ip)
                except Exception,e:
                    basePerformanceLogger.error('申请浮动ip失败!'+'\r\n'+e.message)
                self._accountResource.add_floatIp(test_floatIp)

                tmp_zone=None
                tmp_net=None
                tmp_testType=None
                tmp_name=None
                #同网段
                if i==0 and j==0:
                    basePerformanceLogger.info('启动同网段的第一台云主机')
                    tmp_zone=ZONE_NAMES[0]
                    tmp_net=self._test_iperf_net1_id
                    tmp_testType='iperf_one_net'
                    tmp_name=addUUID('iperf_one_' + str(j))
                #同网段
                elif i==0 and j==1:
                    basePerformanceLogger.info('启动同网段的第二台云主机')
                    tmp_zone=ZONE_NAMES[1]
                    tmp_net=self._test_iperf_net1_id
                    tmp_testType = 'iperf_one_net'
                    tmp_name = addUUID('iperf_one_' + str(j))
                #不同网段
                elif i==1 and j==0:
                    basePerformanceLogger.info('启动不同网段的第一台云主机')
                    tmp_zone=ZONE_NAMES[0]
                    tmp_net=self._test_iperf_net1_id
                    tmp_testType = 'iperf_two_net'
                    tmp_name = addUUID('iperf_two_' + str(j))
                #不同网段
                else:
                    basePerformanceLogger.info('启动不同网段的第二台云主机')
                    tmp_zone=ZONE_NAMES[1]
                    tmp_net = self._test_iperf_net2_id
                    tmp_testType = 'iperf_two_net'
                    tmp_name = addUUID('iperf_two_' + str(j))
                #创建云主机
                test_compute = Compute()
                test_compute.name=tmp_name
                test_compute.testType = tmp_testType
                basePerformanceLogger.info('启动云主机' + test_compute.name)
                try:
                    test_compute.id=self._novaClient.bootCompute(test_compute.name,
                                                                 self._test_iperf_flavor_id,
                                                                 self._test_image_id,
                                                                 tmp_net,
                                                                 self._default_secgroup_id,
                                                                 tmp_zone,
                                                                 self._user_data_path)
                    test_compute.ip = self._novaClient.getComputeIp(test_compute.name)
                except Exception,e:
                    basePerformanceLogger.error('启动云主机'+test_compute.name+'失败!'+'\r\n'+e.message)

                #绑定浮动ip
                basePerformanceLogger.info('为云主机' + test_compute.name + '绑定浮动ip:' + test_floatIp.ip)
                try:
                    is_add_succ=self._novaClient.addFloatForCompute(test_compute.id,test_floatIp.ip)
                    if is_add_succ:
                        test_compute.float_ip=test_floatIp.ip
                except Exception,e:
                    basePerformanceLogger.error('为云主机' + test_compute.name + '绑定浮动ip:' + test_floatIp.ip+'失败!'+'\r\n'+e.message)
                iperf_computePair.append(test_compute)
                self._accountResource.add_compute(test_compute)
                #设置一组iperf云主机
            self._accountResource.add_iperfComputePair(iperf_computePair)

    def getBasePerformanceAccountResource(self):
        return self._accountResource


#!-*- coding:utf8 -*-
from src.clients.neutronClient import NeutronClient
from src.clients.cinderClient import CinderClient
from src.clients.novaClient import NovaClient
from config.config import DEFAULT_SECGROUP_NAME
from config.config import TEST_IMAGE_NAME
from config.config import ADMIN_FLOAT_NET_NAME
from config.config import ZONE_NAMES
from config.config import IS_STABILITY_TEST_IPERF
from config.config import FLOAT_IP_QOS
from config.config import STABILITY_IPERF_ACCOUNT_OS_TENANT_NAME
from config.config import STABILITY_IPERF_ACCOUNT_OS_PROJECT_NAME
from config.config import STABILITY_IPERF_ACCOUNT_OS_USERNAME
from config.config import STABILITY_IPERF_ACCOUNT_OS_PASSWORD
from config.config import STABILITY_TEST_IPERF_FLAVOR
from config.config import STABILITY_TEST_IPERF_GROUP_NUM
from src.common import addUUID
from src.common import writeObjectIntoFile
from src.pojo.Compute import Compute
from src.pojo.NET import Net
from src.pojo.Router import Router
from src.pojo.FloatIp import FloatIp
from src.logger import stabilityIperfLogger
from src.init import Init
from src.accountResourceTools import getDefaultSecGroupId
from src.accountResourceTools import getAdminFloatNetId
from src.accountResourceTools import getTestImageId
from src.accountResourceTools import getFlavorId

class InitIperfResource():
    def __init__(self):
        self._os_tenant_name=STABILITY_IPERF_ACCOUNT_OS_TENANT_NAME
        self._os_project_name=STABILITY_IPERF_ACCOUNT_OS_PROJECT_NAME
        self._os_username =STABILITY_IPERF_ACCOUNT_OS_USERNAME
        self._os_password=STABILITY_IPERF_ACCOUNT_OS_PASSWORD

        self._init=Init(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password,stabilityIperfLogger)
        self._accountResource = self._init.initAccountResource()

        self._router_name = 'iperf_router'
        self._user_data_path='userdata/user_data'

        self._test_iperf_net1_name = 'iperf_net1'
        self._test_iperf_subnet1_cidr = '192.168.70.0/24'
        self._test_iperf_net2_name = 'iperf_net2'
        self._test_iperf_subnet2_cidr = '192.168.80.0/24'

        stabilityIperfLogger.info('===初始化稳定性测试基础资源[iperf账号]===')
        self._initResource()

    def _initResource(self):
        """
        公共资源初始化
        :return:
        """
        stabilityIperfLogger.info('初始化命令行客户端')
        self._neutronClient=NeutronClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._novaClient=NovaClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._cinderClient=CinderClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)

        stabilityIperfLogger.info('初始化默认安全组、测试镜像、测试镜像')
        self._default_secgroup_id=getDefaultSecGroupId(self._accountResource.get_secgroups(),DEFAULT_SECGROUP_NAME)
        self._admin_float_net_id=getAdminFloatNetId(self._accountResource.get_adminNets(),ADMIN_FLOAT_NET_NAME)
        self._test_image_id=getTestImageId(self._accountResource.get_images(),TEST_IMAGE_NAME)

        stabilityIperfLogger.info('初始化一个路由器资源，创建名为' + self._router_name + '的路由')
        test_router=Router()
        test_router.name=addUUID(self._router_name)
        try:
            test_router.id=self._neutronClient.createRouter(test_router.name,self._admin_float_net_id)
        except Exception,e:
            stabilityIperfLogger.error('创建路由器'+self._router_name+'失败!'+'\r\n'+e.message)
        self._router_id=test_router.id
        self._accountResource.add_router(test_router)

        #判断需要测试的类型
        if IS_STABILITY_TEST_IPERF:
            stabilityIperfLogger.info('===开始初始化稳定性测试iperf资源===')
            self._initIperf()

        stabilityIperfLogger.info('将测试初始化资源写入到文件dbs/stabilityIperfTestAccountResource.dbs')
        writeObjectIntoFile(self._accountResource,'dbs/stabilityIperfTestAccountResource.dbs')


    def _initIperf(self):
        """
        初始化iperf测试必须有的资源
        :return:
        """
        stabilityIperfLogger.info('初始化iperf测试的云主机规格')
        self._test_iperf_flavor_id=getFlavorId(self._accountResource.get_flavors(),STABILITY_TEST_IPERF_FLAVOR)

        stabilityIperfLogger.info('初始化iperf测试的网络'+self._test_iperf_net1_name+'和'+self._test_iperf_net2_name)
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
            stabilityIperfLogger.error('初始化iperf测试的网络'+self._test_iperf_net1_name+'和'+self._test_iperf_net2_name+'失败!'+'\r\n'+e.message)
        self._test_iperf_net1_id=test_iperf_net1.id
        self._test_iperf_net2_id=test_iperf_net2.id
        self._accountResource.add_net(test_iperf_net1)
        self._accountResource.add_net(test_iperf_net2)

        stabilityIperfLogger.info('将iperf网络' + self._test_iperf_net1_name + '绑定到路由器' + self._router_name)
        try:
            test_iperf_net1_subnet_id=self._neutronClient.getSubNetId(self._test_iperf_net1_id)
            self._neutronClient.addRouterInterface(self._router_id,test_iperf_net1_subnet_id)
        except Exception,e:
            stabilityIperfLogger.error('将iperf网络' + self._test_iperf_net1_name + '绑定到路由器' + self._router_name+'失败!'+e.message)
        stabilityIperfLogger.info('将iperf网络' + self._test_iperf_net2_name + '绑定到路由器' + self._router_name)
        try:
            test_iperf_net2_subnet_id = self._neutronClient.getSubNetId(self._test_iperf_net2_id)
            self._neutronClient.addRouterInterface(self._router_id, test_iperf_net2_subnet_id)
        except Exception,e:
            stabilityIperfLogger.error('将iperf网络' + self._test_iperf_net2_name + '绑定到路由器' + self._router_name+'失败!'+e.message)

        # 获取可用域
        if len(ZONE_NAMES) < 2:
            stabilityIperfLogger.error('可用域' + ZONE_NAMES + '少于两个无法进行iperf测试')
            return

        for i in range(STABILITY_TEST_IPERF_GROUP_NUM):
            stabilityIperfLogger.info('初始化iperf测试的云主机')
            # 启动一组iperf测试云主机,不同网段
            stabilityIperfLogger.info('启动一组iperf测试的云主机,在不同网段')
            iperf_computePair=[]
            for j in range(2):
                #申请一个浮动ip
                stabilityIperfLogger.info('申请一个浮动ip')
                test_floatIp = FloatIp()
                try:
                    test_floatIp.ip = self._neutronClient.getFloatIp(self._admin_float_net_id, FLOAT_IP_QOS)
                    test_floatIp.id = self._neutronClient.getFloatId(test_floatIp.ip)
                    stabilityIperfLogger.info('申请到一个浮动ip:' + test_floatIp.ip)
                except Exception,e:
                    stabilityIperfLogger.error('申请浮动ip失败!'+'\r\n'+e.message)
                self._accountResource.add_floatIp(test_floatIp)

                zone=None
                net_id=None
                tmp_testType = 'iperf_two_net'
                name=None
                #第一台
                if j==0:
                    stabilityIperfLogger.info('启动第一台云主机')
                    zone=ZONE_NAMES[0]
                    net_id=self._test_iperf_net1_id
                    name=addUUID('iperf_' + str(i)+'_'+str(j))
                #第二台
                elif j==1:
                    stabilityIperfLogger.info('启动第二台云主机')
                    zone=ZONE_NAMES[1]
                    net_id=self._test_iperf_net2_id
                    name = addUUID('iperf_' + str(i)+'_'+str(j))

                #创建云主机
                test_compute = Compute()
                test_compute.name=name
                test_compute.testType = tmp_testType
                stabilityIperfLogger.info('启动云主机' + test_compute.name)
                try:
                    test_compute.id=self._novaClient.bootCompute(test_compute.name,
                                                                 self._test_iperf_flavor_id,
                                                                 self._test_image_id,
                                                                 net_id,
                                                                 self._default_secgroup_id,
                                                                 zone,
                                                                 self._user_data_path)
                    test_compute.ip = self._novaClient.getComputeIp(test_compute.name)
                except Exception,e:
                    stabilityIperfLogger.error('启动云主机'+test_compute.name+'失败!'+'\r\n'+e.message)
                #绑定浮动ip
                stabilityIperfLogger.info('为云主机' + test_compute.name + '绑定浮动ip:' + test_floatIp.ip)
                try:
                    is_add_succ=self._novaClient.addFloatForCompute(test_compute.id,test_floatIp.ip)
                    if is_add_succ:
                        test_compute.float_ip=test_floatIp.ip
                except Exception,e:
                    stabilityIperfLogger.error('为云主机' + test_compute.name + '绑定浮动ip:' + test_floatIp.ip+'失败!'+'\r\n'+e.message)
                iperf_computePair.append(test_compute)
                self._accountResource.add_compute(test_compute)
                #设置一组iperf云主机
            self._accountResource.add_iperfComputePair(iperf_computePair)

    def getStabilityIperfAccountResource(self):
        return self._accountResource


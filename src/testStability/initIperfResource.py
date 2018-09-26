#!-*- coding:utf8 -*-
from src.clients.openstackClient import OpenstackClient
from src.clients.cinderClient import CinderClient
from src.clients.novaClient import NovaClient
from src.common.fileTool import FileTool
from src.loggers import Loggers
from src.readConfig import ReadConfig
from src.common.strTool import StrTool
from src.pojo.Compute import Compute
from src.pojo.NET import Net
from src.pojo.Router import Router
from src.pojo.FloatIp import FloatIp
from src.init import Init
from src.accountResourceTools import getDefaultSecGroupId
from src.accountResourceTools import getAdminFloatNetId
from src.accountResourceTools import getTestImageId
from src.accountResourceTools import getFlavorId

class InitIperfResource:
    def __init__(self):
        self._readConfig=ReadConfig()
        self._loggers=Loggers()

        self._os_tenant_name=self._readConfig.accounts.stability_iperf_os_tenant_name
        self._os_project_name=self._readConfig.accounts.stability_iperf_os_project_name
        self._os_username =self._readConfig.accounts.stability_iperf_os_username
        self._os_password=self._readConfig.accounts.stability_iperf_os_password

        self._init=Init(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password,self._loggers.stabilityIperfLogger)
        self._accountResource = self._init.initAccountResource()

        self._router_name = 'basebench_iperf_router'
        self._user_data_path='userdata/user_data'

        self._test_iperf_net1_name = 'basebench_iperf_net1'
        self._test_iperf_subnet1_cidr = '192.168.70.0/24'
        self._test_iperf_net2_name = 'basebench_iperf_net2'
        self._test_iperf_subnet2_cidr = '192.168.80.0/24'

        self._loggers.stabilityIperfLogger.info('===初始化稳定性测试基础资源[iperf账号]===')
        self._initResource()

    def _initResource(self):
        """
        公共资源初始化
        :return:
        """
        self._loggers.stabilityIperfLogger.info('初始化命令行客户端')
        self._openstackClient=OpenstackClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._novaClient=NovaClient(self._os_project_name,self._os_username,self._os_password)
        self._cinderClient=CinderClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)

        self._loggers.stabilityIperfLogger.info('初始化默认安全组、测试镜像、测试镜像')
        self._default_secgroup_id=getDefaultSecGroupId(self._accountResource.get_secgroups(),self._readConfig.base.default_secgroup_name)
        self._admin_float_net_id=getAdminFloatNetId(self._accountResource.get_adminNets(),self._readConfig.base.admin_float_net_name)
        self._test_image_id=getTestImageId(self._accountResource.get_images(),self._readConfig.base.test_image_name)

        self._zone_names = self._readConfig.base.zone_names.split('||')

        #判断需要测试的类型
        if self._readConfig.executeTest.is_stability_test_iperf.lower()=='true':
            self._loggers.stabilityIperfLogger.info('===开始初始化稳定性测试iperf资源===')
            self._initIperf()

        self._loggers.stabilityIperfLogger.info('将测试初始化资源写入到文件dbs/stabilityIperfTestAccountResource.dbs')
        FileTool.writeObjectIntoFile(self._accountResource,'dbs/stabilityIperfTestAccountResource.dbs')


    def _initIperf(self):
        """
        初始化iperf测试必须有的资源
        :return:
        """
        self._loggers.stabilityIperfLogger.info('初始化iperf测试的云主机规格')
        self._test_iperf_flavor_id=getFlavorId(self._accountResource.get_flavors(),self._readConfig.executeTest.stability_test_iperf_flavor)

        self._loggers.stabilityIperfLogger.info('初始化iperf测试的网络'+self._test_iperf_net1_name+'和'+self._test_iperf_net2_name)
        test_iperf_net1=Net()
        test_iperf_net2 = Net()
        test_iperf_net1.name=self._test_iperf_net1_name
        test_iperf_net1.cidr = self._test_iperf_subnet1_cidr
        test_iperf_net2.name=self._test_iperf_net2_name
        test_iperf_net2.cidr=self._test_iperf_subnet2_cidr
        try:
            test_iperf_net1.id=self._openstackClient.createNetwork(self._test_iperf_net1_name,self._test_iperf_subnet1_cidr)
            test_iperf_net2.id = self._openstackClient.createNetwork(self._test_iperf_net2_name, self._test_iperf_subnet2_cidr)
        except Exception,e:
            self._loggers.stabilityIperfLogger.error('初始化iperf测试的网络'+self._test_iperf_net1_name+'和'+self._test_iperf_net2_name+'失败!'+'\r\n'+e.message)
        self._test_iperf_net1_id=test_iperf_net1.id
        self._test_iperf_net2_id=test_iperf_net2.id
        self._accountResource.add_net(test_iperf_net1)
        self._accountResource.add_net(test_iperf_net2)

        self._loggers.stabilityIperfLogger.info('初始化一个路由器资源，创建名为' + self._router_name + '的路由')
        test_router=Router()
        test_router.name=StrTool.addUUID(self._router_name)
        try:
            test_router.id=self._openstackClient.createRouter(test_router.name,self._admin_float_net_id)
        except Exception,e:
            self._loggers.stabilityIperfLogger.error('创建路由器'+self._router_name+'失败!'+'\r\n'+e.message)
        self._router_id=test_router.id
        self._loggers.stabilityIperfLogger.info('将iperf网络' + self._test_iperf_net1_name + '绑定到路由器' + self._router_name)
        try:
            test_iperf_net1_subnet_id=self._openstackClient.getSubNetId(self._test_iperf_net1_id)
            self._openstackClient.addRouterInterface(self._router_id,test_iperf_net1_subnet_id)
            test_router.add_subnet_id(test_iperf_net1_subnet_id)
        except Exception,e:
            self._loggers.stabilityIperfLogger.error('将iperf网络' + self._test_iperf_net1_name + '绑定到路由器' + self._router_name+'失败!'+e.message)
        self._loggers.stabilityIperfLogger.info('将iperf网络' + self._test_iperf_net2_name + '绑定到路由器' + self._router_name)
        try:
            test_iperf_net2_subnet_id = self._openstackClient.getSubNetId(self._test_iperf_net2_id)
            self._openstackClient.addRouterInterface(self._router_id, test_iperf_net2_subnet_id)
            test_router.add_subnet_id(test_iperf_net2_subnet_id)
        except Exception,e:
            self._loggers.stabilityIperfLogger.error('将iperf网络' + self._test_iperf_net2_name + '绑定到路由器' + self._router_name+'失败!'+e.message)
        self._accountResource.add_router(test_router)

        # 获取可用域
        if len(self._zone_names) < 2:
            self._loggers.stabilityIperfLogger.error('可用域' + self._zone_names + '少于两个无法进行iperf测试')
            return

        for i in range(int(self._readConfig.executeTest.stability_test_iperf_group_num)):
            self._loggers.stabilityIperfLogger.info('初始化iperf测试的云主机')
            # 启动一组iperf测试云主机,不同网段
            self._loggers.stabilityIperfLogger.info('启动一组iperf测试的云主机,在不同网段')
            iperf_computePair=[]
            for j in range(2):
                #申请一个浮动ip
                self._loggers.stabilityIperfLogger.info('申请一个浮动ip')
                test_floatIp = FloatIp()
                try:
                    test_floatIp.ip = self._openstackClient.getFloatIp(self._admin_float_net_id)
                    test_floatIp.id = self._openstackClient.getFloatId(test_floatIp.ip)
                    self._loggers.stabilityIperfLogger.info('申请到一个浮动ip:' + test_floatIp.ip)
                except Exception,e:
                    self._loggers.stabilityIperfLogger.error('申请浮动ip失败!'+'\r\n'+e.message)
                self._accountResource.add_floatIp(test_floatIp)

                zone=None
                net_id=None
                tmp_testType = 'iperf_two_net'
                name=None
                #第一台
                if j==0:
                    self._loggers.stabilityIperfLogger.info('启动第一台云主机')
                    zone=self._zone_names[0]
                    net_id=self._test_iperf_net1_id
                    name=StrTool.addUUID('basebench_iperf_' + str(i)+'_'+str(j))
                #第二台
                elif j==1:
                    self._loggers.stabilityIperfLogger.info('启动第二台云主机')
                    zone=self._zone_names[1]
                    net_id=self._test_iperf_net2_id
                    name = StrTool.addUUID('basebench_iperf_' + str(i)+'_'+str(j))

                #创建云主机
                test_compute = Compute()
                test_compute.name=name
                test_compute.testType = tmp_testType
                self._loggers.stabilityIperfLogger.info('启动云主机' + test_compute.name)
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
                    self._loggers.stabilityIperfLogger.error('启动云主机'+test_compute.name+'失败!'+'\r\n'+e.message)
                #绑定浮动ip
                self._loggers.stabilityIperfLogger.info('为云主机' + test_compute.name + '绑定浮动ip:' + test_floatIp.ip)
                try:
                    is_add_succ=self._novaClient.addFloatForCompute(test_compute.id,test_floatIp.ip)
                    if is_add_succ:
                        test_compute.float_ip=test_floatIp.ip
                except Exception,e:
                    self._loggers.stabilityIperfLogger.error('为云主机' + test_compute.name + '绑定浮动ip:' + test_floatIp.ip+'失败!'+'\r\n'+e.message)
                iperf_computePair.append(test_compute)
                self._accountResource.add_compute(test_compute)
                #设置一组iperf云主机
            self._accountResource.add_iperfComputePair(iperf_computePair)

    def getStabilityIperfAccountResource(self):
        return self._accountResource


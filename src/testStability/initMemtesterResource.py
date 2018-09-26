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
import random

class InitMemtesterResource:
    def __init__(self):
        self._readConfig=ReadConfig()
        self._loggers=Loggers()

        self._os_tenant_name=self._readConfig.accounts.stability_memtester_os_tenant_name
        self._os_project_name=self._readConfig.accounts.stability_memtester_os_project_name
        self._os_username =self._readConfig.accounts.stability_memtester_os_username
        self._os_password=self._readConfig.accounts.stability_memtester_os_password

        self._init=Init(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password,self._loggers.stabilityMemtesterLogger)
        self._accountResource = self._init.initAccountResource()

        self._router_name='basebench_memtester_router'
        self._user_data_path='userdata/user_data'

        self._test_memtester_net_name='basebench_memtester_net'
        self._test_memtester_subnet_cidr='192.168.50.0/24'

        self._loggers.stabilityMemtesterLogger.info('===初始化稳定性测试基础资源[memtester账号]===')
        self._initResource()

    def _initResource(self):
        """
        公共资源初始化
        :return:
        """
        self._loggers.stabilityMemtesterLogger.info('初始化命令行客户端')
        self._openstackClient=OpenstackClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._novaClient=NovaClient(self._os_project_name,self._os_username,self._os_password)
        self._cinderClient=CinderClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)

        self._loggers.stabilityMemtesterLogger.info('初始化默认安全组、测试镜像、测试镜像')
        self._default_secgroup_id=getDefaultSecGroupId(self._accountResource.get_secgroups(),self._readConfig.base.default_secgroup_name)
        self._admin_float_net_id=getAdminFloatNetId(self._accountResource.get_adminNets(),self._readConfig.base.admin_float_net_name)
        self._test_image_id=getTestImageId(self._accountResource.get_images(),self._readConfig.base.test_image_name)

        self._zone_names = self._readConfig.base.zone_names.split('||')

        #判断是否进行memtester测试
        if self._readConfig.executeTest.is_stability_test_memtester.lower()=='true':
            self._loggers.stabilityMemtesterLogger.info('===开始初始化稳定性测试memtester资源===')
            self._initMemtester()

        self._loggers.stabilityMemtesterLogger.info('将测试初始化资源写入到文件dbs/stabilityMemtesterTestAccountResource.dbs')
        FileTool.writeObjectIntoFile(self._accountResource,'dbs/stabilityMemtesterTestAccountResource.dbs')

    def _initMemtester(self):
        """
        根据memtester所需要测试，创建云主机
        :return:
        """
        self._loggers.stabilityMemtesterLogger.info('初始化memtester测试的云主机规格')
        self._test_memtester_flavor_id = getFlavorId(self._accountResource.get_flavors(), self._readConfig.executeTest.stability_test_memtester_flavor)

        self._loggers.stabilityMemtesterLogger.info('初始化memtester网络资源，创建名为' + self._test_memtester_net_name + '的网络')
        test_memtester_net = Net()
        test_memtester_net.name = StrTool.addUUID(self._test_memtester_net_name)
        test_memtester_net.cidr = self._test_memtester_subnet_cidr
        try:
            test_memtester_net.id = self._openstackClient.createNetwork(test_memtester_net.name, test_memtester_net.cidr)
        except Exception,e:
            self._loggers.stabilityMemtesterLogger.error('创建网络'+test_memtester_net.name+'失败!'+'\r\n'+e.message)
        self._test_memtester_net_id = test_memtester_net.id
        self._accountResource.add_net(test_memtester_net)

        self._loggers.stabilityMemtesterLogger.info('初始化一个路由器资源，创建名为' + self._router_name + '的路由')
        test_router=Router()
        test_router.name=StrTool.addUUID(self._router_name)
        try:
            test_router.id=self._openstackClient.createRouter(test_router.name,self._admin_float_net_id)
        except Exception,e:
            self._loggers.stabilityMemtesterLogger.error('创建路由器'+test_router.name+'失败!'+'\r\n'+e.message)
        self._router_id=test_router.id
        self._loggers.stabilityMemtesterLogger.info('将memtester网络' + self._test_memtester_net_name + '绑定到路由器' + self._router_name)
        try:
            test_memtester_net_subnet_id = self._openstackClient.getSubNetId(self._test_memtester_net_id)
            self._openstackClient.addRouterInterface(self._router_id, test_memtester_net_subnet_id)
            test_router.add_subnet_id(test_memtester_net_subnet_id)
        except Exception,e:
            self._loggers.stabilityMemtesterLogger.error('将memtester网络' + self._test_memtester_net_name + '绑定到路由器' + self._router_name+'失败!'+'\r\n'+e.message)
        self._accountResource.add_router(test_router)

        self._loggers.stabilityMemtesterLogger.info('初始化memtester测试的云主机')
        for i in range(int(self._readConfig.executeTest.stability_test_memtester_num)):
            computeName = StrTool.addUUID('basebench_memtester'+str(i))
            testType = 'memtester'

            #申请一个浮动ip
            self._loggers.stabilityMemtesterLogger.info('申请一个浮动ip')
            test_floatIp=FloatIp()
            try:
                test_floatIp.ip = self._openstackClient.getFloatIp(self._admin_float_net_id)
                test_floatIp.id=self._openstackClient.getFloatId(test_floatIp.ip)
                self._loggers.stabilityMemtesterLogger.info('申请到一个浮动ip:' + test_floatIp.ip)
            except Exception,e:
                self._loggers.stabilityMemtesterLogger.error('申请浮动ip失败!'+'\r\n'+e.message)
            self._accountResource.add_floatIp(test_floatIp)

            #启动云主机
            test_compute = Compute()
            test_compute.name = computeName
            test_compute.testType=testType
            self._loggers.stabilityMemtesterLogger.info('启动云主机'+test_compute.name)
            try:
                test_compute.id=self._novaClient.bootCompute(computeName,
                                                             self._test_memtester_flavor_id,
                                                             self._test_image_id,
                                                             self._test_memtester_net_id,
                                                             self._default_secgroup_id,
                                                             random.choice(self._zone_names),
                                                             self._user_data_path)
            except Exception,e:
                self._loggers.stabilityMemtesterLogger.error('启动云主机'+test_compute.name+'失败!'+'\r\n'+e.message)

            #绑定浮动ip
            self._loggers.stabilityMemtesterLogger.info('为云主机' + test_compute.name + '绑定浮动ip:' + test_floatIp.ip)
            try:
                is_add_succ=self._novaClient.addFloatForCompute(test_compute.id,test_floatIp.ip)
                if is_add_succ:
                   test_compute.float_ip=test_floatIp.ip
            except Exception,e:
                self._loggers.stabilityMemtesterLogger.error('为云主机'+test_compute.name+'绑定浮动ip:'+test_floatIp.ip+'失败!'+'\r\n'+e.message)
            self._accountResource.add_memtesterCompute(test_compute)
            self._accountResource.add_compute(test_compute)

    def getStabilityMemtesterAccountResource(self):
        return self._accountResource


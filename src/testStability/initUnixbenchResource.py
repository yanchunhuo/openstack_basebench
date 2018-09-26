#!-*- coding:utf8 -*-
from src.accountResourceTools import getDefaultSecGroupId
from src.accountResourceTools import getAdminFloatNetId
from src.accountResourceTools import getTestImageId
from src.accountResourceTools import getFlavorId
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
import random

class InitUnixbenchResource:
    def __init__(self):
        self._readConfig = ReadConfig()
        self._loggers = Loggers()

        self._os_tenant_name=self._readConfig.accounts.stability_unixbench_os_tenant_name
        self._os_project_name=self._readConfig.accounts.stability_unixbench_os_project_name
        self._os_username =self._readConfig.accounts.stability_unixbench_os_username
        self._os_password=self._readConfig.accounts.stability_unixbench_os_password

        self._init=Init(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password,self._loggers.stabilityUnixbenchLogger)
        self._accountResource = self._init.initAccountResource()

        self._router_name='basebench_unixbench_router'
        self._user_data_path='userdata/user_data'

        self._test_unixbench_net_name='basebench_unixbench_net'
        self._test_unixbench_subnet_cidr='192.168.30.0/24'

        self._loggers.stabilityUnixbenchLogger.info('===初始化稳定性测试基础资源[unixbench账号]===')
        self._initResource()

    def _initResource(self):
        """
        公共资源初始化
        :return:
        """
        self._loggers.stabilityUnixbenchLogger.info('初始化命令行客户端')
        self._openstackClient=OpenstackClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._novaClient=NovaClient(self._os_project_name,self._os_username,self._os_password)
        self._cinderClient=CinderClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)

        self._loggers.stabilityUnixbenchLogger.info('初始化默认安全组、测试镜像、测试镜像')
        self._default_secgroup_id=getDefaultSecGroupId(self._accountResource.get_secgroups(),self._readConfig.base.default_secgroup_name)
        self._admin_float_net_id=getAdminFloatNetId(self._accountResource.get_adminNets(),self._readConfig.base.admin_float_net_name)
        self._test_image_id=getTestImageId(self._accountResource.get_images(),self._readConfig.base.test_image_name)

        self._zone_names = self._readConfig.base.zone_names.split('||')

        #判断是否进行unixbench测试
        if self._readConfig.executeTest.is_stability_test_unixbench.lower()=='true':
            self._loggers.stabilityUnixbenchLogger.info('===开始初始化稳定性测试unixbench资源===')
            self._initUnixbench()

        self._loggers.stabilityUnixbenchLogger.info('将测试初始化资源写入到文件dbs/stabilityUnixbenchTestAccountResource.dbs')
        FileTool.writeObjectIntoFile(self._accountResource,'dbs/stabilityUnixbenchTestAccountResource.dbs')

    def _initUnixbench(self):
        """
        根据unixbench所需要测试，创建云主机
        :return:
        """
        self._loggers.stabilityUnixbenchLogger.info('初始化unixbench测试的云主机规格')
        self._test_unixbench_flavor_id = getFlavorId(self._accountResource.get_flavors(), self._readConfig.executeTest.stability_test_unixbench_flavor)

        self._loggers.stabilityUnixbenchLogger.info('初始化unixbench网络资源，创建名为' + self._test_unixbench_net_name + '的网络')
        test_unixbench_net = Net()
        test_unixbench_net.name = StrTool.addUUID(self._test_unixbench_net_name)
        test_unixbench_net.cidr = self._test_unixbench_subnet_cidr
        try:
            test_unixbench_net.id = self._openstackClient.createNetwork(test_unixbench_net.name, test_unixbench_net.cidr)
            self._test_unixbench_net_id = test_unixbench_net.id
        except Exception,e:
            self._loggers.stabilityUnixbenchLogger.error('创建unixbench所需网络' + self._test_unixbench_net_name + '失败!'+'\r\n'+e.message)

        self._loggers.stabilityUnixbenchLogger.info('初始化一个路由器资源，创建名为' + self._router_name + '的路由')
        test_router = Router()
        test_router.name = StrTool.addUUID(self._router_name)
        try:
            test_router.id = self._openstackClient.createRouter(test_router.name, self._admin_float_net_id)
            self._router_id = test_router.id
        except Exception, e:
            self._loggers.stabilityUnixbenchLogger.error('创建路由器' + self._router_name + '失败!' + '\r\n' + e.message)
        self._loggers.stabilityUnixbenchLogger.info('将unixbench网络' + self._test_unixbench_net_name + '绑定到路由器' + self._router_name)
        try:
            test_unixbench_net_subnet_id = self._openstackClient.getSubNetId(self._test_unixbench_net_id)
            self._openstackClient.addRouterInterface(self._router_id, test_unixbench_net_subnet_id)
            test_router.add_subnet_id(test_unixbench_net_subnet_id)
            test_unixbench_net.add_subnet_id(test_unixbench_net_subnet_id)
        except Exception, e:
            self._loggers.stabilityUnixbenchLogger.error('将unixbench网络' + self._test_unixbench_net_name + '绑定到路由器' + self._router_name +'失败!'+'\r\n'+e.message)
        self._accountResource.add_net(test_unixbench_net)
        self._accountResource.add_router(test_router)

        self._loggers.stabilityUnixbenchLogger.info('初始化unixbench测试的云主机')
        for i in range(int(self._readConfig.executeTest.stability_test_unixbench_num)):
            computeName = StrTool.addUUID('basebench_unixbench'+str(i))
            testType = 'unixbench'

            #申请一个浮动ip
            self._loggers.stabilityUnixbenchLogger.info('申请一个浮动ip')
            test_floatIp=FloatIp()
            try:
                test_floatIp.ip = self._openstackClient.getFloatIp(self._admin_float_net_id)
                test_floatIp.id = self._openstackClient.getFloatId(test_floatIp.ip)
            except Exception,e:
                self._loggers.stabilityUnixbenchLogger.error('申请浮动ip失败!'+'\r\n'+e.message)
            self._accountResource.add_floatIp(test_floatIp)

            #启动云主机
            test_compute = Compute()
            test_compute.name = computeName
            test_compute.testType=testType
            try:
                test_compute.id=self._novaClient.bootCompute(test_compute.name,
                                                             self._test_unixbench_flavor_id,
                                                             self._test_image_id,
                                                             self._test_unixbench_net_id,
                                                             self._default_secgroup_id,
                                                             random.choice(self._zone_names),
                                                             self._user_data_path)
            except Exception, e:
                self._loggers.stabilityUnixbenchLogger.error('启动云主机'+test_compute.name+'失败!'+'\r\n'+e.message)
            #绑定浮动ip
            self._loggers.stabilityUnixbenchLogger.info('为云主机' + test_compute.name + '绑定浮动ip:' + test_floatIp.ip)
            try:
                is_add_succ=self._novaClient.addFloatForCompute(test_compute.id,test_floatIp.ip)
                if is_add_succ:
                   test_compute.float_ip=test_floatIp.ip
            except Exception, e:
                self._loggers.stabilityUnixbenchLogger.error('为云主机' + test_compute.name + '绑定浮动ip:' + test_floatIp.ip + '失败!' + '\r\n' + e.message)
            self._accountResource.add_unixbenchCompute(test_compute)
            self._accountResource.add_compute(test_compute)

    def getStabilityUnixbenchAccountResource(self):
        return self._accountResource


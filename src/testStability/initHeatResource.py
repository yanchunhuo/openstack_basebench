#!-*- coding:utf8 -*-
from src.clients.openstackClient import OpenstackClient
from src.clients.cinderClient import CinderClient
from src.clients.novaClient import NovaClient
from src.clients.heatClient import HeatClient
from src.common.fileTool import FileTool
from src.loggers import Loggers
from src.readConfig import ReadConfig
from src.common.strTool import StrTool
from src.pojo.Heat import Heat
from src.pojo.NET import Net
from src.pojo.Router import Router
from src.init import Init
from src.accountResourceTools import getDefaultSecGroupId
from src.accountResourceTools import getAdminFloatNetId
from src.accountResourceTools import getTestImageId
from src.accountResourceTools import getFlavorId

class InitHeatResource:
    def __init__(self):
        self._readConfig=ReadConfig()
        self._loggers=Loggers()

        self._os_tenant_name=self._readConfig.accounts.stability_heat_os_tenant_name
        self._os_project_name=self._readConfig.accounts.stability_heat_os_project_name
        self._os_username =self._readConfig.accounts.stability_heat_os_username
        self._os_password=self._readConfig.accounts.stability_heat_os_password

        self._init=Init(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password,self._loggers.stabilityHeatLogger)
        self._accountResource = self._init.initAccountResource()

        self._router_name='basebench_heat_router'
        self._user_data_path='userdata/user_data'

        self._test_heat_net_name='basebench_heat_net'
        self._test_heat_subnet_cidr='192.168.50.0/24'

        self._loggers.stabilityHeatLogger.info('===初始化稳定性测试基础资源[heat账号]===')
        self._initResource()

    def _initResource(self):
        """
        公共资源初始化
        :return:
        """
        self._loggers.stabilityHeatLogger.info('初始化命令行客户端')
        self._openstackClient=OpenstackClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._novaClient=NovaClient(self._os_project_name,self._os_username,self._os_password)
        self._cinderClient=CinderClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._heatClient = HeatClient(self._os_tenant_name, self._os_project_name, self._os_username,self._os_password)

        self._loggers.stabilityHeatLogger.info('初始化默认安全组、测试镜像、测试镜像')
        self._default_secgroup_id=getDefaultSecGroupId(self._accountResource.get_secgroups(),self._readConfig.base.default_secgroup_name)
        self._admin_float_net_id=getAdminFloatNetId(self._accountResource.get_adminNets(),self._readConfig.base.admin_float_net_name)
        self._test_image_id=getTestImageId(self._accountResource.get_images(),self._readConfig.base.test_image_name)

        #判断是否进行memtester测试
        if self._readConfig.executeTest.is_stability_test_heat.lower()=='true':
            self._loggers.stabilityHeatLogger.info('===开始初始化稳定性测试heat资源===')
            self._initHeat()

            self._loggers.stabilityHeatLogger.info('将测试初始化资源写入到文件dbs/stabilityHeatTestAccountResource.dbs')
        FileTool.writeObjectIntoFile(self._accountResource,'dbs/stabilityHeatTestAccountResource.dbs')

    def _initHeat(self):
        """
        根据heat所需要测试，创建云主机
        :return:
        """
        self._loggers.stabilityHeatLogger.info('初始化heat测试的云主机规格')
        self._test_heat_flavor_id = getFlavorId(self._accountResource.get_flavors(), self._readConfig.executeTest.stability_test_heat_flavor)
        self._test_heat_flavor_name = getFlavorId(self._accountResource.get_flavors(), self._readConfig.executeTest.stability_test_heat_flavor)

        self._loggers.stabilityHeatLogger.info('初始化heat网络资源，创建名为' + self._test_heat_net_name + '的网络')
        test_heat_net = Net()
        test_heat_net.name = StrTool.addUUID(self._test_heat_net_name)
        test_heat_net.cidr = self._test_heat_subnet_cidr
        try:
            test_heat_net.id = self._openstackClient.createNetwork(test_heat_net.name, test_heat_net.cidr)
        except Exception,e:
            self._loggers.stabilityHeatLogger.error('初始化网络'+self._router_name+'失败!'+'\r\n'+e.message)
        self._test_heat_net_id = test_heat_net.id
        self._accountResource.add_net(test_heat_net)

        self._loggers.stabilityHeatLogger.info('初始化一个路由器资源，创建名为' + self._router_name + '的路由')
        test_router=Router()
        test_router.name=StrTool.addUUID(self._router_name)
        try:
            test_router.id = self._openstackClient.createRouter(test_router.name, self._admin_float_net_id)
        except Exception,e:
            self._loggers.stabilityHeatLogger.error('创建路由器'+self._router_name+'失败!'+'\r\n'+e.message)
        self._router_id=test_router.id
        self._loggers.stabilityHeatLogger.info('将heat网络' + self._test_heat_net_name + '绑定到路由器' + self._router_name)
        try:
            test_heat_net_subnet_id = self._openstackClient.getSubNetId(self._test_heat_net_id)
            self._openstackClient.addRouterInterface(self._router_id, test_heat_net_subnet_id)
            test_router.add_subnet_id(test_heat_net_subnet_id)
        except Exception, e:
            self._loggers.stabilityHeatLogger.error('将heat网络' + self._test_heat_net_name + '绑定到路由器' + self._router_name + '失败!' + '\r\n' + e.message)
        self._accountResource.add_router(test_router)

        # 初始化heat必须有的资源
        self._password = '123456..'
        self._max_computes = '5'
        self._min_computes = '3'
        self._alarm_type = 'cpu_util'
        self._max_alarmvalue = '90'
        self._min_alarmvalue = '45'
        self._heat_templatepath = 'heat_template/heat_new.yaml'
        for i in range(int(self._readConfig.executeTest.stability_test_heat_group_num)):
            heatName = StrTool.addUUID('basebench_heat'+str(i))
            testType = 'heat'
            #启动heat
            test_heat = Heat()
            test_heat.name = heatName
            test_heat.testType=testType
            self._loggers.stabilityHeatLogger.info('创建一个伸缩组名为'+ test_heat.name)
            try:
                test_heat.id=self._heatClient.creatHeat(self._test_heat_net_id,
                                                      self._test_heat_subnet_cidr,
                                                      self._test_image_id,
                                                      self._readConfig.base.test_image_name,
                                                      self._test_heat_flavor_id,
                                                      self._test_heat_flavor_name,
                                                      self._password,
                                                      self._default_secgroup_id,
                                                      self._max_computes,
                                                      self._min_computes,
                                                      self._alarm_type,
                                                      self._max_alarmvalue,
                                                      self._min_alarmvalue,
                                                      self._heat_templatepath,
                                                      heatName)
            except Exception, e:
                self._loggers.stabilityHeatLogger.info('创建一个伸缩组名为' + test_heat.name + '失败!' + '\r\n' + e.message)
            self._accountResource.add_heatCompute(test_heat)

    def getStabilityheatAccountResource(self):
        return self._accountResource


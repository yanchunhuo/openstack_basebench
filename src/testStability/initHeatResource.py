#!-*- coding:utf8 -*-
from src.clients.neutronClient import NeutronClient
from src.clients.cinderClient import CinderClient
from src.clients.novaClient import NovaClient
from src.clients.heatClient import HeatClient
from config.config import DEFAULT_SECGROUP_NAME
from config.config import TEST_IMAGE_NAME
from config.config import ADMIN_FLOAT_NET_NAME
from config.config import IS_STABILITY_TEST_HEAT
from config.config import STABILITY_HEAT_ACCOUNT_OS_TENANT_NAME
from config.config import STABILITY_HEAT_ACCOUNT_OS_PROJECT_NAME
from config.config import STABILITY_HEAT_ACCOUNT_OS_USERNAME
from config.config import STABILITY_HEAT_ACCOUNT_OS_PASSWORD
from config.config import STABILITY_TEST_HEAT_GROUP_NUM
from config.config import STABILITY_TEST_HEAT_FLAVOR
from src.common import addUUID
from src.common import writeObjectIntoFile
from src.pojo.Heat import Heat
from src.pojo.NET import Net
from src.pojo.Router import Router
from src.logger import stabilityHeatLogger
from src.init import Init
from src.accountResourceTools import getDefaultSecGroupId
from src.accountResourceTools import getAdminFloatNetId
from src.accountResourceTools import getTestImageId
from src.accountResourceTools import getFlavorId

class InitHeatResource():
    def __init__(self):
        self._os_tenant_name=STABILITY_HEAT_ACCOUNT_OS_TENANT_NAME
        self._os_project_name=STABILITY_HEAT_ACCOUNT_OS_PROJECT_NAME
        self._os_username =STABILITY_HEAT_ACCOUNT_OS_USERNAME
        self._os_password=STABILITY_HEAT_ACCOUNT_OS_PASSWORD

        self._init=Init(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password,stabilityHeatLogger)
        self._accountResource = self._init.initAccountResource()

        self._router_name='heat_router'
        self._user_data_path='userdata/user_data'

        self._test_heat_net_name='heat_net'
        self._test_heat_subnet_cidr='192.168.50.0/24'

        stabilityHeatLogger.info('===初始化稳定性测试基础资源[heat账号]===')
        self._initResource()

    def _initResource(self):
        """
        公共资源初始化
        :return:
        """
        stabilityHeatLogger.info('初始化命令行客户端')
        self._neutronClient=NeutronClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._novaClient=NovaClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._cinderClient=CinderClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._heatClient = HeatClient(self._os_tenant_name, self._os_project_name, self._os_username,self._os_password)

        stabilityHeatLogger.info('初始化默认安全组、测试镜像、测试镜像')
        self._default_secgroup_id=getDefaultSecGroupId(self._accountResource.get_secgroups(),DEFAULT_SECGROUP_NAME)
        self._admin_float_net_id=getAdminFloatNetId(self._accountResource.get_adminNets(),ADMIN_FLOAT_NET_NAME)
        self._test_image_id=getTestImageId(self._accountResource.get_images(),TEST_IMAGE_NAME)

        stabilityHeatLogger.info('初始化一个路由器资源，创建名为' + self._router_name + '的路由')
        test_router=Router()
        test_router.name=addUUID(self._router_name)
        try:
            test_router.id = self._neutronClient.createRouter(test_router.name, self._admin_float_net_id)
        except Exception,e:
            stabilityHeatLogger.error('创建路由器'+self._router_name+'失败!'+'\r\n'+e.message)
        self._router_id=test_router.id
        self._accountResource.add_router(test_router)

        #判断是否进行memtester测试
        if IS_STABILITY_TEST_HEAT:
            stabilityHeatLogger.info('===开始初始化稳定性测试heat资源===')
            self._initHeat()

            stabilityHeatLogger.info('将测试初始化资源写入到文件dbs/stabilityHeatTestAccountResource.dbs')
        writeObjectIntoFile(self._accountResource,'dbs/stabilityHeatTestAccountResource.dbs')

    def _initHeat(self):
        """
        根据heat所需要测试，创建云主机
        :return:
        """
        stabilityHeatLogger.info('初始化heat测试的云主机规格')
        self._test_heat_flavor_id = getFlavorId(self._accountResource.get_flavors(), STABILITY_TEST_HEAT_FLAVOR)
        self._test_heat_flavor_name = getFlavorId(self._accountResource.get_flavors(), STABILITY_TEST_HEAT_FLAVOR)

        stabilityHeatLogger.info('初始化heat网络资源，创建名为' + self._test_heat_net_name + '的网络')
        test_heat_net = Net()
        test_heat_net.name = addUUID(self._test_heat_net_name)
        test_heat_net.cidr = self._test_heat_subnet_cidr
        try:
            test_heat_net.id = self._neutronClient.createNetwork(test_heat_net.name, test_heat_net.cidr)
        except Exception,e:
            stabilityHeatLogger.error('初始化网络'+self._router_name+'失败!'+'\r\n'+e.message)
        self._test_heat_net_id = test_heat_net.id
        self._accountResource.add_net(test_heat_net)

        stabilityHeatLogger.info('将heat网络' + self._test_heat_net_name + '绑定到路由器' + self._router_name)
        try:
            test_heat_net_subnet_id = self._neutronClient.getSubNetId(self._test_heat_net_id)
        except Exception, e:
            stabilityHeatLogger.error('将heat网络' + self._test_heat_net_name + '绑定到路由器' + self._router_name + '失败!' + '\r\n' + e.message)
        self._neutronClient.addRouterInterface(self._router_id, test_heat_net_subnet_id)

        # 初始化heat必须有的资源
        self._password = '123456..'
        self._max_computes = '5'
        self._min_computes = '3'
        self._alarm_type = 'cpu_util'
        self._max_alarmvalue = '90'
        self._min_alarmvalue = '45'
        self._heat_templatepath = '/root/lmy/testEnv/basebench/heat_template/heat_new.yaml'


        for i in range(STABILITY_TEST_HEAT_GROUP_NUM):
            heatName = addUUID('heat'+str(i))
            testType = 'heat'




            #启动heat
            test_heat = Heat()
            test_heat.name = heatName
            test_heat.testType=testType
            stabilityHeatLogger.info('创建一个伸缩组名为'+ test_heat.name)
            try:
                test_heat.id=self._heatClient.creatHeat(self._test_heat_net_id,
                                                      self._test_heat_subnet_cidr,
                                                      self._test_image_id,
                                                      TEST_IMAGE_NAME,
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
                stabilityHeatLogger.info('创建一个伸缩组名为' + test_heat.name + '失败!' + '\r\n' + e.message)


            self._accountResource.add_heatCompute(test_heat)


    def getStabilityheatAccountResource(self):
        return self._accountResource


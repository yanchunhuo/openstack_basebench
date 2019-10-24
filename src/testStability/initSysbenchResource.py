#!-*- coding:utf8 -*-
from src.accountResourceTools import getDefaultSecGroupId
from src.accountResourceTools import getAdminFloatNetId
from src.accountResourceTools import getTestImageId
from src.accountResourceTools import getFlavorId
from src.clients.openstackClient import OpenstackClient
from src.clients.cinderClient import CinderClient
from src.clients.novaClient import NovaClient
from src.clients.troveClient import TroveClient
from src.common.fileTool import FileTool
from src.loggers import Loggers
from src.readConfig import ReadConfig
from src.common.strTool import StrTool
from src.pojo.Compute import Compute
from src.pojo.Trove import Trove
from src.pojo.NET import Net
from src.pojo.Router import Router
from src.pojo.FloatIp import FloatIp
from src.init import Init

import random

class InitSysbenchResource:
    def __init__(self):
        self._readConfig = ReadConfig()
        self._loggers = Loggers()

        self._os_tenant_name=self._readConfig.accounts.stability_sysbench_os_tenant_name
        self._os_project_name=self._readConfig.accounts.stability_sysbench_os_project_name
        self._os_username =self._readConfig.accounts.stability_sysbench_os_username
        self._os_password = self._readConfig.accounts.stability_sysbench_os_password


        self._init=Init(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password,self._loggers.stabilitySysbenchLogger)
        self._accountResource = self._init.initAccountResource()

        self._router_name = 'basebench_sysbench_router'
        self._user_data_path='userdata/user_data'

        self._test_sysbench_net_name = 'basebench_sysbench'
        self._test_sysbench_subnet_cidr = '192.168.70.0/24'

        self._loggers.stabilitySysbenchLogger.info('===初始化稳定性测试基础资源[sysbench账号]===')
        self._initResource()

    def _initResource(self):
        """
        公共资源初始化
        :return:
        """
        self._loggers.stabilitySysbenchLogger.info('初始化命令行客户端')
        self._openstackClient=OpenstackClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._novaClient=NovaClient(self._os_project_name,self._os_username,self._os_password)
        self._cinderClient=CinderClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._troveClient = TroveClient(self._os_tenant_name, self._os_project_name, self._os_username,self._os_password)

        self._loggers.stabilitySysbenchLogger.info('初始化默认安全组、测试浮动ip、测试云主机镜像')
        self._default_secgroup_id=getDefaultSecGroupId(self._accountResource.get_secgroups(),self._readConfig.base.default_secgroup_name)
        self._admin_float_net_id=getAdminFloatNetId(self._accountResource.get_adminNets(),self._readConfig.base.admin_float_net_name)
        self._test_image_id=getTestImageId(self._accountResource.get_images(),self._readConfig.base.test_image_name)

        self._zone_names = self._readConfig.base.zone_names.split('||')

        #判断需要测试的类型
        if self._readConfig.executeTest.is_stability_test_memtester.lower()=='true':
            self._loggers.stabilitySysbenchLogger.info('===开始初始化稳定性测试sysbench资源===')
            self._initSysbench()

        self._loggers.stabilitySysbenchLogger.info('将测试初始化资源写入到文件dbs/stabilitySysbenchTestAccountResource.dbs')
        FileTool.writeObjectIntoFile(self._accountResource,'dbs/stabilitySysbenchTestAccountResource.dbs')


    def _initSysbench(self):
        """
        初始化Sysbench测试必须有的资源
        :return:
        """
        self._loggers.stabilitySysbenchLogger.info('初始化Sysbench测试的云主机规格')
        self._test_sysbench_flavor_id=getFlavorId(self._accountResource.get_flavors(),self._readConfig.executeTest.stability_test_sysbench_flavor)

        self._loggers.stabilitySysbenchLogger.info('初始化Sysbench测试的网络'+self._test_sysbench_net_name)
        test_sysbench_net=Net()
        test_sysbench_net.name=self._test_sysbench_net_name
        test_sysbench_net.cidr = self._test_sysbench_subnet_cidr
        try:
            test_sysbench_net.id=self._openstackClient.createNetwork(self._test_sysbench_net_name,self._test_sysbench_subnet_cidr)
        except Exception as e:
            self._loggers.stabilitySysbenchLogger.info('创建网络' + self._test_sysbench_net_name + '失败'+'\r\n'+e.args.__str__())
        self._test_sysbench_net_id=test_sysbench_net.id

        self._loggers.stabilitySysbenchLogger.info('初始化一个路由器资源，创建名为' + self._router_name + '的路由')
        test_router = Router()
        test_router.name = StrTool.addUUID(self._router_name)
        try:
            test_router.id = self._openstackClient.createRouter(test_router.name, self._admin_float_net_id)
        except Exception as e:
            self._loggers.stabilitySysbenchLogger.info('创建路由器' + self._router_name + '失败' + '\r\n' + e.args.__str__())
        self._router_id = test_router.id
        self._loggers.stabilitySysbenchLogger.info('将Sysbench网络' + self._test_sysbench_net_name + '绑定到路由器' + self._router_name)
        try:
            test_sysbench_net_subnet_id=self._openstackClient.getSubNetId(self._test_sysbench_net_id)
            self._openstackClient.addRouterInterface(self._router_id, test_sysbench_net_subnet_id)
            test_router.add_subnet_id(test_sysbench_net_subnet_id)
            test_sysbench_net.add_subnet_id(test_sysbench_net_subnet_id)
        except Exception as e:
            self._loggers.stabilitySysbenchLogger.info('将Sysbench网络' + self._test_sysbench_net_name + '绑定到路由器' + self._router_name+ '失败'+'\r\n'+e.args.__str__())
        self._accountResource.add_net(test_sysbench_net)
        self._accountResource.add_router(test_router)

        #初始化trove必须有的资源
        self._trove_volume_size = '100'
        self._database_name = 'sbtest'
        self._user_name = 'test'
        self._user_password = '123456..'
        self._datastore_name = 'mysql'
        self._datastore_version_name = '5.6'

        for i in range(int(self._readConfig.executeTest.stability_test_sysbench_group_num)):
            self._loggers.stabilitySysbenchLogger.info('初始化Sysbench测试的云主机')
            # 启动一组Sysbench测试,同网段
            sysbench_computePair=[]

            computeName = StrTool.addUUID('basebench_sysbench' + str(i))
            testType = 'sysbench'

            #申请一个浮动ip
            test_floatIp = FloatIp()
            try:
                test_floatIp.ip = self._openstackClient.getFloatIp(self._admin_float_net_id)
                test_floatIp.id = self._openstackClient.getFloatId(test_floatIp.ip)
                self._loggers.stabilitySysbenchLogger.info('申请到一个浮动ip:' + test_floatIp.ip)
            except Exception as e:
                self._loggers.stabilitySysbenchLogger.info('申请浮动ip失败:'+'\r\n'+e.args.__str__())

            self._accountResource.add_floatIp(test_floatIp)


            #启动云主机
            test_compute = Compute()
            test_compute.name = computeName
            test_compute.testType=testType
            self._loggers.stabilitySysbenchLogger.info('启动云主机'+test_compute.name)
            try:
                test_compute.id=self._novaClient.bootCompute(computeName,
                                                         self._test_sysbench_flavor_id,
                                                         self._test_image_id,
                                                         self._test_sysbench_net_id,
                                                         self._default_secgroup_id,
                                                         random.choice(self._zone_names),
                                                         self._user_data_path)
            except Exception as e:
                self._loggers.stabilitySysbenchLogger.info('启动云主机' + test_compute.name + '失败'+'\r\n'+e.args.__str__())

            #绑定浮动ip
            self._loggers.stabilitySysbenchLogger.info('为云主机' + test_compute.name + '绑定浮动ip:' + test_floatIp.ip)
            try:
                is_add_succ=self._novaClient.addFloatForCompute(test_compute.id,test_floatIp.ip)
                if is_add_succ:
                    test_compute.float_ip = test_floatIp.ip
            except Exception as e:
                self._loggers.stabilitySysbenchLogger.info('为云主机' + test_compute.name + '绑定浮动ip:' + test_floatIp.ip + '失败'+'\r\n'+e.args.__str__())

            #创建数据库实例
            troveName = StrTool.addUUID('trove' + str(i))
            test_trove = Trove()
            test_trove.name = troveName
            self._loggers.stabilitySysbenchLogger.info('创建一台数据库实例' + test_trove.name)
            try:
                test_trove.id = self._troveClient.createtrove(test_trove.name,
                                                               self._test_sysbench_flavor_id,
                                                               self._trove_volume_size,
                                                               self._database_name,
                                                               self._user_name,
                                                               self._user_password,
                                                               self._test_sysbench_net_id,
                                                               random.choice(self._zone_names),
                                                               self._datastore_name,
                                                               self._datastore_version_name)
            except Exception as e:
                self._loggers.stabilitySysbenchLogger.info('创建一台数据库实例' + test_trove.name + '失败'+'\r\n'+e.args.__str__())

            test_trove.ip = self._novaClient.getComputeIp(test_trove.name)

            sysbench_computePair.append(test_compute)
            self._accountResource.add_compute(test_compute)
            sysbench_computePair.append(test_trove)
            #self._accountResource.add_compute(test_trove)
            #设置一组iperf云主机
            self._accountResource.add_sysbenchComputePair(sysbench_computePair)

    def getStabilitySysbenchAccountResource(self):
        return self._accountResource


#!-*- coding:utf8 -*-
from src.clients.neutronClient import NeutronClient
from src.clients.cinderClient import CinderClient
from src.clients.novaClient import NovaClient
from src.clients.troveClient import TroveClient
from config.config import DEFAULT_SECGROUP_NAME
from config.config import TEST_IMAGE_NAME
from config.config import ADMIN_FLOAT_NET_NAME
from config.config import ZONE_NAMES
from config.config import IS_STABILITY_TEST_SYSBENCH
from config.config import FLOAT_IP_QOS
from config.config import STABILITY_SYSBENCH_ACCOUNT_OS_TENANT_NAME
from config.config import STABILITY_SYSBENCH_ACCOUNT_OS_PROJECT_NAME
from config.config import STABILITY_SYSBENCH_ACCOUNT_OS_USERNAME
from config.config import STABILITY_SYSBENCH_ACCOUNT_OS_PASSWORD
from config.config import STABILITY_TEST_SYSBENCH_FLAVOR
from config.config import STABILITY_TEST_SYSBENCH_GROUP_NUM
from src.common import addUUID
from src.common import writeObjectIntoFile
from src.pojo.Compute import Compute
from src.pojo.Trove import Trove
from src.pojo.NET import Net
from src.pojo.Router import Router
from src.pojo.FloatIp import FloatIp
from src.logger import stabilitySysbenchLogger
from src.init import Init
from src.accountResourceTools import getDefaultSecGroupId
from src.accountResourceTools import getAdminFloatNetId
from src.accountResourceTools import getTestImageId
from src.accountResourceTools import getFlavorId
import random

class InitSysbenchResource():
    def __init__(self):
        self._os_tenant_name=STABILITY_SYSBENCH_ACCOUNT_OS_TENANT_NAME
        self._os_project_name=STABILITY_SYSBENCH_ACCOUNT_OS_PROJECT_NAME
        self._os_username =STABILITY_SYSBENCH_ACCOUNT_OS_USERNAME
        self._os_password=STABILITY_SYSBENCH_ACCOUNT_OS_PASSWORD


        self._init=Init(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password,stabilitySysbenchLogger)
        self._accountResource = self._init.initAccountResource()

        self._router_name = 'sysbench_router'
        self._user_data_path='userdata/user_data'

        self._test_sysbench_net_name = 'sysbench'
        self._test_sysbench_subnet_cidr = '192.168.70.0/24'

        stabilitySysbenchLogger.info('===初始化稳定性测试基础资源[sysbench账号]===')
        self._initResource()

    def _initResource(self):
        """
        公共资源初始化
        :return:
        """
        stabilitySysbenchLogger.info('初始化命令行客户端')
        self._neutronClient=NeutronClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._novaClient=NovaClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._cinderClient=CinderClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._troveClient = TroveClient(self._os_tenant_name, self._os_project_name, self._os_username,self._os_password)

        stabilitySysbenchLogger.info('初始化默认安全组、测试浮动ip、测试云主机镜像')
        self._default_secgroup_id=getDefaultSecGroupId(self._accountResource.get_secgroups(),DEFAULT_SECGROUP_NAME)
        self._admin_float_net_id=getAdminFloatNetId(self._accountResource.get_adminNets(),ADMIN_FLOAT_NET_NAME)
        self._test_image_id=getTestImageId(self._accountResource.get_images(),TEST_IMAGE_NAME)

        stabilitySysbenchLogger.info('初始化一个路由器资源，创建名为' + self._router_name + '的路由')
        test_router=Router()
        test_router.name=addUUID(self._router_name)
        try:
            test_router.id=self._neutronClient.createRouter(test_router.name,self._admin_float_net_id)
        except Exception, e:
            stabilitySysbenchLogger.info('创建路由器' + self._router_name + '失败'+'\r\n'+e.message)
        self._router_id=test_router.id
        self._accountResource.add_router(test_router)

        #判断需要测试的类型
        if IS_STABILITY_TEST_SYSBENCH:
            stabilitySysbenchLogger.info('===开始初始化稳定性测试sysbench资源===')
            self._initSysbench()

        stabilitySysbenchLogger.info('将测试初始化资源写入到文件dbs/stabilitySysbenchTestAccountResource.dbs')
        writeObjectIntoFile(self._accountResource,'dbs/stabilitySysbenchTestAccountResource.dbs')


    def _initSysbench(self):
        """
        初始化Sysbench测试必须有的资源
        :return:
        """
        stabilitySysbenchLogger.info('初始化Sysbench测试的云主机规格')
        self._test_sysbench_flavor_id=getFlavorId(self._accountResource.get_flavors(),STABILITY_TEST_SYSBENCH_FLAVOR)

        stabilitySysbenchLogger.info('初始化Sysbench测试的网络'+self._test_sysbench_net_name)
        test_sysbench_net=Net()
        test_sysbench_net.name=self._test_sysbench_net_name
        test_sysbench_net.cidr = self._test_sysbench_subnet_cidr
        try:
            test_sysbench_net.id=self._neutronClient.createNetwork(self._test_sysbench_net_name,self._test_sysbench_subnet_cidr)
        except Exception, e:
            stabilitySysbenchLogger.info('创建网络' + self._test_sysbench_net_name + '失败'+'\r\n'+e.message)

        self._test_sysbench_net_id=test_sysbench_net.id
        self._accountResource.add_net(test_sysbench_net)

        stabilitySysbenchLogger.info('将Sysbench网络' + self._test_sysbench_net_name + '绑定到路由器' + self._router_name)
        try:
            test_sysbench_net_subnet_id=self._neutronClient.getSubNetId(self._test_sysbench_net_id)
        except Exception, e:
            stabilitySysbenchLogger.info('将Sysbench网络' + self._test_sysbench_net_name + '绑定到路由器' + self._router_name+ '失败'+'\r\n'+e.message)
        self._neutronClient.addRouterInterface(self._router_id,test_sysbench_net_subnet_id)
        #初始化trove必须有的资源


        self._trove_volume_size = '100'
        self._database_name = 'sbtest'
        self._user_name = 'test'
        self._user_password = '123456..'
        self._datastore_name = 'mysql'
        self._datastore_version_name = '5.6'


        for i in range(STABILITY_TEST_SYSBENCH_GROUP_NUM):
            stabilitySysbenchLogger.info('初始化Sysbench测试的云主机')
            # 启动一组Sysbench测试,同网段
            sysbench_computePair=[]

            computeName = addUUID('sysbench' + str(i))
            testType = 'sysbench'

            #申请一个浮动ip
            test_floatIp = FloatIp()
            try:
                test_floatIp.ip = self._neutronClient.getFloatIp(self._admin_float_net_id, FLOAT_IP_QOS)
                test_floatIp.id = self._neutronClient.getFloatId(test_floatIp.ip)
                stabilitySysbenchLogger.info('申请到一个浮动ip:' + test_floatIp.ip)
            except Exception, e:
                stabilitySysbenchLogger.info('申请浮动ip失败:'+'\r\n'+e.message)

            self._accountResource.add_floatIp(test_floatIp)



            #启动云主机
            test_compute = Compute()
            test_compute.name = computeName
            test_compute.testType=testType
            stabilitySysbenchLogger.info('启动云主机'+test_compute.name)
            try:
                test_compute.id=self._novaClient.bootCompute(computeName,
                                                         self._test_sysbench_flavor_id,
                                                         self._test_image_id,
                                                         self._test_sysbench_net_id,
                                                         self._default_secgroup_id,
                                                         random.choice(ZONE_NAMES),
                                                         self._user_data_path)
            except Exception, e:
                stabilitySysbenchLogger.info('启动云主机' + test_compute.name + '失败'+'\r\n'+e.message)


            #绑定浮动ip
            stabilitySysbenchLogger.info('为云主机' + test_compute.name + '绑定浮动ip:' + test_floatIp.ip)
            try:
                is_add_succ=self._novaClient.addFloatForCompute(test_compute.id,test_floatIp.ip)
            except Exception, e:
                stabilitySysbenchLogger.info('为云主机' + test_compute.name + '绑定浮动ip:' + test_floatIp.ip + '失败'+'\r\n'+e.message)
            if is_add_succ:
               test_compute.float_ip=test_floatIp.ip



            #创建数据库实例
            troveName = addUUID('trove' + str(i))
            test_trove = Trove()
            test_trove.name = troveName
            stabilitySysbenchLogger.info('创建一台数据库实例' + test_trove.name)
            try:
                test_trove.id = self._troveClient.createtrove(test_trove.name,
                                                               self._test_sysbench_flavor_id,
                                                               self._trove_volume_size,
                                                               self._database_name,
                                                               self._user_name,
                                                               self._user_password,
                                                               self._test_sysbench_net_id,
                                                               random.choice(ZONE_NAMES),
                                                               self._datastore_name,
                                                               self._datastore_version_name)
            except Exception, e:
                stabilitySysbenchLogger.info('创建一台数据库实例' + test_trove.name + '失败'+'\r\n'+e.message)

            test_trove.ip = self._novaClient.getComputeIp(test_trove.name)


            sysbench_computePair.append(test_compute)
            self._accountResource.add_compute(test_compute)
            sysbench_computePair.append(test_trove)
            #self._accountResource.add_compute(test_trove)
            #设置一组iperf云主机
            self._accountResource.add_sysbenchComputePair(sysbench_computePair)


    def getStabilitySysbenchAccountResource(self):
        return self._accountResource


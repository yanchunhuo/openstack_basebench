#!-*- coding:utf8 -*-
from src.clients.neutronClient import NeutronClient
from src.clients.cinderClient import CinderClient
from src.clients.novaClient import NovaClient
from config.config import DEFAULT_SECGROUP_NAME
from config.config import STABILITY_TEST_UNIXBENCH_FLAVOR
from config.config import TEST_IMAGE_NAME
from config.config import ADMIN_FLOAT_NET_NAME
from config.config import ZONE_NAMES
from config.config import IS_STABILITY_TEST_UNIXBENCH
from config.config import FLOAT_IP_QOS
from config.config import STABILITY_UNIXBENCH_ACCOUNT_OS_TENANT_NAME
from config.config import STABILITY_UNIXBENCH_ACCOUNT_OS_PROJECT_NAME
from config.config import STABILITY_UNIXBENCH_ACCOUNT_OS_USERNAME
from config.config import STABILITY_UNIXBENCH_ACCOUNT_OS_PASSWORD
from config.config import STABILITY_TEST_UNIXBENCH_NUM
from src.common import addUUID
from src.common import writeObjectIntoFile
from src.pojo.Compute import Compute
from src.pojo.NET import Net
from src.pojo.Router import Router
from src.pojo.FloatIp import FloatIp
from src.logger import stabilityUnixbenchLogger
from src.init import Init
from src.accountResourceTools import getDefaultSecGroupId
from src.accountResourceTools import getAdminFloatNetId
from src.accountResourceTools import getTestImageId
from src.accountResourceTools import getFlavorId
import random

class InitUnixbenchResource():
    def __init__(self):
        self._os_tenant_name=STABILITY_UNIXBENCH_ACCOUNT_OS_TENANT_NAME
        self._os_project_name=STABILITY_UNIXBENCH_ACCOUNT_OS_PROJECT_NAME
        self._os_username =STABILITY_UNIXBENCH_ACCOUNT_OS_USERNAME
        self._os_password=STABILITY_UNIXBENCH_ACCOUNT_OS_PASSWORD

        self._init=Init(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password,stabilityUnixbenchLogger)
        self._accountResource = self._init.initAccountResource()

        self._router_name='unixbench_router'
        self._user_data_path='userdata/user_data'

        self._test_unixbench_net_name='unixbench_net'
        self._test_unixbench_subnet_cidr='192.168.30.0/24'

        stabilityUnixbenchLogger.info('===初始化稳定性测试基础资源[unixbench账号]===')
        self._initResource()

    def _initResource(self):
        """
        公共资源初始化
        :return:
        """
        stabilityUnixbenchLogger.info('初始化命令行客户端')
        self._neutronClient=NeutronClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._novaClient=NovaClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._cinderClient=CinderClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)

        stabilityUnixbenchLogger.info('初始化默认安全组、测试镜像、测试镜像')
        self._default_secgroup_id=getDefaultSecGroupId(self._accountResource.get_secgroups(),DEFAULT_SECGROUP_NAME)
        self._admin_float_net_id=getAdminFloatNetId(self._accountResource.get_adminNets(),ADMIN_FLOAT_NET_NAME)
        self._test_image_id=getTestImageId(self._accountResource.get_images(),TEST_IMAGE_NAME)

        stabilityUnixbenchLogger.info('初始化一个路由器资源，创建名为' + self._router_name + '的路由')
        test_router=Router()
        test_router.name=addUUID(self._router_name)
        try:
            test_router.id=self._neutronClient.createRouter(test_router.name,self._admin_float_net_id)
            self._router_id = test_router.id
        except Exception, e:
            stabilityUnixbenchLogger.error('创建路由器' + self._router_name + '失败!'+'\r\n'+e.message)
        self._accountResource.add_router(test_router)

        #判断是否进行unixbench测试
        if IS_STABILITY_TEST_UNIXBENCH:
            stabilityUnixbenchLogger.info('===开始初始化稳定性测试unixbench资源===')
            self._initUnixbench()

        stabilityUnixbenchLogger.info('将测试初始化资源写入到文件dbs/stabilityUnixbenchTestAccountResource.dbs')
        writeObjectIntoFile(self._accountResource,'dbs/stabilityUnixbenchTestAccountResource.dbs')

    def _initUnixbench(self):
        """
        根据unixbench所需要测试，创建云主机
        :return:
        """
        stabilityUnixbenchLogger.info('初始化unixbench测试的云主机规格')
        self._test_unixbench_flavor_id = getFlavorId(self._accountResource.get_flavors(), STABILITY_TEST_UNIXBENCH_FLAVOR)

        stabilityUnixbenchLogger.info('初始化unixbench网络资源，创建名为' + self._test_unixbench_net_name + '的网络')
        test_unixbench_net = Net()
        test_unixbench_net.name = addUUID(self._test_unixbench_net_name)
        test_unixbench_net.cidr = self._test_unixbench_subnet_cidr
        try:
            test_unixbench_net.id = self._neutronClient.createNetwork(test_unixbench_net.name, test_unixbench_net.cidr)
            self._test_unixbench_net_id = test_unixbench_net.id
        except Exception,e:
            stabilityUnixbenchLogger.error('创建unixbench所需网络' + self._test_unixbench_net_name + '失败!'+'\r\n'+e.message)
        self._accountResource.add_net(test_unixbench_net)

        stabilityUnixbenchLogger.info('将unixbench网络' + self._test_unixbench_net_name + '绑定到路由器' + self._router_name)
        try:
            test_unixbench_net_subnet_id = self._neutronClient.getSubNetId(self._test_unixbench_net_id)
            self._neutronClient.addRouterInterface(self._router_id, test_unixbench_net_subnet_id)
        except Exception, e:
            stabilityUnixbenchLogger.error('将unixbench网络' + self._test_unixbench_net_name + '绑定到路由器' + self._router_name +'失败!'+'\r\n'+e.message)

        stabilityUnixbenchLogger.info('初始化unixbench测试的云主机')
        for i in range(STABILITY_TEST_UNIXBENCH_NUM):
            computeName = addUUID('unixbench'+str(i))
            testType = 'unixbench'

            #申请一个浮动ip
            stabilityUnixbenchLogger.info('申请一个浮动ip')
            test_floatIp=FloatIp()
            try:
                test_floatIp.ip = self._neutronClient.getFloatIp(self._admin_float_net_id,FLOAT_IP_QOS)
                test_floatIp.id = self._neutronClient.getFloatId(test_floatIp.ip)
            except Exception,e:
                stabilityUnixbenchLogger.error('申请浮动ip失败!'+'\r\n'+e.message)
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
                                                             random.choice(ZONE_NAMES),
                                                             self._user_data_path)
            except Exception, e:
                stabilityUnixbenchLogger.error('启动云主机'+test_compute.name+'失败!'+'\r\n'+e.message)
            #绑定浮动ip
            stabilityUnixbenchLogger.info('为云主机' + test_compute.name + '绑定浮动ip:' + test_floatIp.ip)
            try:
                is_add_succ=self._novaClient.addFloatForCompute(test_compute.id,test_floatIp.ip)
                if is_add_succ:
                   test_compute.float_ip=test_floatIp.ip
            except Exception, e:
                stabilityUnixbenchLogger.error('为云主机' + test_compute.name + '绑定浮动ip:' + test_floatIp.ip + '失败!' + '\r\n' + e.message)
            self._accountResource.add_unixbenchCompute(test_compute)
            self._accountResource.add_compute(test_compute)

    def getStabilityUnixbenchAccountResource(self):
        return self._accountResource


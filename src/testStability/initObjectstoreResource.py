#!-*- coding:utf8 -*-
import random
from config.config import STABILITY_OBJECTSTORE_ACCOUNT_OS_TENANT_NAME
from config.config import STABILITY_OBJECTSTORE_ACCOUNT_OS_PROJECT_NAME
from config.config import STABILITY_OBJECTSTORE_ACCOUNT_OS_USERNAME
from config.config import STABILITY_OBJECTSTORE_ACCOUNT_OS_PASSWORD
from config.config import IS_STABILITY_TEST_OBJECTSTORAGE
from config.config import DEFAULT_SECGROUP_NAME
from config.config import ADMIN_FLOAT_NET_NAME
from config.config import TEST_IMAGE_NAME
from config.config import STABILITY_TEST_OSS_FLAVOR
from config.config import FLOAT_IP_QOS
from config.config import ZONE_NAMES
from src.init import Init
from src.logger import stabilityObjectStorageLogger
from src.clients.neutronClient import NeutronClient
from src.clients.novaClient import NovaClient
from src.accountResourceTools import getDefaultSecGroupId
from src.accountResourceTools import getAdminFloatNetId
from src.accountResourceTools import getTestImageId
from src.accountResourceTools import getFlavorId
from src.common import addUUID
from src.common import writeObjectIntoFile
from src.pojo.Compute import Compute
from src.pojo.NET import Net
from src.pojo.Router import Router
from src.pojo.FloatIp import FloatIp

class InitObjectStoreResource():
    def __init__(self):
        self._os_tenant_name = STABILITY_OBJECTSTORE_ACCOUNT_OS_TENANT_NAME
        self._os_project_name = STABILITY_OBJECTSTORE_ACCOUNT_OS_PROJECT_NAME
        self._os_username = STABILITY_OBJECTSTORE_ACCOUNT_OS_USERNAME
        self._os_password = STABILITY_OBJECTSTORE_ACCOUNT_OS_PASSWORD

        self._init = Init(self._os_tenant_name, self._os_project_name, self._os_username, self._os_password,stabilityObjectStorageLogger)
        self._accountResource = self._init.initAccountResource()

        self._router_name = 'stablity_oss_router'
        self._user_data_path = 'userdata/user_data'
        self._oss_net_name = 'oss_stable_net'
        self._oss_subnet_cidr = '192.168.50.0/24'

        stabilityObjectStorageLogger.info('===初始化对象存储稳定性测试资源===')
        self._initResource()

    def _initResource(self):
        """
         """
        stabilityObjectStorageLogger.info('初始化命令行客户端')
        self._neutronClient = NeutronClient(self._os_tenant_name, self._os_project_name, self._os_username,self._os_password)
        self._novaClient = NovaClient(self._os_tenant_name, self._os_project_name, self._os_username, self._os_password)

        stabilityObjectStorageLogger.info('初始化默认安全组、外部网络、测试镜像')
        self._default_secgroup_id = getDefaultSecGroupId(self._accountResource.get_secgroups(), DEFAULT_SECGROUP_NAME)
        self._admin_float_net_id = getAdminFloatNetId(self._accountResource.get_adminNets(), ADMIN_FLOAT_NET_NAME)
        self._test_image_id = getTestImageId(self._accountResource.get_images(), TEST_IMAGE_NAME)

        stabilityObjectStorageLogger.info('初始化一个路由器资源，创建名为' + self._router_name + '的路由')
        test_router = Router()
        test_router.name = addUUID(self._router_name)
        try:
            test_router.id = self._neutronClient.createRouter(test_router.name, self._admin_float_net_id)
        except Exception,e:
            stabilityObjectStorageLogger.error('创建路由器'+test_router.name+'失败!'+'\r\n'+e.message)
        self._router_id = test_router.id
        self._accountResource.add_router(test_router)

        if IS_STABILITY_TEST_OBJECTSTORAGE:
            stabilityObjectStorageLogger.info('===开始初始化对象存储稳定性测试资源===')
            self._initObjectstore()

        stabilityObjectStorageLogger.info('将测试初始化资源写入到文件dbs/stabilityObjectStorageTestAccountResource.dbs')
        writeObjectIntoFile(self._accountResource, 'dbs/stabilityObjectStorageTestAccountResource.dbs')

    def _initObjectstore(self):
        '''
        初始化对象存储稳定性测试资源
        :return:
        '''
        stabilityObjectStorageLogger.info('初始化对象存储测试的云主机规格')
        self._test_oss_flavor_id = getFlavorId(self._accountResource.get_flavors(), STABILITY_TEST_OSS_FLAVOR)

        stabilityObjectStorageLogger.info('初始化对象存储网络资源，创建名为' + self._oss_net_name + '的网络')
        oss_test_net = Net()
        oss_test_net.name = addUUID(self._oss_net_name)
        oss_test_net.cidr = self._oss_subnet_cidr
        try:
            oss_test_net.id = self._neutronClient.createNetwork(oss_test_net.name, oss_test_net.cidr)
        except Exception,e:
            stabilityObjectStorageLogger.error('创建网络'+oss_test_net.name+'失败!'+'\r\n'+e.message)
        self._oss_test_net_id = oss_test_net.id
        self._accountResource.add_net(oss_test_net)

        stabilityObjectStorageLogger.info('将网络' + self._oss_net_name + '绑定到路由器' + self._router_name)
        try:
            self._oss_subnet_id = self._neutronClient.getSubNetId(self._oss_test_net_id)
            self._neutronClient.addRouterInterface(self._router_id, self._oss_subnet_id)
        except Exception,e:
            stabilityObjectStorageLogger.error('将对象存储网络' + self._oss_net_name+ '绑定到路由器' + self._router_name+'失败!'++'\r\n'+e.message)

        stabilityObjectStorageLogger.info('初始化对象存储测试的云主机')
        computeName = addUUID('OSS')
        testType = addUUID('OSS')

        #申请浮动IP
        test_oss_floatIp = FloatIp()
        try:
            test_oss_floatIp.ip = self._neutronClient.getFloatIp(self._admin_float_net_id, FLOAT_IP_QOS)
            test_oss_floatIp.id = self._neutronClient.getFloatId(test_oss_floatIp.ip)
        except Exception,e:
            stabilityObjectStorageLogger.error('申请浮动ip失败!'+'\r\n'+e.message)
        self._accountResource.add_floatIp(test_oss_floatIp)

        #启动云主机
        test_oss_compute = Compute()
        test_oss_compute.name = computeName
        test_oss_compute.testType = testType
        try:
            test_oss_compute.id = self._novaClient.bootCompute(computeName,
                                                               self._test_oss_flavor_id,
                                                               self._test_image_id,
                                                               self._oss_test_net_id,
                                                               self._default_secgroup_id,
                                                               random.choice(ZONE_NAMES),
                                                               self._user_data_path)
        except Exception,e:
            stabilityObjectStorageLogger.error('启动云主机'+test_oss_compute.name+'失败!'+'\r\n'+e.message)
        # 绑定浮动ip
        try:
            is_add_succ=self._novaClient.addFloatForCompute(test_oss_compute.id, test_oss_floatIp.ip)
            if is_add_succ:
                test_oss_compute.float_ip = test_oss_floatIp.ip
        except Exception,e:
            stabilityObjectStorageLogger.error('为云主机'+test_oss_compute.name+'绑定浮动ip:'+test_oss_floatIp.ip+'失败!'+'\r\n'+e.message)

        self._accountResource.add_objectstorageCompute(test_oss_compute)
        self._accountResource.add_compute(test_oss_compute)

    def getStableObjectstoreResource(self):
        return self._accountResource


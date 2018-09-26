#!-*- coding:utf8 -*-
from src.accountResourceTools import getDefaultSecGroupId
from src.accountResourceTools import getAdminFloatNetId
from src.accountResourceTools import getTestImageId
from src.accountResourceTools import getFlavorId
from src.common.fileTool import FileTool
from src.loggers import Loggers
from src.readConfig import ReadConfig
from src.common.strTool import StrTool
from src.clients.openstackClient import OpenstackClient
from src.clients.novaClient import NovaClient
from src.init import Init
from src.pojo.Compute import Compute
from src.pojo.NET import Net
from src.pojo.Router import Router
from src.pojo.FloatIp import FloatIp
import random


class InitObjectStoreResource:
    def __init__(self):
        self._readConfig=ReadConfig()
        self._loggers=Loggers()

        self._os_tenant_name = self._readConfig.accounts.stability_objstore_os_tenant_name
        self._os_project_name = self._readConfig.accounts.stability_objstore_os_project_name
        self._os_username = self._readConfig.accounts.stability_objstore_os_username
        self._os_password = self._readConfig.accounts.stability_objstore_os_password

        self._init = Init(self._os_tenant_name, self._os_project_name, self._os_username, self._os_password,self._loggers.stabilityObjstoreLogger)
        self._accountResource = self._init.initAccountResource()

        self._router_name = 'basebench_stablity_oss_router'
        self._user_data_path = 'userdata/user_data'
        self._oss_net_name = 'basebench_oss_stable_net'
        self._oss_subnet_cidr = '192.168.50.0/24'

        self._loggers.stabilityObjstoreLogger.info('===初始化对象存储稳定性测试资源===')
        self._initResource()

    def _initResource(self):
        """
         """
        self._loggers.stabilityObjstoreLogger.info('初始化命令行客户端')
        self._openstackClient = OpenstackClient(self._os_tenant_name, self._os_project_name, self._os_username,self._os_password)
        self._novaClient = NovaClient(self._os_project_name, self._os_username, self._os_password)

        self._loggers.stabilityObjstoreLogger.info('初始化默认安全组、外部网络、测试镜像')
        self._default_secgroup_id = getDefaultSecGroupId(self._accountResource.get_secgroups(), self._readConfig.base.default_secgroup_name)
        self._admin_float_net_id = getAdminFloatNetId(self._accountResource.get_adminNets(), self._readConfig.base.admin_float_net_name)
        self._test_image_id = getTestImageId(self._accountResource.get_images(), self._readConfig.base.test_image_name)

        self._zone_names = self._readConfig.base.zone_names.split('||')

        if self._readConfig.executeTest.is_stability_test_objstore.lower()=='true':
            self._loggers.stabilityObjstoreLogger.info('===开始初始化对象存储稳定性测试资源===')
            self._initObjectstore()

        self._loggers.stabilityObjstoreLogger.info('将测试初始化资源写入到文件dbs/stabilityObjectStorageTestAccountResource.dbs')
        FileTool.writeObjectIntoFile(self._accountResource, 'dbs/stabilityObjectStorageTestAccountResource.dbs')

    def _initObjectstore(self):
        """
        初始化对象存储稳定性测试资源
        :return:
        """
        self._loggers.stabilityObjstoreLogger.info('初始化对象存储测试的云主机规格')
        self._test_oss_flavor_id = getFlavorId(self._accountResource.get_flavors(), self._readConfig.executeTest.stability_test_objstore_load_flavor)

        self._loggers.stabilityObjstoreLogger.info('初始化对象存储网络资源，创建名为' + self._oss_net_name + '的网络')
        oss_test_net = Net()
        oss_test_net.name = StrTool.addUUID(self._oss_net_name)
        oss_test_net.cidr = self._oss_subnet_cidr
        try:
            oss_test_net.id = self._openstackClient.createNetwork(oss_test_net.name, oss_test_net.cidr)
        except Exception,e:
            self._loggers.stabilityObjstoreLogger.error('创建网络'+oss_test_net.name+'失败!'+'\r\n'+e.message)
        self._oss_test_net_id = oss_test_net.id
        self._accountResource.add_net(oss_test_net)

        self._loggers.stabilityObjstoreLogger.info('初始化一个路由器资源，创建名为' + self._router_name + '的路由')
        test_router = Router()
        test_router.name = StrTool.addUUID(self._router_name)
        try:
            test_router.id = self._openstackClient.createRouter(test_router.name, self._admin_float_net_id)
        except Exception, e:
            self._loggers.stabilityObjstoreLogger.error('创建路由器' + test_router.name + '失败!' + '\r\n' + e.message)
        self._router_id = test_router.id
        self._loggers.stabilityObjstoreLogger.info('将网络' + self._oss_net_name + '绑定到路由器' + self._router_name)
        try:
            oss_subnet_id = self._openstackClient.getSubNetId(self._oss_test_net_id)
            self._openstackClient.addRouterInterface(self._router_id, oss_subnet_id)
            test_router.add_subnet_id(oss_subnet_id)
        except Exception,e:
            self._loggers.stabilityObjstoreLogger.error('将对象存储网络' + self._oss_net_name+ '绑定到路由器' + self._router_name+'失败!'+'\r\n'+e.message)
        self._accountResource.add_router(test_router)

        self._loggers.stabilityObjstoreLogger.info('初始化对象存储测试的云主机')
        computeName = StrTool.addUUID('basebench_OSS')
        testType = StrTool.addUUID('OSS')

        #申请浮动IP
        test_oss_floatIp = FloatIp()
        try:
            test_oss_floatIp.ip = self._openstackClient.getFloatIp(self._admin_float_net_id)
            test_oss_floatIp.id = self._openstackClient.getFloatId(test_oss_floatIp.ip)
        except Exception,e:
            self._loggers.stabilityObjstoreLogger.error('申请浮动ip失败!'+'\r\n'+e.message)
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
                                                               random.choice(self._zone_names),
                                                               self._user_data_path)
        except Exception,e:
            self._loggers.stabilityObjstoreLogger.error('启动云主机'+test_oss_compute.name+'失败!'+'\r\n'+e.message)
        # 绑定浮动ip
        try:
            is_add_succ=self._novaClient.addFloatForCompute(test_oss_compute.id, test_oss_floatIp.ip)
            if is_add_succ:
                test_oss_compute.float_ip = test_oss_floatIp.ip
        except Exception,e:
            self._loggers.stabilityObjstoreLogger.error('为云主机'+test_oss_compute.name+'绑定浮动ip:'+test_oss_floatIp.ip+'失败!'+'\r\n'+e.message)

        self._accountResource.add_objectstorageCompute(test_oss_compute)
        self._accountResource.add_compute(test_oss_compute)

    def getStableObjectstoreResource(self):
        return self._accountResource


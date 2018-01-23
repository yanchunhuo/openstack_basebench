#!-*- coding:utf8 -*-
from src.clients.neutronClient import NeutronClient
from src.clients.cinderClient import CinderClient
from src.clients.novaClient import NovaClient
from src.clients.loadbalancerClient import LoadbalancerClient
from config.config import DEFAULT_SECGROUP_NAME
from config.config import TEST_IMAGE_NAME
from config.config import ADMIN_FLOAT_NET_NAME
from config.config import ZONE_NAMES
from config.config import IS_STABILITY_TEST_LOADBALANCER
from config.config import IS_STABILITY_TEST_JMETER
from config.config import FLOAT_IP_QOS
from config.config import STABILITY_LOADBALANCER_ACCOUNT_OS_TENANT_NAME
from config.config import STABILITY_LOADBALANCER_ACCOUNT_OS_PROJECT_NAME
from config.config import STABILITY_LOADBALANCER_ACCOUNT_OS_USERNAME
from config.config import STABILITY_LOADBALANCER_ACCOUNT_OS_PASSWORD
from config.config import STABILITY_TEST_LOADBALANCER_FLAVOR
from config.config import STABILITY_TEST_LOADBALANCER_GROUP_NUM
from config.config import STABILITY_TEST_LOADBALANCER_MEMBER_NUM
from config.config import STABILITY_TEST_LOADBALANCER_MEMBER_WEIGHT
from config.config import connection_limit,protocol,protocol_port,lb_algorithmt,delay_time,max_retries,timeout,protocol_type
from src.common import addUUID
from src.common import writeObjectIntoFile
from src.pojo.Compute import Compute
from src.pojo.NET import Net
from src.pojo.Router import Router
from src.pojo.FloatIp import FloatIp
from src.pojo.LoadBalancer import LoadBalancer
from src.logger import stabilityLoadbalancerLogger
from src.init import Init
from src.accountResourceTools import getDefaultSecGroupId
from src.accountResourceTools import getAdminFloatNetId
from src.accountResourceTools import getTestImageId
from src.accountResourceTools import getFlavorId
import random

class InitLoadbalancerResource():
    def __init__(self):
        self._os_tenant_name=STABILITY_LOADBALANCER_ACCOUNT_OS_TENANT_NAME
        self._os_project_name=STABILITY_LOADBALANCER_ACCOUNT_OS_PROJECT_NAME
        self._os_username =STABILITY_LOADBALANCER_ACCOUNT_OS_USERNAME
        self._os_password=STABILITY_LOADBALANCER_ACCOUNT_OS_PASSWORD

        self._init=Init(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password,stabilityLoadbalancerLogger)
        self._accountResource = self._init.initAccountResource()
        self._router_name = 'loadbalancer_router'
        self._user_data_path='userdata/user_data'

        self._test_loadbalancer_net_name = 'loadbalancer_net'
        self._test_loadbalancer_subnet_cidr = '192.168.80.0/24'
        self._test_loadbalancer_subnet_cidr = '192.168.80.0/24'

        stabilityLoadbalancerLogger.info('===初始化稳定性测试基础资源[loadbalancer账号]===')
        self._initResource()

    def _initResource(self):
        """
        公共资源初始化
        :return:
        """
        stabilityLoadbalancerLogger.info('初始化命令行客户端')
        self._neutronClient=NeutronClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._novaClient=NovaClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._cinderClient=CinderClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._loadbalancerClient = LoadbalancerClient(self._os_tenant_name, self._os_project_name, self._os_username,self._os_password)

        stabilityLoadbalancerLogger.info('初始化默认安全组、测试镜像、测试镜像')
        self._default_secgroup_id=getDefaultSecGroupId(self._accountResource.get_secgroups(),DEFAULT_SECGROUP_NAME)
        self._admin_float_net_id=getAdminFloatNetId(self._accountResource.get_adminNets(),ADMIN_FLOAT_NET_NAME)
        self._test_image_id=getTestImageId(self._accountResource.get_images(),TEST_IMAGE_NAME)

        stabilityLoadbalancerLogger.info('初始化一个路由器资源，创建名为' + self._router_name + '的路由')
        test_router=Router()
        test_router.name=addUUID(self._router_name)
        try:
            test_router.id=self._neutronClient.createRouter(test_router.name,self._admin_float_net_id)
        except Exception, e:
            stabilityLoadbalancerLogger.error('创建路由器' + self._router_name + '失败!'+'\r\n'+e.message)
        self._router_id=test_router.id
        self._accountResource.add_router(test_router)

        #判断需要测试的类型
        if IS_STABILITY_TEST_LOADBALANCER and IS_STABILITY_TEST_JMETER:
            stabilityLoadbalancerLogger.info('===开始初始化稳定性测试loadbalancer资源===')
            self._initLoadbalancer()

        stabilityLoadbalancerLogger.info('将测试初始化资源写入到文件dbs/stabilityLoadbalancerTestAccountResource.dbs')
        writeObjectIntoFile(self._accountResource,'dbs/stabilityLoadbalancerTestAccountResource.dbs')


    def _initLoadbalancer(self):
        """
        初始化loadbalancer测试必须有的资源
        :return:
        """
        stabilityLoadbalancerLogger.info('初始化loadbalancer测试的云主机规格')
        self._test_loadbalancer_flavor_id=getFlavorId(self._accountResource.get_flavors(),STABILITY_TEST_LOADBALANCER_FLAVOR)

        stabilityLoadbalancerLogger.info('初始化loadbalancer测试的网络'+self._test_loadbalancer_net_name)
        test_loadbalancer_net=Net()
        test_loadbalancer_net.name=self._test_loadbalancer_net_name
        test_loadbalancer_net.cidr = self._test_loadbalancer_subnet_cidr
        try:
            test_loadbalancer_net.id=self._neutronClient.createNetwork(self._test_loadbalancer_net_name,self._test_loadbalancer_subnet_cidr)
        except Exception, e:
            stabilityLoadbalancerLogger.error('创建loadbalancer网络' + self._test_unixbench_net_name + '失败!'+'\r\n'+e.message)
        self._test_loadbalancer_net_id=test_loadbalancer_net.id
        self._accountResource.add_net(test_loadbalancer_net)

        stabilityLoadbalancerLogger.info('将loadbalancer网络' + self._test_loadbalancer_net_name + '绑定到路由器' + self._router_name)
        try:
            test_loadbalancer_net_subnet_id = self._neutronClient.getSubNetId(self._test_loadbalancer_net_id)
            self._neutronClient.addRouterInterface(self._router_id,test_loadbalancer_net_subnet_id)
        except Exception, e:
            stabilityLoadbalancerLogger.error('将loadbalancer网络' + self._test_loadbalancer_net_name + '绑定到路由器' + self._router_name+'失败!'+'\r\n'+e.message)

        for i in range(STABILITY_TEST_LOADBALANCER_GROUP_NUM):
            stabilityLoadbalancerLogger.info('初始化loadbalancer测试的云主机')
            loadbalancerName = addUUID('loadbalancer' + str(i))
            test_loadbalancer = LoadBalancer()
            test_loadbalancer.name = loadbalancerName
            # 启动一组loadbalancer测试云主机,以及一台jmeter云主机
            member_ips_weight = []
            for j in range(STABILITY_TEST_LOADBALANCER_MEMBER_NUM):
                member_computeName = addUUID('loadbalancer_' + str(i)+'_'+str(j))
                tmp_testType = 'loadbalancer'

                #申请一个浮动ip
                stabilityLoadbalancerLogger.info('为后端服务器申请一个浮动ip')
                member_floatIp = FloatIp()
                try:
                    member_floatIp.ip = self._neutronClient.getFloatIp(self._admin_float_net_id, FLOAT_IP_QOS)
                    member_floatIp.id = self._neutronClient.getFloatId(member_floatIp.ip)
                    stabilityLoadbalancerLogger.info('为后端服务器申请到一个浮动ip:'+member_floatIp.ip)
                except Exception, e:
                    stabilityLoadbalancerLogger.error('为后端服务器申请浮动ip失败!'+'\r\n'+e.message)
                self._accountResource.add_floatIp(member_floatIp)

                #创建云主机
                member_compute = Compute()
                member_compute.name=member_computeName
                member_compute.testType = tmp_testType
                try:
                    member_compute.id=self._novaClient.bootCompute(member_compute.name,
                                                                 self._test_loadbalancer_flavor_id,
                                                                 self._test_image_id,
                                                                 self._test_loadbalancer_net_id,
                                                                 self._default_secgroup_id,
                                                                 random.choice(ZONE_NAMES),
                                                                 self._user_data_path)
                except Exception, e:
                    stabilityLoadbalancerLogger.error('启动一台后端服务器'+member_compute.name+'失败!'+'\r\n'+e.message)

                #绑定浮动ip
                stabilityLoadbalancerLogger.info('为后端服务器' + member_compute.name + '绑定浮动ip:' + member_floatIp.ip)
                try:
                    is_add_succ=self._novaClient.addFloatForCompute(member_compute.id,member_floatIp.ip)
                    if is_add_succ:
                        member_compute.float_ip=member_floatIp.ip
                except Exception, e:
                    stabilityLoadbalancerLogger.error('为后端服务器' + member_compute.name + '绑定浮动ip:' + member_floatIp.ip+'失败!'+'\r\n'+e.message)
                test_loadbalancer.add_member(member_compute)
                self._accountResource.add_compute(member_compute)
                tmp_member_ip_weight = []
                member_compute.ip = self._novaClient.getComputeIp(member_compute.name)
                member_weight = STABILITY_TEST_LOADBALANCER_MEMBER_WEIGHT[j]
                tmp_member_ip_weight.append(member_compute.ip)
                tmp_member_ip_weight.append(member_weight)
                member_ips_weight.append(tmp_member_ip_weight)

            # 申请一个浮动ip
            stabilityLoadbalancerLogger.info('为负载均衡器申请到一个浮动ip')
            loadbalancer_floatIp = FloatIp()
            try:
                loadbalancer_floatIp.ip = self._neutronClient.getFloatIp(self._admin_float_net_id, FLOAT_IP_QOS)
                loadbalancer_floatIp.id = self._neutronClient.getFloatId(loadbalancer_floatIp.ip)
                stabilityLoadbalancerLogger.info('为负载均衡器申请到一个浮动ip:' + loadbalancer_floatIp.ip)
            except Exception,e:
                stabilityLoadbalancerLogger.error('为负载均衡器申请浮动ip失败!'+'\r\n'+e.message)
            self._accountResource.add_floatIp(loadbalancer_floatIp)
            #启动负载均衡器
            try:
                test_loadbalancer.id = self._loadbalancerClient.createLoadbalancer(test_loadbalancer.name,
                                                                                   loadbalancer_floatIp.id,
                                                                                   test_loadbalancer_net_subnet_id,
                                                                                   connection_limit,
                                                                                   protocol,
                                                                                   protocol_port,
                                                                                   lb_algorithmt,
                                                                                   delay_time,
                                                                                   max_retries,
                                                                                   timeout,
                                                                                   protocol_type,
                                                                                   member_ips_weight)
            except Exception,e:
                stabilityLoadbalancerLogger.error('启动负载均衡器'+test_loadbalancer.name+'失败!'+'\r\n'+e.message)
            if test_loadbalancer.id:
                test_loadbalancer.virtual_ip = loadbalancer_floatIp.ip
                test_loadbalancer.port = protocol_port

                jmeter_computeName = addUUID('loadbalancer_jmeter' + str(i))
                tmp_testType = 'loadbalancer_jmeter'
                # 申请一个浮动ip
                stabilityLoadbalancerLogger.info('为负载均衡器加压云主机申请到一个浮动ip')
                jmeter_floatIp = FloatIp()
                try:
                    jmeter_floatIp.ip = self._neutronClient.getFloatIp(self._admin_float_net_id, FLOAT_IP_QOS)
                    jmeter_floatIp.id = self._neutronClient.getFloatId(jmeter_floatIp.ip)
                    stabilityLoadbalancerLogger.info('为负载均衡器加压云主机申请到一个浮动ip:'+jmeter_floatIp.ip)
                except Exception,e:
                    stabilityLoadbalancerLogger.error('为负载均衡器加压云主机申请浮动ip失败!'+'\r\n'+e.message)
                self._accountResource.add_floatIp(jmeter_floatIp)

                # 创建均衡负载器加压的云主机
                jmeter_compute = Compute()
                jmeter_compute.name = jmeter_computeName
                jmeter_compute.testType = tmp_testType
                try:
                    jmeter_compute.id = self._novaClient.bootCompute(jmeter_compute.name,
                                                                   self._test_loadbalancer_flavor_id,
                                                                   self._test_image_id,
                                                                   self._test_loadbalancer_net_id,
                                                                   self._default_secgroup_id,
                                                                   random.choice(ZONE_NAMES),
                                                                   self._user_data_path)
                except Exception, e:
                    stabilityLoadbalancerLogger.error('启动负载均衡器加压云主机'+jmeter_compute.name+'失败!'+'\r\n'+e.message)
                # 绑定浮动ip
                stabilityLoadbalancerLogger.info('为负载均衡器加压云主机' + jmeter_compute.name + '绑定浮动ip:' + jmeter_floatIp.ip)
                try:
                    is_add_succ = self._novaClient.addFloatForCompute(jmeter_compute.id, jmeter_floatIp.ip)
                    if is_add_succ:
                        jmeter_compute.float_ip = jmeter_floatIp.ip
                        test_loadbalancer.load_compute = jmeter_compute
                except Exception, e:
                    stabilityLoadbalancerLogger.error('为负载均衡器加压云主机' + jmeter_compute.name + '绑定浮动ip:' + jmeter_floatIp.ip + '失败!' + '\r\n' + e.message)
                self._accountResource.add_compute(jmeter_compute)
                test_loadbalancer.load_compute=jmeter_compute

            #设置一组loadbalancer云主机
            self._accountResource.add_loadbalancer(test_loadbalancer)

    def getStabilityLoadbalancerAccountResource(self):
        return self._accountResource


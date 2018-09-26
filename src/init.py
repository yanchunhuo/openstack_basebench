#!-*- coding:utf8 -*-
from src.clients.openstackClient import OpenstackClient
from src.clients.novaClient import NovaClient
from src.clients.cinderClient import CinderClient
from src.clients.keystoneClient import KeystoneClient
from src.readConfig import ReadConfig
from src.pojo.AccountResource import AccountResource
from src.pojo.Account import Account
from src.pojo.SecGroup import SecGroup
from src.pojo.AdminNet import AdminNet
from src.pojo.Flavor import Flavor
from src.pojo.Image import Image
from src.pojo.VolumeType import VolumeType

class Init:
    def __init__(self,os_tenant_name,os_project_name,os_username,os_password,logger):
        self._readConfig=ReadConfig()
        self._logger=logger
        self._logger.info('===开始初始化账号'+os_username+'公共资源===')
        self._os_tenant_name=os_tenant_name
        self._os_project_name=os_project_name
        self._os_username=os_username
        self._os_password=os_password

        self._accountResource=AccountResource()

        self._openstackClient=OpenstackClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._novaClient=NovaClient(self._os_project_name,self._os_username,self._os_password)
        self._cinderClient=CinderClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._keystoneClient=KeystoneClient()

    def initAccountResource(self):
        """
        初始化一个账号，并设置必要的公共资源
        :return:
        """
        self._logger.info('创建账号'+self._os_username)
        test_account = Account()
        test_account.os_tenant_name = self._os_tenant_name
        test_account.os_project_name = self._os_project_name
        test_account.os_username = self._os_username
        test_account.os_password = self._os_password
        try:
            project_id,user_id=self._keystoneClient.createAccount(self._os_project_name,self._os_username,self._os_password)
            test_account.os_project_id=project_id
            test_account.os_userid=user_id
            self._keystoneClient.setAccountBucketsQuota(500,project_id)
            #openstack O版本无需配置
            #self._keystoneClient.setAccountImageQuota(500,100,project_id)
            self._keystoneClient.setAccountNetworkQuota(project_id,100,100,100,100,100)
            self._keystoneClient.setInstanceStorageQuota(project_id,65535,100,1024000,100,100,327675)
            self._keystoneClient.setObjectStoreQuota(5497558138880,project_id)
        except Exception,e:
            self._logger.error('创建账号'+self._os_username+'失败!'+'\r\n'+e.message)
        self._accountResource.add_account(test_account)

        self._logger.info('初始化默认安全组资源'+self._readConfig.base.default_secgroup_name)
        default_secgroup = SecGroup()
        default_secgroup.name = self._readConfig.base.default_secgroup_name
        try:
            default_secgroup.id=self._openstackClient.getSecGroupId(self._readConfig.base.default_secgroup_name)
            # 将安全组tcp规则放开
            self._logger.info('开放安全组'+default_secgroup.name+'的tcp规则')
            self._openstackClient.addAllowTcpRule(default_secgroup.id)
            # 将安全组icmp规则放开
            self._logger.info('开放安全组' + default_secgroup.name + '的icmp规则')
            self._openstackClient.addAllowIcmpRule(default_secgroup.id)
        except Exception,e:
            self._logger.error('初始化安全组资源'+self._readConfig.base.default_secgroup_name+'失败!'+'\r\n'+e.message)
        self._accountResource.add_secgroup(default_secgroup)

        #账户加入外部网络
        self._logger.info('初始化外部网络资源' + self._readConfig.base.admin_float_net_name)
        admin_float_net = AdminNet()
        admin_float_net.name = self._readConfig.base.admin_float_net_name
        try:
            admin_float_net.id=self._openstackClient.getNetId(self._readConfig.base.admin_float_net_name)
        except Exception,e:
            self._logger.error('初始化外部网络'+self._readConfig.base.admin_float_net_name+'资源失败!'+'\r\n'+e.message)
        self._accountResource.add_adminNet(admin_float_net)

        #账户里加入云主机类型
        self._logger.info('初始化云主机规格资源'+self._readConfig.base.flavor_type_names)
        flavor_types=self._readConfig.base.flavor_type_names.split('||')
        for flavor_type_str in flavor_types:
            tmp_flavor_type=flavor_type_str.split('&')
            flavor_type=Flavor()
            flavor_type.type=tmp_flavor_type[0]
            flavor_type.name=tmp_flavor_type[1]
            try:
                flavor_type.id=self._novaClient.getFlavorId(flavor_type.name)
            except Exception, e:
                self._logger.error('初始化云主机规格资源' + flavor_type_str + '失败!' + '\r\n' + e.message)
            self._accountResource.add_flavor(flavor_type)

        #账户里加入镜像
        self._logger.info('初始化测试镜像资源' + self._readConfig.base.test_image_name)
        test_image = Image()
        test_image.name = self._readConfig.base.test_image_name
        try:
            test_image.id=self._novaClient.getImageId(self._readConfig.base.test_image_name)
        except Exception,e:
            self._logger.error('初始化测试镜像资源'+self._readConfig.base.test_image_name+'失败!'+'\r\n'+e.message)
        self._accountResource.add_image(test_image)

        #账户里加入磁盘类型
        self._logger.info('初始化磁盘类型资源'+self._readConfig.base.volume_type_names)
        volume_types=self._readConfig.base.volume_type_names.split('||')
        for volume_type_str in volume_types:
            volume_type=VolumeType()
            tmp_volume_type=volume_type_str.split('&')
            volume_type.type=tmp_volume_type[0]
            volume_type.name=tmp_volume_type[1]
            try:
                volume_type.id=self._cinderClient.getVolumeTypeId(volume_type.name)
            except Exception, e:
                self._logger.error('初始化磁盘类型资源' + volume_type_str + '失败!' + '\r\n' + e.message)
            self._accountResource.add_volumeType(volume_type)

        #账户里加入可用域
        self._logger.info('初始化可用域资源')
        self._accountResource.add_zone(self._readConfig.base.zone_names.split('||'))

        return self._accountResource

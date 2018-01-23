#!-*- coding:utf8 -*-
from src.pojo.AccountResource import AccountResource
from src.pojo.Account import Account
from src.pojo.SecGroup import SecGroup
from src.pojo.AdminNet import AdminNet
from src.pojo.Flavor import Flavor
from src.pojo.Image import Image
from src.pojo.VolumeType import VolumeType

from src.clients.neutronClient import NeutronClient
from src.clients.novaClient import NovaClient
from src.clients.cinderClient import CinderClient
from src.clients.keystoneClient import KeystoneClient
from config.config import DEFAULT_SECGROUP_NAME
from config.config import ADMIN_FLOAT_NET_NAME
from config.config import FLAVOR_TYPE_NAME
from config.config import TEST_IMAGE_NAME
from config.config import VOLUME_TYPE_NAME
from config.config import ZONE_NAMES

class Init():
    def __init__(self,os_tenant_name,os_project_name,os_username,os_password,logger):
        self._logger=logger
        self._logger.info('===开始初始化账号'+os_username+'公共资源===')
        self._os_tenant_name=os_tenant_name
        self._os_project_name=os_project_name
        self._os_username=os_username
        self._os_password=os_password

        self._accountResource=AccountResource()

        self._neutronClient=NeutronClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._novaClient=NovaClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
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
            self._keystoneClient.setAccountImageQuota(500,100,project_id)
            self._keystoneClient.setAccountNetworkQuota(project_id,100,100,100,100,100)
            self._keystoneClient.setInstanceStorageQuota(project_id,65535,100,1024000,100,100,327675)
            self._keystoneClient.setObjectStoreQuota(5497558138880,project_id)
        except Exception,e:
            self._logger.error('创建账号'+self._os_username+'失败!'+'\r\n'+e.message)
        self._accountResource.add_account(test_account)

        self._logger.info('初始化默认安全组资源'+DEFAULT_SECGROUP_NAME)
        default_secgroup = SecGroup()
        default_secgroup.name = DEFAULT_SECGROUP_NAME
        try:
            default_secgroup.id=self._neutronClient.getSecGroupId(DEFAULT_SECGROUP_NAME)
            # 将安全组tcp规则放开
            self._logger.info('开放安全组'+default_secgroup.name+'的tcp规则')
            self._neutronClient.addAllowTcpRule(default_secgroup.id)
        except Exception,e:
            self._logger.error('初始化安全组资源'+DEFAULT_SECGROUP_NAME+'失败!'+'\r\n'+e.message)
        self._accountResource.add_secgroup(default_secgroup)


        #账户加入外部网络
        self._logger.info('初始化外部网络资源' + ADMIN_FLOAT_NET_NAME)
        admin_float_net = AdminNet()
        admin_float_net.name = ADMIN_FLOAT_NET_NAME
        try:
            admin_float_net.id=self._neutronClient.getNetId(ADMIN_FLOAT_NET_NAME)
        except Exception,e:
            self._logger.error('初始化外部网络'+ADMIN_FLOAT_NET_NAME+'资源失败!'+'\r\n'+e.message)
        self._accountResource.add_adminNet(admin_float_net)

        #账户里加入云主机类型
        self._logger.info('初始化云主机规格资源'+FLAVOR_TYPE_NAME.__str__())
        for key in FLAVOR_TYPE_NAME:
            tmpflavor=Flavor()
            tmpflavor.type=key
            tmpflavor.name=FLAVOR_TYPE_NAME[key]
            try:
                tmpflavor.id=self._novaClient.getFlavorId(tmpflavor.name)
            except Exception, e:
                self._logger.error('初始化云主机规格资源' + FLAVOR_TYPE_NAME.__str__() + '失败!' + '\r\n' + e.message)
            self._accountResource.add_flavor(tmpflavor)

        #账户里加入镜像
        self._logger.info('初始化测试镜像资源' + TEST_IMAGE_NAME)
        test_image = Image()
        test_image.name = TEST_IMAGE_NAME
        try:
            test_image.id=self._novaClient.getImageId(TEST_IMAGE_NAME)
        except Exception,e:
            self._logger.error('初始化测试镜像资源'+TEST_IMAGE_NAME+'失败!'+'\r\n'+e.message)
        self._accountResource.add_image(test_image)

        #账户里加入磁盘类型
        self._logger.info('初始化磁盘类型资源'+VOLUME_TYPE_NAME.__str__())
        for key in VOLUME_TYPE_NAME:
            tmpvolumetype=VolumeType()
            tmpvolumetype.type=key
            tmpvolumetype.name=VOLUME_TYPE_NAME[key]
            try:
                tmpvolumetype.id=self._cinderClient.getVolumeTypeId(VOLUME_TYPE_NAME[key])
            except Exception, e:
                self._logger.error('初始化磁盘类型资源' + VOLUME_TYPE_NAME.__str__() + '失败!' + '\r\n' + e.message)
            self._accountResource.add_volumeType(tmpvolumetype)

        #账户里加入可用域
        self._logger.info('初始化可用域资源')
        self._accountResource.add_zone(ZONE_NAMES)

        return self._accountResource

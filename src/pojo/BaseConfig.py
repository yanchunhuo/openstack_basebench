# -*- coding:utf8 -*-
class BaseConfig:
    def __init__(self):
        self.admin_os_tenant_name=None
        self.admin_os_project_name=None
        self.admin_os_username=None
        self.admin_os_password=None
        self.os_auth_url=None
        self.default_secgroup_name=None
        self.admin_float_net_name=None
        self.float_ip_qos=None
        self.volume_type_names=None
        self.test_image_name=None
        self.flavor_type_names=None
        self.zone_names=None
        self.compute_user_name=None
        self.compute_user_password=None

    @property
    def admin_os_tenant_name(self):
        return self.admin_os_tenant_name

    @admin_os_tenant_name.setter
    def admin_os_tenant_name(self,admin_os_tenant_name):
        self.admin_os_tenant_name=admin_os_tenant_name

    @property
    def admin_os_project_name(self):
        return self.admin_os_project_name

    @admin_os_project_name.setter
    def admin_os_project_name(self,admin_os_project_name):
        self.admin_os_project_name=admin_os_project_name

    @property
    def admin_os_username(self):
        return self.admin_os_username

    @admin_os_username.setter
    def admin_os_username(self,admin_os_username):
        self.admin_os_username=admin_os_username

    @property
    def admin_os_password(self):
        return self.admin_os_password

    @admin_os_password.setter
    def admin_os_password(self,admin_os_password):
        self.admin_os_password=admin_os_password

    @property
    def os_auth_url(self):
        return self.os_auth_url

    @os_auth_url.setter
    def os_auth_url(self,os_auth_url):
        self.os_auth_url=os_auth_url

    @property
    def default_secgroup_name(self):
        return self.default_secgroup_name

    @default_secgroup_name.setter
    def default_secgroup_name(self,default_secgroup_name):
        self.default_secgroup_name=default_secgroup_name

    @property
    def admin_float_net_name(self):
        return self.admin_float_net_name

    @admin_float_net_name.setter
    def admin_float_net_name(self,admin_float_net_name):
        self.admin_float_net_name=admin_float_net_name

    @property
    def float_ip_qos(self):
        return self.float_ip_qos

    @float_ip_qos.setter
    def float_ip_qos(self,float_ip_qos):
        self.float_ip_qos=float_ip_qos

    @property
    def volume_type_names(self):
        return self.volume_type_names

    @volume_type_names.setter
    def volume_type_names(self,volume_type_names):
        self.volume_type_names=volume_type_names


    @property
    def test_image_name(self):
        return self.test_image_name

    @test_image_name.setter
    def test_image_name(self,test_image_name):
        self.test_image_name=test_image_name

    @property
    def flavor_type_names(self):
        return self.flavor_type_names

    @flavor_type_names.setter
    def flavor_type_names(self,flavor_type_names):
        self.flavor_type_names=flavor_type_names

    @property
    def zone_names(self):
        return self.zone_names

    @zone_names.setter
    def zone_names(self,zone_names):
        self.zone_names=zone_names

    @property
    def compute_user_name(self):
        return self.compute_user_name

    @compute_user_name.setter
    def compute_user_name(self,compute_user_name):
        self.compute_user_name=compute_user_name

    @property
    def compute_user_password(self):
        return self.compute_user_password

    @compute_user_password.setter
    def compute_user_password(self,compute_user_password):
        self.compute_user_password=compute_user_password
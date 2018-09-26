#!-*- coding:utf8 -*-

class Account:
    def __init__(self):
        self.os_tenant_name=None
        self.os_project_name=None
        self.os_project_id=None
        self.os_username=None
        self.os_userid=None
        self.os_password=None

    @property
    def os_tenant_name(self):
        return self.os_tenant_name

    @os_tenant_name.setter
    def os_tenant_name(self,os_tenant_name):
        self.os_tenant_name=os_tenant_name

    @property
    def os_project_name(self):
        return self.os_project_name

    @os_project_name.setter
    def os_project_name(self, os_project_name):
        self.os_project_name = os_project_name

    @property
    def os_password(self):
        return self.os_password

    @os_password.setter
    def os_password(self, os_password):
        self.os_password = os_password

    @property
    def os_username(self):
        return self.os_username

    @os_username.setter
    def os_username(self, os_username):
        self.os_username = os_username

    @property
    def os_project_id(self):
        return self.os_project_id

    @os_project_id.setter
    def os_project_id(self,os_project_id):
        self.os_project_id=os_project_id

    @property
    def os_userid(self):
        return self.os_userid

    @os_userid.setter
    def os_userid(self,os_userid):
        self.os_userid=os_userid

#!-*- coding:utf8 -*-
from src.readConfig import ReadConfig

class AuthTool:

    def __init__(self):
        self._readConfig=ReadConfig()
        self._os_auth_url=self._readConfig.base.os_auth_url
        self._admin_os_tenant_name = self._readConfig.base.admin_os_tenant_name
        self._admin_os_username = self._readConfig.base.admin_os_username
        self._admin_os_password = self._readConfig.base.admin_os_password

    def novaInsertAuth(self, str, os_project_name, os_username, os_password):
        """
        nova相关命令行加入授权信息
        :param str:
        :param os_project_name:
        :param os_username:
        :param os_password:
        :return:
        """
        return str.replace(" ",' --os-username ' + os_username + ' --os-project-name ' + os_project_name + ' --os-password ' + os_password + ' --os-auth-url ' + self._os_auth_url + ' ',1)

    def cinderInsertAuth(self, str, os_tenant_name,os_project_name, os_username, os_password):
        """
        nova相关命令行加入授权信息
        :param str:
        :param os_tenant_name:
        :param os_project_name:
        :param os_username:
        :param os_password:
        :return:
        """
        return str.replace(" ",' --os-tenant-name ' + os_tenant_name +' --os-username ' + os_username + ' --os-project-name ' + os_project_name + ' --os-password ' + os_password + ' --os-auth-url ' + self._os_auth_url + ' ',1)

    def neutronInsertAuth(self, str, os_project_name, os_username, os_password):
        """
        neutronInsertAuth相关命令行加入授权信息
        :param os_project_name:
        :param str:
        :param os_username:
        :param os_password:
        :return:
        """
        return str.replace(" ",
                           ' --os-username ' + os_username + ' --os-project-name ' + os_project_name + ' --os-password ' + os_password + ' --os-auth-url ' + self._os_auth_url + ' ',
                           1)

    def openstackInsertAuth(self, str, os_project_name, os_username, os_password):
        """
        openstackInsertAuth相关命令行加入授权信息
        :param str:
        :param os_project_name:
        :param os_username:
        :param os_password:
        :return:
        """
        return str.replace(" ",
                           ' --os-username ' + os_username + ' --os-project-name ' + os_project_name + ' --os-password ' + os_password + ' --os-auth-url ' + self._os_auth_url + ' ',
                           1)

    def heatInsertAuth(self, str, os_tenant_name, os_project_name, os_username, os_password):
        """
        heatInsertAuth相关命令行加入授权信息
        :param str:
        :param os_tenant_name:
        :param os_project_name:
        :param os_username:
        :param os_password:
        :return:
        """
        return str.replace(" ",
                           ' --os-tenant-name ' + os_tenant_name + ' --os-project-name ' + os_project_name + ' --os-username ' + os_username + ' --os-password ' + os_password + ' --os-auth-url ' + self._os_auth_url + ' ',
                           1)

    def troveInsertAuth(self, str, os_tenant_name, os_project_name, os_username, os_password):
        """
        heatInsertAuth相关命令行加入授权信息
        :param str:
        :param os_tenant_name:
        :param os_project_name:
        :param os_username:
        :param os_password:
        :return:
        """
        return str.replace(" ",
                           ' --os-tenant-name ' + os_tenant_name + ' --os-project-name ' + os_project_name + ' --os-username ' + os_username + ' --os-password ' + os_password + ' --os-auth-url ' + self._os_auth_url + ' ',
                           1)

    def insertAdminAuth(self, str):
        """
        加入admin授权信息
        :param str:
        :return:
        """
        return str.replace(" ",
                           ' --os-username ' + self._admin_os_username + ' --os-tenant-name ' + self._admin_os_tenant_name + ' --os-password ' + self._admin_os_password + ' --os-auth-url ' + self._os_auth_url + ' ',
                           1)
#!-*- coding:utf8 -*-
from src.clients.keystoneClient import KeystoneClient
from src.clients.openstackClient import OpenstackClient
from src.readConfig import ReadConfig

class DeleteAccounts:

    def __init__(self):
        self._readConfig=ReadConfig()
        self._os_tenant_name = self._readConfig.base.admin_os_tenant_name
        self._os_project_name = self._readConfig.base.admin_os_project_name
        self._os_username = self._readConfig.base.admin_os_username
        self._os_password = self._readConfig.base.admin_os_password
        self._keystoneClient = KeystoneClient()
        self._openstackClient = OpenstackClient(self._os_tenant_name, self._os_project_name, self._os_username,self._os_password)


    def deleteAccountwithFloatingips(self):
        """
        删除账户下及名下的浮动ip
        :return:
        """
        tmp_project_ids = self._keystoneClient.getProjectId(self._readConfig.tools.cleanup_keyword)
        if tmp_project_ids:
            project_ids = tmp_project_ids.split()
            for project_id in project_ids:
                floatingip_ids = self._openstackClient.getAccountfloatingipIds(project_id)
                self._openstackClient.deleteAllFloatIp(floatingip_ids)
            self._keystoneClient.delAccount(project_ids)
        return True

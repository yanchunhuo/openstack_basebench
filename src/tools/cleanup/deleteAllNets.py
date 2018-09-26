#!-*- coding:utf8 -*-
from src.clients.openstackClient import OpenstackClient
from src.readConfig import ReadConfig

class DeleteAllNets:
    def __init__(self,os_tenant_name,os_project_name,os_username,os_password):
        self._readConfig = ReadConfig()
        self._os_tenant_name=os_tenant_name
        self._os_project_name=os_project_name
        self._os_username=os_username
        self._os_password=os_password
        self._openstackClient = OpenstackClient(self._os_tenant_name, self._os_project_name, self._os_username,
                                              self._os_password)


    def deleteNet(self):
        """
        删除所有的网络
        :return:
        """
        tmp_net_ids = self._openstackClient.getNetId(self._readConfig.tools.cleanup_keyword)
        if tmp_net_ids:
            net_ids = tmp_net_ids.split()
            self._openstackClient.deleteAllNet(net_ids)
        return True
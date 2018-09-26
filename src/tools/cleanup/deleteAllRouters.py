#!-*- coding:utf8 -*-
from src.clients.openstackClient import OpenstackClient
from src.readConfig import ReadConfig

class DeleteAllRoutes:
    def __init__(self,os_tenant_name,os_project_name,os_username,os_password):
        self._readConfig = ReadConfig()
        self._os_tenant_name=os_tenant_name
        self._os_project_name=os_project_name
        self._os_username=os_username
        self._os_password=os_password
        self._openstackClient = OpenstackClient(self._os_tenant_name, self._os_project_name, self._os_username,
                                              self._os_password)

    def deleteRouters(self):
        """
        删除路由器
        :return:
        """
        tmp_router_ids = self._openstackClient.getRouterId(self._readConfig.tools.cleanup_keyword)
        if tmp_router_ids:
            router_ids = tmp_router_ids.split()
            self._openstackClient.deleteAllRouter(router_ids)
        return True
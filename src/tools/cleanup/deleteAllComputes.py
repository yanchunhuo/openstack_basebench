#!-*- coding:utf8 -*-
from src.clients.novaClient import NovaClient
from src.readConfig import ReadConfig

class DeleteAllComputes:
    def __init__(self,os_tenant_name,os_project_name,os_username,os_password):
        self._readConfig = ReadConfig()
        self._os_tenant_name=os_tenant_name
        self._os_project_name=os_project_name
        self._os_username=os_username
        self._os_password=os_password
        self._novaClient = NovaClient(self._os_project_name, self._os_username, self._os_password)

    def deleteComputes(self):
        """
        删除所有的云主机
        :return:
        """
        tmp_compute_ids = self._novaClient.getTenantsComputeId(self._readConfig.tools.cleanup_keyword)
        if tmp_compute_ids:
            compute_ids = tmp_compute_ids.split()
            self._novaClient.deleteAllCompute(compute_ids)
        return True

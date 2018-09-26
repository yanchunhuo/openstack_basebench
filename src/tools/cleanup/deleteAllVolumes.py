#!-*- coding:utf8 -*-
from src.clients.cinderClient import CinderClient
from src.readConfig import ReadConfig

class DeleteAllVolumes:
    def __init__(self,os_tenant_name,os_project_name,os_username,os_password):
        self._readConfig = ReadConfig()
        self._os_tenant_name=os_tenant_name
        self._os_project_name=os_project_name
        self._os_username=os_username
        self._os_password=os_password
        self._cinderClient = CinderClient(self._os_tenant_name, self._os_project_name, self._os_username,
                                          self._os_password)

    def deleteVolumes(self):
        """
        删除所有的云硬盘
        :return:
        """
        tmp_volume_ids = self._cinderClient.getVolumeId(self._readConfig.tools.cleanup_keyword)
        if tmp_volume_ids:
            volume_ids = tmp_volume_ids.split()
            self._cinderClient.deleteAllVolume(volume_ids)
        return True

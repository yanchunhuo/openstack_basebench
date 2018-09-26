#!-*- coding:utf8 -*-
from src.authTool import AuthTool
from src.timeoutThread.checkTroveDel import CheckTroveDel
from src.timeoutThread.checkTroveRunSucc import CheckTroveRunSucc
import subprocess


class TroveClient:
    def __init__(self,os_tenant_name,os_project_name,os_username,os_password):
        self._authTool=AuthTool()
        self._os_tenant_name=os_tenant_name
        self._os_project_name=os_project_name
        self._os_username=os_username
        self._os_password=os_password


    def _troveInertAuth(self, command):
        """
        trove相关命令行加入授权信息
        :param command:
        :return:
        """
        return self._authTool.troveInsertAuth(command, self._os_tenant_name, self._os_project_name, self._os_username,self._os_password)

    def createtrove(self, trove_name, flavor_id, trove_volume_size, database_name, user_name,user_password, net_id, zone_name, datastore_name, datastore_version_name):
        """
         创建数据库实例
        :param trove_name:
        :param flavor_id:
        :param trove_volume_size:
        :param database_name:
        :param user_name:
        :param user_password:
        :param net_id:
        :param zone_name:
        :param datastore_name:
        :param datastore_version_name:
        :return: trove_id
        """
        command = "trove create " + trove_name + " "+flavor_id+" --size " + trove_volume_size + " --databases " + database_name + " --users " + user_name + ":"+user_password + " --nic net-id=" + net_id + " --availability_zone " + zone_name + "  --datastore " + datastore_name + " --datastore_version " + datastore_version_name + "|grep -w id|awk -F '|' '{print $3}'"
        command = self._troveInertAuth(command)
        try:
            trove_id = subprocess.check_output(command, shell=True)
            trove_id = trove_id.strip()
            if not trove_id:
                return None
            self._is_trove_run_succ(trove_id)
            return trove_id
        except Exception:
            return None

    def _is_trove_run_succ(self,trove_id):
        """
        数据库实例创建60秒后是否处于运行中
        :param trove_id:
        :return:
        """
        command = "trove list|grep -i "+trove_id+"|awk -F '|' '{print $6}'"
        command = self._troveInertAuth(command)
        checkTroveRunSucc=CheckTroveRunSucc(trove_id,command)
        checkTroveRunSucc.start()
        checkTroveRunSucc.join(300)
        is_succ=checkTroveRunSucc.getIsSucc()
        if not is_succ:
            checkTroveRunSucc.setIsSucc(True)
            return False
        elif is_succ:
            return True

    def deleteAllTrove(self, trove_ids):
        """
        删除所有数据库实例
        :param trove_ids:
        :return:
        """
        if len(trove_ids) != 0:
            #不支持批量，一个一个删除
            for trove_id in trove_ids:
                del_command = "trove delete " + trove_id + ' '
                del_command = self._troveInertAuth(del_command)
                subprocess.check_output(del_command, shell=True)
                self._is_trove_del(trove_id)

    def _is_trove_del(self,trove_id):
        """
        检测账号下数据库实例是否全部删除
        :param trove_id:
        :return:
        """
        has_trove_command="trove list |grep -E '"+trove_id+"'|awk '{print $0}'"
        has_trove_command =self._troveInertAuth(has_trove_command)
        checkTroveDel=CheckTroveDel(trove_id,has_trove_command)
        checkTroveDel.start()
        checkTroveDel.join(60)
        is_succ=checkTroveDel.getIsSucc()
        if not is_succ:
            checkTroveDel.setIsSucc(True)
            return False
        elif is_succ:
            return True
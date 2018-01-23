#!-*- coding:utf8 -*-
from src import common
from src.timeoutThread.checkVolumeCreateSucc import CheckVolumeCreateSucc
from src.timeoutThread.checkAllVolumeDel import CheckAllVolumeDel
import subprocess

class CinderClient():
    def __init__(self,os_tenant_name,os_project_name,os_username,os_password):
        self._os_tenant_name=os_tenant_name
        self._os_project_name=os_project_name
        self._os_username=os_username
        self._os_password=os_password

    def _cinderInertAuth(self,command):
        """
        cinder命令加入授权信息
        :param command:
        :return:
        """
        return common.novaInsertAuth(command, self._os_tenant_name, self._os_project_name, self._os_username,self._os_password)

    def getVolumeTypeId(self,volume_type_name):
        """
        获得磁盘类型的id
        :param volume_type_name:
        :return:volume_type_id
        """
        command="cinder type-list |grep -i "+volume_type_name+"|awk -F '|' '{print $2}'"
        command=self._cinderInertAuth(command)
        volume_type_id=subprocess.check_output(command,shell=True)
        volume_type_id=volume_type_id.strip()
        if not volume_type_id:
            return None
        return volume_type_id

    def createVolume(self,volume_name,volume_type_id,volume_size):
        """
        volume_size：
        :param volume_name:
        :param volume_type_id:
        :param volume_size:单位为GB
        :return:volume_id
        """
        command="cinder create --name "+volume_name+" --volume-type "+volume_type_id+" "+str(volume_size)+"|grep -w id|awk -F '|' '{print $3}'"
        command=self._cinderInertAuth(command)
        volume_id=subprocess.check_output(command,shell=True)
        volume_id=volume_id.strip()
        self._is_volume_create_succ(volume_id)
        return volume_id

    def _is_volume_create_succ(self,volume_id):
        """
        每0.5秒判断一次云硬盘是否创建成功，30秒超时
        :param volume_id:
        :return:
        """
        command = "cinder list|grep -i " + volume_id.strip() + " |grep -i 'available'|awk '{print $0}'"
        command = self._cinderInertAuth(command)
        checkVolumeCreateSucc=CheckVolumeCreateSucc(volume_id,command)
        checkVolumeCreateSucc.start()
        checkVolumeCreateSucc.join(30)
        is_succ =checkVolumeCreateSucc.getIsSucc()
        if not is_succ:
            checkVolumeCreateSucc.setIsSucc(True)
            return False
        elif is_succ:
            return True

    def deleteAllVolume(self,volume_ids):
        """
        每0.5秒判断一次云硬盘是否创建成功，30秒超时
        :param volume_ids:
        :return:
        """
        if len(volume_ids) != 0:
            del_command = "cinder delete "
            for volume_id in volume_ids:
                del_command = del_command + volume_id + ' '
            del_command = self._cinderInertAuth(del_command)
            subprocess.check_output(del_command, shell=True)
            self._is_all_volume_del(volume_ids)
            return True

    def _is_all_volume_del(self,volume_ids):
        """
        检测账号云硬盘是否全部删除
        :param volume_ids:
        :return:
        """
        num=len(volume_ids)
        if num!=0:
            has_volume_command = "cinder list|grep -E '"
            for i,volume_id in enumerate(volume_ids):
                if i!=num-1:
                    has_volume_command=has_volume_command+volume_id+'|'
                else:
                    has_volume_command=has_volume_command+volume_id
            has_volume_command=has_volume_command+"'|awk '{print $0}'"
            has_volume_command =self._cinderInertAuth(has_volume_command)
            checkAllVolumeDel=CheckAllVolumeDel(volume_ids,has_volume_command)
            checkAllVolumeDel.start()
            checkAllVolumeDel.join(1800)
            is_succ=checkAllVolumeDel.getIsSucc()
            if not is_succ:
                checkAllVolumeDel.setIsSucc(True)
                return False
            elif is_succ:
                return True



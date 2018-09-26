#!-*- coding:utf8 -*-
from src.authTool import AuthTool
from src.timeoutThread.checkComputeRunSucc import CheckComputeRunSucc
from src.timeoutThread.checkAllComputeDel import CheckAllComputeDel
import subprocess

class NovaClient:
    def __init__(self,os_project_name,os_username,os_password):
        self._authTool=AuthTool()
        self._os_project_name=os_project_name
        self._os_username=os_username
        self._os_password=os_password

    def _novaInertAuth(self,command):
        """
        nova相关命令行加入授权信息
        :param command:
        :return:
        """
        return self._authTool.novaInsertAuth(command,self._os_project_name,self._os_username,self._os_password)

    def getImageId(self,image_name):
        """
        获得镜像id
        :param image_name:
        :return:image_id
        """
        command="nova image-list |grep -i "+image_name+"|awk -F '|' '{print$2}'"
        command=self._novaInertAuth(command)
        image_id=subprocess.check_output(command,shell=True)
        image_id = image_id.strip()
        if not image_id:
            return None
        return image_id

    def getFlavorId(self,flavor_name):
        """
        获得云主机规格id
        :param flavor_name:
        :return:flavor_id
        """
        command="nova flavor-list |grep -i "+flavor_name+"|awk -F '|' '{print $2}'"
        command=self._novaInertAuth(command)
        flavor_id=subprocess.check_output(command,shell=True)
        flavor_id=flavor_id.strip()
        if not flavor_id:
            return None
        return flavor_id

    def bootCompute(self,compute_name,flavor_id,image_id,net_id,secgroup_id,zone_name,user_data_file_path):
        """
        启动一台云主机，并绑定浮动ip
        :param compute_name:
        :param flavor_id:
        :param image_id:
        :param net_id:
        :param secgroup_id:
        :param zone_name:
        :param user_data_file_path:
        :return:compute_id
        """
        command="nova boot --flavor "+flavor_id+" --image "+image_id+" --security-groups "+secgroup_id+" --nic net-id="+net_id+" --availability-zone "+zone_name+"  --user-data "+user_data_file_path+" "+compute_name+"|grep -w id|awk -F '|' '{print $3}'"
        command=self._novaInertAuth(command)
        compute_id=subprocess.check_output(command,shell=True)
        compute_id = compute_id.strip()
        if not compute_id:
            return None
        self._is_compute_run_succ(compute_id)
        return compute_id

    def _is_compute_run_succ(self,compute_id):
        """
        云主机创建60秒后是否处于运行中
        :param compute_id:
        :return:
        """
        command = "nova list|grep -i "+compute_id+"|awk -F '|' '{print $4}'"
        command = self._novaInertAuth(command)
        checkComputeRunSucc=CheckComputeRunSucc(compute_id,command)
        checkComputeRunSucc.start()
        checkComputeRunSucc.join(120)
        is_succ=checkComputeRunSucc.getIsSucc()
        if not is_succ:
            checkComputeRunSucc.setIsSucc(True)
            return False
        elif is_succ:
            return True

    def getComputeId(self,compute_name):
        """
        获取云主机id
        :param compute_name:
        :return:compute_id
        """
        command = "nova list|grep -i "+compute_name+"|awk -F '|' '{print $2}'"
        command =self._novaInertAuth(command)
        compute_id = subprocess.check_output(command, shell=True)
        compute_id = compute_id.strip()
        if not compute_id:
            return None
        return compute_id

    def getTenantsComputeId(self,compute_name):
        """
        获取所有账户云主机id
        :param compute_name:
        :return:compute_id
        """
        command = "nova list --all-tenant|grep -i "+compute_name+"|awk -F '|' '{print $2}'"
        command =self._novaInertAuth(command)
        compute_id = subprocess.check_output(command, shell=True)
        compute_id = compute_id.strip()
        if not compute_id:
            return None
        return compute_id

    def getComputeFloatIp(self,compute_name):
        """
        获取云主机浮动ip
        :param compute_name:
        :return:float_ip
        """
        compute_id=self.getComputeId(compute_name)
        command="nova list |grep -i "+compute_id+"|awk -F '|' '{print $7}'|awk -F '=' '{print $2}'"
        command=self._novaInertAuth(command)
        float_ip=subprocess.check_output(command,shell=True)
        float_ip=float_ip.split(',')[-1]
        float_ip=float_ip.strip()
        if not float_ip:
            return None
        return float_ip

    def getComputeIp(self,compute_name):
        """
        获取云主机ip
        :param compute_name:
        :return:ip
        """
        compute_id=self.getComputeId(compute_name)
        command="nova list |grep -i "+compute_id+"|awk -F '|' '{print $7}'|awk -F '=' '{print $2}'"
        command=self._novaInertAuth(command)
        ip=subprocess.check_output(command,shell=True)
        ip=ip.split(',')[0]
        ip=ip.strip()
        if not ip:
            return None
        return ip

    def addFloatForCompute(self,compute_id,float_ip_address):
        """
        绑定浮动ip
        :param compute_id:
        :param float_ip_address:
        :return:
        """
        command = "nova floating-ip-associate "+compute_id+" "+float_ip_address
        command =self._novaInertAuth(command)
        subprocess.check_output(command, shell=True)
        return True

    def attachVolume(self,compute_id,volume_id,device_name):
        """
        挂载云硬盘
        :param compute_id:
        :param volume_id:
        :param device_name:
        :return:
        """
        command="nova volume-attach "+compute_id+' '+volume_id+' '+device_name
        command=self._novaInertAuth(command)
        subprocess.check_output(command,shell=True)
        return True

    def deleteAllCompute(self,compute_ids):
        """
        删除所有云主机
        :param compute_ids:
        :return:
        """
        if len(compute_ids)!=0:
            del_command="nova delete "
            for compute_id in compute_ids:
                del_command=del_command+compute_id+' '
            del_command=self._novaInertAuth(del_command)
            subprocess.check_output(del_command,shell=True)
            self._is_all_compute_del(compute_ids)
        return True

    def _is_all_compute_del(self,compute_ids):
        """
        检测云主机是否全部删除
        :param compute_ids:
        :return:
        """
        num=len(compute_ids)
        if num!=0:
            has_compute_command = "nova list |grep -E '"
            for i,compute_id in enumerate(compute_ids):
                if i!=num-1:
                    has_compute_command=has_compute_command+compute_id+"|"
                else:
                    has_compute_command=has_compute_command+compute_id
            has_compute_command=has_compute_command+"'|awk '{print $0}'"
            has_compute_command =self._novaInertAuth(has_compute_command)
            checkAllComputeDel=CheckAllComputeDel(compute_ids,has_compute_command)
            checkAllComputeDel.start()
            checkAllComputeDel.join(1800)
            is_succ=checkAllComputeDel.getIsSucc()
            if not is_succ:
                checkAllComputeDel.setIsSucc(True)
                return False
            elif is_succ:
                return True



#!-*- coding:utf8 -*-
import subprocess
from src import common
from src.logger import logger
from src.timeoutThread.checkAllHeatRunSucc import CheckAllHeatRunSucc
from src.timeoutThread.checkAllHeatDel import CheckAllHeatDel
from heat_template import *

class HeatClient():
    def __init__(self,os_tenant_name,os_project_name,os_username,os_password):
        self._os_tenant_name = os_tenant_name
        self._os_project_name = os_project_name
        self._os_username = os_username
        self._os_password = os_password

    def _heatInsertAuth(self,commad):
        return common.heatInsertAuth(commad,self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)

    def _dealTemplateFiles(self,net_id,net_CIDR,image_id,image_name,flavor_id,flavor_type_name,passwd,secGroup_id,max_computes,min_computes,alarm_type,max_alarmvalue,min_alarmvalue):
        """
        处理伸缩组2个模板
        :param net_id:
        :param net_CIDR:
        :param image_id:
        :param image_name:
        :param flavor_id:
        :param flavor_type_name:
        :param passwd:
        :param secGroup_id:
        :param max_computes:
        :param min_computes:
        :param alarm_type: 可选值有cpu_util和memory.usage
        :param max_alarmvalue: 范围为（1，100）
        :param min_alarmvalue: 范围为（1，100）
        :return:
        """
        with open('heat_template/heat_old.yaml','r+') as heat_f,open('heat_template/lb_server_old.yaml','r+') as lb_f:
            heat_new_f = open('heat_template/heat_new.yaml','w+')
            lb_new_f = open('heat_template/lb_server.yaml','w+')
            soure_heat_text = heat_f.read()
            soure_lb_text = lb_f.read()
            #替换字符串
            resulte_heat_text = soure_heat_text.replace("net_id",net_id).replace('net_CIDR',net_CIDR).replace("image_id",image_id).replace('images_name',image_name).replace("flavorid",flavor_id).\
                     replace('passwd',passwd).replace('secGroup_id',secGroup_id).replace('flavor_type',flavor_type_name).replace('max_computes',max_computes).replace('min_computes',min_computes).\
                replace('alarm_type',alarm_type).replace('max_alarmvalue',max_alarmvalue).replace('min_alarmvalue',min_alarmvalue)

            resulte_lb_text = soure_lb_text.replace("net_id", net_id).replace("image_id", image_id).replace("flavorid", flavor_id).\
                             replace('passwd', passwd).replace('secGroup_id',secGroup_id)
            heat_f.seek(0,0)
            lb_f.seek(0, 0)

            heat_new_f.write(resulte_heat_text)
            lb_new_f.write(resulte_lb_text)

            heat_f.close()
            heat_new_f.close()
            lb_f.close()
            lb_new_f.close()

    def creatHeat(self,net_id,net_CIDR,image_id,image_name,flavor_id,flavor_type,passwd,secGroup_id,max_computes,min_computes,alarm_type,max_alarmvalue,min_alarmvalue,heat_templatepath,heat_name):
        """
        创建伸缩组
        :param net_id:
        :param net_CIDR:
        :param image_id:
        :param image_name:
        :param flavor_id:
        :param flavor_type:
        :param passwd:
        :param secGroup_id:
        :param max_computes:
        :param min_computes:
        :param alarm_type: 可选值有cpu_util和memory.usage
        :param max_alarmvalue: 范围为（1，100）
        :param min_alarmvalue: 范围为（1，100）
        :param heat_templatepath:新模板的路径
        :param heat_name:
        :return:
        """
        logger.info('创建一个自动伸缩组'+ heat_name)
        self._dealTemplateFiles(net_id,
                                net_CIDR,
                                image_id,
                                image_name,
                                flavor_id,
                                flavor_type,
                                passwd,
                                secGroup_id,
                                max_computes,
                                min_computes,
                                alarm_type,
                                max_alarmvalue,
                                min_alarmvalue)
        commad = "heat stack-create -f" + heat_templatepath + " "+ heat_name + "| grep -i "+heat_name+ "| awk -F '|' '{print$2}'"
        commad = self._heatInsertAuth(commad)
        try:
            heat_id = subprocess.check_output(commad, shell=True)
            heat_id = heat_id.strip()
            if not heat_id:
                logger.error('创建一个自动伸缩组' + heat_name + '失败')
                return None
            self._is_heat_run_succ(heat_id)
            return heat_id
        except Exception,e:
            logger.error('创建一个自动伸缩组'+ heat_name + '失败'+'\r\n'+e.message)
            return None


    def _is_heat_run_succ(self,heat_id):
        """
        伸缩组创建60s后是否处于运行状态
        :param heat_id:
        :return:
        """
        logger.info('检测伸缩组'+ heat_id + '运行状态...')
        commad = "heat stack-list| grep -i "+ heat_id + "| awk -F '|' '{print $4}'"
        commad = self._heatInsertAuth(commad)
        checkHeatRunSucc = CheckAllHeatRunSucc(heat_id,commad)
        checkHeatRunSucc.start()
        checkHeatRunSucc.join(60)
        is_succ = checkHeatRunSucc.getIsSucc()
        if not is_succ:
            logger.error('伸缩组' + heat_id +'60s未处于运行状态')
            checkHeatRunSucc.setIsSucc(True)
        elif is_succ:
            return True


    def deleteAllHeat(self,heat_ids):
        """
        删除伸缩组
        :param heat_ids:
        :return:
        """
        logger.info('删除伸缩组'+ heat_ids.__str__())
        if len(heat_ids) != 0:
            del_commad = "heat stack-delete "
            for id in heat_ids:
                del_commad = del_commad + id + ' '
            del_commad = self._heatInsertAuth(del_commad)
            try:
                subprocess.check_output(del_commad,shell=True)
                self._is_del_all_heat(heat_ids)
                return True
            except Exception,e:
                logger.error("删除伸缩组失败" + heat_ids.__str__() +'\r\n'+e.message)
                return False

    def _is_del_all_heat(self,heat_ids):
        """
        检测账号下伸缩组是否全部删除
        :param heat_ids:
        :return:
        """
        logger.info('检测伸缩组:' + heat_ids.__str__() + '是否已全部删除完成')
        num = len(heat_ids)
        if num != 0:
            has_heat_command = "heat stack-list |grep -E '"
            for i, heat_id in enumerate(heat_ids):
                if i != num - 1:
                    has_heat_command = has_heat_command + heat_id + "|"
                else:
                    has_heat_command = has_heat_command + heat_id
            has_heat_command = has_heat_command + "'|awk '{print $0}'"
            has_heat_command = self._heatInsertAuth(has_heat_command)
            checkHeatDel = CheckAllHeatDel(heat_ids,command=has_heat_command)
            checkHeatDel.start()
            checkHeatDel.join(1800)
            is_succ = checkHeatDel.getIsSucc()
            if not is_succ:
                logger.error('删除所有伸缩组'+ heat_ids.__str__() + '1800秒后未完全删除'+ '\r\n')
                checkHeatDel.setIsSucc(True)
                return False
            elif is_succ:
                return True





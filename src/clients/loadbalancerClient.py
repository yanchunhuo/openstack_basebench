#!-*- coding:utf8 -*-
import subprocess
from src import common

class LoadbalancerClient():
    def __init__(self, os_tenant_name, os_project_name, os_username, os_password):
        self._os_tenant_name = os_tenant_name
        self._os_project_name = os_project_name
        self._os_username = os_username
        self._os_password = os_password


    def _neutronInsertAuth(self,command):
        return common.neutronInsertAuth(command,self._os_tenant_name,self._os_username,self._os_password)


    def createLoadbalancer(self, lb_name, floatingip_id, subnet_id, connection_limit, protocol, protocol_port, lb_algorithmt,
                           delay_time, max_retries, timeout, protocol_type, instance_ips_weight):
        """
        创建负载均衡器
        :param lb_name:
        :param floatingip_id:
        :param subnet_id:
        :param connection_limit: 最大连接数，可选5000,10000,20000
        :param protocol: 协议,可选HTTP、TCP
        :param protocol_port: 端口，范围1-65535
        :param lb_algorithmt: 负载均衡方式，可选ROUND_ROBIN,LEAST_CONNECTIONS,SOURCE_IP
        :param delay_time: 间隔时间，范围2-60
        :param max_retries: 尝试次数，范围1-10
        :param timeout: 超时时间，范围5-300
        :param protocol_type: 健康检查方式，可选PING、HTTP
        :param instance_ips_weight: 数组[云主机ip,weight],weight范围1-10
        :return: loadbalancer_id
        """
        command = "neutron lbaas-loadbalancer-create --name " + lb_name + " --floatingip_id " + floatingip_id + " -f json"
        command = self._neutronInsertAuth(command)
        loadbalancer_id = subprocess.check_output(command, shell=True)
        loadbalancer_id = common.getStringWithLBRB(loadbalancer_id, '{"Field": "id", "Value": "', '"}')
        loadbalancer_id = loadbalancer_id.strip()
        if not loadbalancer_id:
            return None
        self._addInterfaceForLoadbalancer(loadbalancer_id, subnet_id)
        listener_id = self._addListenerForLoadbalancer(lb_name, loadbalancer_id, connection_limit, protocol, protocol_port)
        pool_id = self._addPoolForLoadbalancer(lb_name, listener_id, protocol, lb_algorithmt)
        self._addHealthmonitorForLoadbalancer(delay_time, max_retries, timeout, protocol_type, pool_id)
        for instance_ip_weight in instance_ips_weight:
            self.addMemberForLoadbalancer(subnet_id, instance_ip_weight[0], protocol_port, instance_ip_weight[1], pool_id)
        return loadbalancer_id


    def _addInterfaceForLoadbalancer(self,loadbalancer_id, subnet_id):
        """
        为负载均衡器添加内网接口
        :param loadbalancer_id:
        :param subnet_id:
        :return:
        """
        command = "neutron lbaas-loadbalancer-interface-add " + loadbalancer_id + " " + subnet_id + " -f json"
        command = self._neutronInsertAuth(command)
        subprocess.check_output(command, shell=True)
        return True

    def _addListenerForLoadbalancer(self, listener_name, loadbalancer_id, connection_limit, protocol, protocol_port):
        """
        为负载均衡器创建监听器
        :param listener_name:
        :param loadbalancer_id:
        :param connection_limit:
        :param protocol:
        :param protocol_port:
        :return: listener_id
        """
        command = "neutron lbaas-listener-create --name " + listener_name + " --loadbalancer " + loadbalancer_id + " --connection_limit "\
                  + connection_limit + " --protocol " + protocol + " --protocol-port " + protocol_port + " -f json"
        command = self._neutronInsertAuth(command)
        listener_id = subprocess.check_output(command, shell=True)
        listener_id = common.getStringWithLBRB(listener_id, '{"Field": "id", "Value": "', '"}')
        listener_id = listener_id.strip()
        if not listener_id:
            return None
        return listener_id

    def _addPoolForLoadbalancer(self, pool_name, listener_id, protocol, lb_algorithmt):
        """
        为负载均衡器创建pool
        :param pool_name:
        :param listener_id:
        :param protocol:
        :param lb_algorithmt:
        :return: pool_id
        """
        command = "neutron lbaas-pool-create --name " + pool_name + " --listener " + listener_id + " --protocol " + protocol\
                  + " --lb-algorithm " + lb_algorithmt + " -f json"
        command = self._neutronInsertAuth(command)
        pool_id = subprocess.check_output(command, shell=True)
        pool_id = common.getStringWithLBRB(pool_id, '{"Field": "id", "Value": "', '"}')
        pool_id = pool_id.strip()
        if not pool_id:
            return None
        return pool_id

    def _addHealthmonitorForLoadbalancer(self, delay_time, max_retries, timeout, protocol_type, pool_id):
        """
        为负载均衡器创建健康检测器
        :param delay_time:
        :param max_retries:
        :param timeout:
        :param protocol_type:
        :param pool_id:
        :return: healthmonitor_id
        """
        command = "neutron lbaas-healthmonitor-create --delay " + delay_time + " --max-retries " + max_retries + " --timeout " + timeout\
                  + " --type " + protocol_type + " --pool  " + pool_id  + " -f json"
        command = self._neutronInsertAuth(command)
        subprocess.check_output(command, shell=True)
        return True

    def addMemberForLoadbalancer(self, subnet_id, instance_ip, protocol_port, weight, pool_id):
        """
        为负载均衡器添加后端服务器
        :param subnet_id:
        :param instance_ip:
        :param protocol_port:
        :param weight:
        :param pool_id:
        :return:
        """
        command = "neutron lbaas-member-create --subnet " + subnet_id + " --address " + str(instance_ip) + " --protocol-port " + str(protocol_port)\
                  + " --weight " + str(weight) + " " + pool_id + " -f json"
        command = self._neutronInsertAuth(command)
        subprocess.check_output(command, shell=True)
        return True

    def _getListenerId(self, loadbalancer_id):
        """
        获取负载均衡器listenerid
        :param loadbalancer_id:
        :return: listener_id
        """
        command = "neutron lbaas-loadbalancer-show " + loadbalancer_id + " -f json"
        command = self._neutronInsertAuth(command)
        tmp_listener_id = subprocess.check_output(command, shell=True)
        tmp_listener_id = common.getStringWithLBRB(tmp_listener_id, '{"Field": "listeners", "Value": "{\\\\"id\\\\": \\\\"', '\\\\"}')
        listener_id = tmp_listener_id.strip()
        if not listener_id:
            return None
        return listener_id

    def _getPoolId(self, listener_id):
        """
        获取所有负载均衡器池id
        :param listener_id:
        :return: pool_id
        """
        command = "neutron lbaas-listener-show " + listener_id + " -f json"
        command = self._neutronInsertAuth(command)
        tmp_pool_id = subprocess.check_output(command, shell=True)
        tmp_pool_id = common.getStringWithLBRB(tmp_pool_id, '{"Field": "default_pool_id", "Value": "', '"}')
        pool_id = tmp_pool_id.strip()
        if not pool_id:
            return None
        return pool_id

    def _getHealthmonitorId(self, pool_id):
        """
        获取所有负载均衡器健康检测器id
        :param pool_id:
        :return: healthmonitor_id
        """
        command = "neutron lbaas-pool-show " + pool_id + " -f json"
        command = self._neutronInsertAuth(command)
        tmp_healthmonitor_id = subprocess.check_output(command, shell=True)
        tmp_healthmonitor_id = common.getStringWithLBRB(tmp_healthmonitor_id, '{"Field": "healthmonitor_id", "Value": "', '"}')
        healthmonitor_id = tmp_healthmonitor_id.strip()
        if not healthmonitor_id:
            return None
        return healthmonitor_id

    def _getMemberId(self, pool_id):
        """
        获取所有负载均衡器后端服务器id
        :param pool_id:
        :return: member_ids
        """
        command = "neutron lbaas-pool-show " + pool_id + " -f json"
        command = self._neutronInsertAuth(command)
        tmp_member_ids = subprocess.check_output(command, shell=True)
        tmp_member_ids = common.getStringWithLBRB(tmp_member_ids, '{"Field": "members", "Value": "', '"}')
        member_ids=[]
        if not tmp_member_ids.strip():
            return member_ids
        member_ids = tmp_member_ids.split('\\n')
        return member_ids

    def _deleteMember(self, pool_id):
        """
        删除负载均衡器中的后端服务器
        :param pool_id:
        :return:
        """
        member_ids = self._getMemberId(pool_id)
        if len(member_ids[0]) != 0:
            for member_id in member_ids:
                del_member_command = "neutron lbaas-member-delete " + member_id + " " + pool_id
                del_member_command = self._neutronInsertAuth(del_member_command)
                subprocess.check_output(del_member_command, shell=True)
                return True

    def _deleteHealthmonitor(self, healthmonitor_id):
        """
        删除负载均衡器中的healthmonitor
        :param healthmonitor_id:
        :return:
        """
        del_healthmonitor_command = "neutron lbaas-healthmonitor-delete " + healthmonitor_id
        del_healthmonitor_command = self._neutronInsertAuth(del_healthmonitor_command)
        subprocess.check_output(del_healthmonitor_command, shell=True)
        return True

    def _deletePool(self, pool_id):
        """
        删除负载均衡器中的pool
        :param pool_id:
        :return:
        """
        del_pool_command = "neutron lbaas-pool-delete " + pool_id
        del_pool_command = self._neutronInsertAuth(del_pool_command)
        subprocess.check_output(del_pool_command, shell=True)
        return True

    def _deleteListener(self, listener_id):
        """
        删除负载均衡器中的listener
        :param listener_id:
        :return:
        """
        del_listener_command = "neutron lbaas-listener-delete " + listener_id
        del_listener_command = self._neutronInsertAuth(del_listener_command)
        subprocess.check_output(del_listener_command, shell=True)
        return True

    def deleteLoadbalancer(self,loadbalancer_ids):
        """
        删除账号下所有负载均衡器
        :param loadbalancer_ids:
        :return:
        """
        if len(loadbalancer_ids) != 0:
            for loadbalancer_id in loadbalancer_ids:
                loadbalancer_id=loadbalancer_id.encode('utf-8')
                del_loadbalancer_command = "neutron lbaas-loadbalancer-delete " + loadbalancer_id
                del_loadbalancer_command = self._neutronInsertAuth(del_loadbalancer_command)
                # 先删除member、healthmonitor、pool、listener再来删除负载均衡器
                listener_id = self._getListenerId(loadbalancer_id)
                pool_id = self._getPoolId(listener_id)
                healthmonitor_id = self._getHealthmonitorId(pool_id)
                self._deleteMember(pool_id)
                self._deleteHealthmonitor(healthmonitor_id)
                self._deletePool(pool_id)
                self._deleteListener(listener_id)
                subprocess.check_output(del_loadbalancer_command, shell=True)
            return True

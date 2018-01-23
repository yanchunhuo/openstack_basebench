#!-*- coding:utf8 -*-
import subprocess
from src import common
class NeutronClient():
    def __init__(self,os_tenant_name,os_project_name,os_username,os_password):
        self._os_tenant_name=os_tenant_name
        self._os_project_name=os_project_name
        self._os_username=os_username
        self._os_password=os_password

    def _neutronInsertAuth(self,command):
        return common.neutronInsertAuth(command,self._os_tenant_name,self._os_username,self._os_password)

    def getSecGroupId(self,secGroup_name):
        """
        得到安全组的id
        :param secGroup_name:
        :return:secGroup_id
        """
        command="neutron security-group-list |grep -i "+secGroup_name+"|awk -F '|' '{print $2}'"
        command=self._neutronInsertAuth(command)
        secGroup_id=subprocess.check_output(command,shell=True)
        secGroup_id=secGroup_id.strip()
        if not secGroup_id:
            return None
        return secGroup_id

    def addAllowTcpRule(self,secGroupId):
        """
        放开tcp 1-65535
        :param secGroupId:
        :return:
        """
        #检测是否有已开放tcp的1-65535端口
        check_command="neutron security-group-show "+secGroupId+"|grep -i 65535|awk {'print $0'}"
        check_command=self._neutronInsertAuth(check_command)
        has_tcp_65535=subprocess.check_output(check_command,shell=True)
        if has_tcp_65535:
            return True
        #放开安全组的tcp的１-65535端口
        command="neutron security-group-rule-create --protocol tcp --port-range-min 1 --port-range-max 65535  "+secGroupId
        command=self._neutronInsertAuth(command)
        subprocess.check_output(command,shell=True)
        return True

    def createNetwork(self,net_name,sub_net_cidr):
        """
        创建一个网络，并设置子网
        :param net_name:
        :param sub_net_cidr:
        :return:net_id
        """
        command="neutron net-create "+net_name+" -f json"
        command = self._neutronInsertAuth(command)
        result=subprocess.check_output(command,shell=True)
        net_id=common.getStringWithLBRB(result,'{"Field": "id", "Value": "','"}')
        net_id=net_id.strip()
        if not net_id:
            return None
        self._createSubnetForNet(net_id,sub_net_cidr)
        return net_id

    def _createSubnetForNet(self,net_id,sub_net_cidr):
        """
        为网络创建子网
        :param net_id:
        :param sub_net_cidr:
        :return:
        """
        command="neutron subnet-create "+net_id+" "+sub_net_cidr+ " -f json"
        command=self._neutronInsertAuth(command)
        subprocess.check_output(command,shell=True)

    def getNetId(self,net_name):
        """
        得到网络的id
        :param net_name:
        :return:net_id
        """
        command="neutron net-list|grep -i "+net_name+"|awk -F '|' '{print $2}'"
        command=self._neutronInsertAuth(command)
        net_id=subprocess.check_output(command,shell=True)
        net_id=net_id.strip()
        if not net_id:
            return None
        return  net_id

    def getSubNetId(self,net_id):
        """
        获得网络的子网id
        :param net_id: 
        :return:subnet_id
        """
        command="neutron net-show "+net_id+"|grep -i subnets|awk -F '|' '{print $3}'"
        command=self._neutronInsertAuth(command)
        subnet_id=subprocess.check_output(command,shell=True)
        subnet_id=subnet_id.strip()
        if not subnet_id:
            return None
        return subnet_id

    def setRouterGW(self,router_id,admin_float_net_id):
        """
        设置路由器的网关
        :param router_id:
        :param admin_float_net_id:
        :return:
        """
        command="neutron router-gateway-set "+router_id+" "+admin_float_net_id
        command=self._neutronInsertAuth(command)
        subprocess.check_output(command,shell=True)

    def createRouter(self,router_name,admin_float_net_id):
        """
        创建一个路由并设置网关
        :param router_name:
        :param admin_float_net_id:
        :return:route_id
        """
        command="neutron router-create "+router_name+" -f json"
        command=self._neutronInsertAuth(command)
        result=subprocess.check_output(command,shell=True)
        route_id=common.getStringWithLBRB(result,'{"Field": "id", "Value": "','"}')
        route_id=route_id.strip()
        if not route_id:
            return None
        self.setRouterGW(route_id, admin_float_net_id)
        return route_id

    def addRouterInterface(self,router_id,sub_net_id):
        """
        将接口绑定到路由器
        :param router_id:
        :param sub_net_id:
        :return:
        """
        command="neutron router-interface-add "+router_id+" "+sub_net_id
        command=self._neutronInsertAuth(command)
        subprocess.check_output(command,shell=True)

    def _getRouterInterface(self,router_id):
        """
        获得路由器的接口子网id
        :param router_id:
        :return: subnet_ids
        """
        command='neutron router-port-list '+router_id+' -f json'
        command=self._neutronInsertAuth(command)
        tmp_subnet_ids=subprocess.check_output(command,shell=True)
        subnet_ids=common.getStringWithLBRB(tmp_subnet_ids,'subnet_id\\\\": \\\\"','\\\\",','all')
        return subnet_ids

    def getFloatIp(self,admin_float_net_id,floating_ip_qos=200):
        """
        申请一个浮动ip
        :param admin_float_net_name:
        :param floating_ip_qos:
        :return: ip_address
        """
        command="neutron floatingip-create --floating-ip-qos "+str(floating_ip_qos)+" "+admin_float_net_id+"|grep -i floating_ip_address|awk -F '|' '{print $3}'"
        command=self._neutronInsertAuth(command)
        ip_address=subprocess.check_output(command,shell=True)
        ip_address=ip_address.strip()
        if not ip_address:
            return None
        return ip_address

    def getFloatId(self,float_ip_address):
        """
        :param float_ip_address:
        :return:
        """
        command="neutron floatingip-list |grep -i "+float_ip_address+"|awk -F '|' '{print $2}'"
        command=self._neutronInsertAuth(command)
        ip_id=subprocess.check_output(command,shell=True)
        ip_id=ip_id.strip()
        return ip_id

    def deleteAllNet(self,net_ids):
        """
        删除所有的网络
        :param net_ids:
        :return:
        """
        if len(net_ids) != 0:
            #不支持批量，一个一个删除
            for net_id in net_ids:
                del_command = "neutron net-delete "+net_id
                del_command = self._neutronInsertAuth(del_command)
                subprocess.check_output(del_command, shell=True)
        return True

    def _delete_router_interface(self,router_id,sub_net_id):
        """
        删除路由器接口
        :param router_id:
        :param sub_net_id:
        :return:
        """
        command="neutron router-interface-delete "+router_id+' '+sub_net_id
        command=self._neutronInsertAuth(command)
        subprocess.check_output(command,shell=True)
        return True

    def deleteAllRouter(self,router_ids):
        """
        删除路由器
        :param router_ids:
        :return:
        """
        # 删除路由器，只能单个单个删除
        if len(router_ids) != 0:
            for router_id in router_ids:
                router_id=router_id.encode('utf-8')
                del_router_command = "neutron router-delete "+router_id
                #先删除端口才能进行删除路由器
                router_subnet_ids=self._getRouterInterface(router_id)
                if router_subnet_ids:
                    if len(router_subnet_ids)!=0:
                        for subnet_id in router_subnet_ids:
                            self._delete_router_interface(router_id,subnet_id)
                #删除路由器
                del_router_command = self._neutronInsertAuth(del_router_command)
                subprocess.check_output(del_router_command, shell=True)
                return True

    def deleteAllFloatIp(self,floatIp_ids):
        """
        删除浮动ip
        :param floatIp_ids:
        :return:
        """
        # 删除浮动ip，只能单个单个删除
        if len(floatIp_ids) != 0:
            for floatIp_id in floatIp_ids:
                floatIp_id=floatIp_id.encode('utf-8')
                del_floatIp_command = "neutron floatingip-delete "+floatIp_id
                #删除浮动ip
                del_floatIp_command = self._neutronInsertAuth(del_floatIp_command)
                subprocess.check_output(del_floatIp_command, shell=True)
        return True
#!-*- coding:utf8 -*-
from src.authTool import AuthTool
from src.common.strTool import StrTool
import subprocess

class OpenstackClient:
    def __init__(self,os_tenant_name,os_project_name,os_username,os_password):
        self._authTool=AuthTool()
        self._os_tenant_name=os_tenant_name
        self._os_project_name=os_project_name
        self._os_username=os_username
        self._os_password=os_password

    def _openstackInsertAuth(self,command):
        return self._authTool.openstackInsertAuth(command,self._os_project_name,self._os_username,self._os_password)

    def getSecGroupId(self,secGroup_name):
        """
        得到安全组的id
        :param secGroup_name:
        :return:secGroup_id
        """
        command="openstack security group list |grep -i "+secGroup_name+"|awk -F '|' '{print $2}'"
        command=self._openstackInsertAuth(command)
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
        check_command="openstack security group show "+secGroupId+"|grep -i \"direction='ingress'\"|grep -i \"port_range_max='65535', port_range_min='1', protocol='tcp', remote_ip_prefix='0.0.0.0/0'\"|awk {'print $0'}"
        check_command=self._openstackInsertAuth(check_command)
        has_tcp_65535=subprocess.check_output(check_command,shell=True)
        if has_tcp_65535:
            return True
        #放开安全组的tcp的１-65535端口
        command="openstack security group rule create --protocol tcp --ingress --remote-ip 0.0.0.0/0 --dst-port 1:65535 "+secGroupId
        command=self._openstackInsertAuth(command)
        subprocess.check_output(command,shell=True)
        return True

    def addAllowIcmpRule(self,secGroupId):
        """
        放开icmp
        :param secGroupId:
        :return:
        """
        #检测是否有已开放icmp端口
        check_command="openstack security group show "+secGroupId+"|grep -i \"direction='ingress'\"|grep -i \"protocol='icmp'\"|awk {'print $0'}"
        check_command=self._openstackInsertAuth(check_command)
        has_icmp=subprocess.check_output(check_command,shell=True)
        if has_icmp:
            return True
        #放开安全组的icmp的所有端口
        command="openstack security group rule create --protocol icmp --ingress --remote-ip 0.0.0.0/0 "+secGroupId
        command=self._openstackInsertAuth(command)
        subprocess.check_output(command,shell=True)
        return True

    def createNetwork(self,net_name,sub_net_cidr):
        """
        创建一个网络，并设置子网
        :param net_name:
        :param sub_net_cidr:
        :return:net_id
        """
        command="openstack network create "+net_name+"|grep -i \"| id\"|awk -F '|' '{print $3}'"
        command = self._openstackInsertAuth(command)
        net_id=subprocess.check_output(command,shell=True)
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
        command="openstack subnet create --subnet-range "+sub_net_cidr+" --network "+net_id+" mysubnet"
        command=self._openstackInsertAuth(command)
        subprocess.check_output(command,shell=True)
        return True

    def getNetId(self,net_name):
        """
        得到网络的id
        :param net_name:
        :return:net_id
        """
        command="openstack network list|grep -i "+net_name+"|awk -F '|' '{print $2}'"
        command=self._openstackInsertAuth(command)
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
        command="openstack network list "+"|grep -i "+net_id+"|awk -F '|' '{print $4}'"
        command=self._openstackInsertAuth(command)
        subnet_id=subprocess.check_output(command,shell=True)
        subnet_id=subnet_id.strip()
        if not subnet_id:
            return None
        return subnet_id

    def getSubnetPortIds(self,subnet_id):
        """
        获得子网的端口id
        :param subnet_id:
        :return:
        """
        command="openstack port list|grep -i "+subnet_id+"|awk -F '|' '{print $2}'"
        command=self._openstackInsertAuth(command)
        subnetPort_ids=subprocess.check_output(command,shell=True)
        subnetPort_ids=subnetPort_ids.strip()
        subnetPort_ids=subnetPort_ids.split('\n')
        return subnetPort_ids

    def deleteSubnetPorts(self,subnetPort_ids):
        """
        删除子网的端口
        :param subnetPort_ids:
        :return:
        """
        if len(subnetPort_ids) != 0:
            del_subnetPorts_command = "openstack port delete "
            for subnetPort_id in subnetPort_ids:
                del_subnetPorts_command=del_subnetPorts_command+subnetPort_id+' '
            del_subnetPorts_command = self._openstackInsertAuth(del_subnetPorts_command)
            subprocess.check_output(del_subnetPorts_command, shell=True)
        return True

    def getRouterId(self,router_name):
        """
        获得路由id
        :param router_name:
        :return:router_id
        """
        command = "openstack router list|grep -i " + router_name +"|awk -F '|' '{print $2}'"
        command = self._openstackInsertAuth(command)
        router_id = subprocess.check_output(command, shell=True)
        router_id = router_id.strip()
        if not router_id:
            return None
        return router_id

    def setRouterGW(self,router_id,admin_float_net_id):
        """
        设置路由器的网关
        :param router_id:
        :param admin_float_net_id:
        :return:
        """
        command="openstack router set --external-gateway "+admin_float_net_id+" "+router_id
        command=self._openstackInsertAuth(command)
        subprocess.check_output(command,shell=True)
        return True

    def createRouter(self,router_name,admin_float_net_id):
        """
        创建一个路由并设置网关
        :param router_name:
        :param admin_float_net_id:
        :return:route_id
        """
        command="openstack router create "+router_name+"|grep -i \"| id\"|awk -F '|' '{print $3}'"
        command=self._openstackInsertAuth(command)
        route_id=subprocess.check_output(command,shell=True)
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
        command="openstack router add subnet "+router_id+" "+sub_net_id
        command=self._openstackInsertAuth(command)
        subprocess.check_output(command,shell=True)
        return True

    def removeRouterInterface(self,router_id,sub_net_id):
        """
        将接口从路由器上解绑
        :param router_id:
        :param sub_net_id:
        :return:
        """
        command="openstack router remove subnet "+router_id+" "+sub_net_id
        command=self._openstackInsertAuth(command)
        subprocess.check_output(command,shell=True)
        return True

    def getFloatIp(self,admin_float_net_id):
        """
        申请一个浮动ip
        :param admin_float_net_id:
        :return: ip_address
        """
        command="openstack floating ip create " +admin_float_net_id+"|grep -i floating_ip_address|awk -F '|' '{print $3}'"
        command=self._openstackInsertAuth(command)
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
        command="openstack floating ip list |grep -i "+float_ip_address+"|awk -F '|' '{print $2}'"
        command=self._openstackInsertAuth(command)
        ip_id=subprocess.check_output(command,shell=True)
        ip_id=ip_id.strip()
        return ip_id

    def getAccountfloatingipIds(self,project_id):
        """
        :param project_id:
        :return:
        """
        command="openstack floating ip list |grep -i " + project_id + "|awk -F '|' '{print $2}'"
        command = self._openstackInsertAuth(command)
        floatingip_ids = subprocess.check_output(command, shell=True)
        floatingip_ids = floatingip_ids.split('\n')
        return floatingip_ids

    def deleteAllNet(self,net_ids):
        """
        删除所有的网络
        :param net_ids:
        :return:
        """
        if len(net_ids) != 0:
            del_command = "openstack network delete "
            for net_id in net_ids:
                del_command = del_command+net_id+' '
            del_command = self._openstackInsertAuth(del_command)
            subprocess.check_output(del_command, shell=True)
        return True

    def _clearRouterGW(self, router_id):
        """
        清除路由器网关
        :param router_id:
        :return:
        """
        command = 'openstack router unset --external-gateway ' + router_id
        command = self._openstackInsertAuth(command)
        subprocess.check_output(command, shell=True)
        return True

    def deleteAllRouter(self,router_ids):
        """
        删除路由器
        :param router_ids:
        :return:
        """
        if len(router_ids) != 0:
            del_router_command = "openstack router delete "
            for router_id in router_ids:
                del_router_command=del_router_command+router_id+' '
            del_router_command = self._openstackInsertAuth(del_router_command)
            subprocess.check_output(del_router_command, shell=True)
        return True

    def deleteAllFloatIp(self,floatIp_ids):
        """
        删除浮动ip
        :param floatIp_ids:
        :return:
        """
        if len(floatIp_ids) != 0:
            del_floatIp_command = "openstack floating ip delete "
            for floatIp_id in floatIp_ids:
                del_floatIp_command = del_floatIp_command+floatIp_id+' '
            del_floatIp_command = self._openstackInsertAuth(del_floatIp_command)
            subprocess.check_output(del_floatIp_command, shell=True)
        return True
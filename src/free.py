#!-*- coding:utf8 -*-
from src.clients.novaClient import NovaClient
from src.clients.openstackClient import OpenstackClient
from src.clients.cinderClient import CinderClient
from src.clients.keystoneClient import KeystoneClient
from src.clients.loadbalancerClient import LoadbalancerClient
from src.clients.troveClient import TroveClient
from src.clients.heatClient import HeatClient
from src.clients.objectstoreClient import ObjectStoreClient

class Free:
    def __init__(self,account_dict):
        self._os_tenant_name=account_dict['os_tenant_name']
        self._os_project_name=account_dict['os_project_name']
        self._os_project_id = account_dict['os_project_id']
        self._os_username=account_dict['os_username']
        self._os_userid=account_dict['os_userid']
        self._os_password=account_dict['os_password']

        self._novaClient=NovaClient(self._os_project_name,self._os_username,self._os_password)
        self._openstackClient=OpenstackClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._cinderClient=CinderClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._loadbalancerClient = LoadbalancerClient(self._os_tenant_name, self._os_project_name, self._os_username,self._os_password)
        self._keystoneClient=KeystoneClient()
        self._troveClient=TroveClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._heatClient = HeatClient(self._os_tenant_name, self._os_project_name, self._os_username,self._os_password)
        self._objectstoreClient = ObjectStoreClient()

    def freeCompute(self,computes_array):
        compute_ids=[]
        for compute in computes_array:
            if compute['id']:
                compute_ids.append(compute['id'])
        self._novaClient.deleteAllCompute(compute_ids)

    def freeVolume(self,volumes_array):
        volume_ids=[]
        for volume in volumes_array:
            if volume['id']:
                volume_ids.append(volume['id'])
        self._cinderClient.deleteAllVolume(volume_ids)

    def freeLoadbalancer(self,loadbalancers_array):
        loadbalancer_ids=[]
        for loadbalancer in loadbalancers_array:
            if loadbalancer['id']:
                loadbalancer_ids.append(loadbalancer['id'])
        self._loadbalancerClient.deleteLoadbalancer(loadbalancer_ids)

    def freeRouter(self,routers_array):
        router_ids=[]
        for router in routers_array:
            router_id=router['id']
            if router_id:
                router_ids.append(router_id)
            router_subnet_ids=router['subnet_ids']
            for router_subnet_id in router_subnet_ids:
                if router_subnet_id:
                    self._openstackClient.removeRouterInterface(router_id,router_subnet_id)
        self._openstackClient.deleteAllRouter(router_ids)

    def freeNet(self,nets_array):
        net_ids=[]
        subnetPort_ids=[]
        for net in nets_array:
            if net['id']:
                subnet_id=self._openstackClient.getSubNetId(net['id'])
                subnetPort_ids=subnetPort_ids+self._openstackClient.getSubnetPortIds(subnet_id)
                net_ids.append(net['id'])
        self._openstackClient.deleteSubnetPorts(subnetPort_ids)
        self._openstackClient.deleteAllNet(net_ids)

    def freeFloatIp(self,floatIps_array):
        floatIp_ids=[]
        for floatIp in floatIps_array:
            if floatIp['id']:
                floatIp_ids.append(floatIp['id'])
        self._openstackClient.deleteAllFloatIp(floatIp_ids)

    def freeSecgroup(self,secgruop_array):
        pass

    def freeSysbench(self,sysbench_array):
        sysbench1_ids=[]
        sysbench_ids = []
        for sysbench1 in sysbench_array:
            if sysbench1[1]:
                sysbench1_ids.append(sysbench1[1])
        for sysbench in sysbench1_ids:
            if sysbench['id']:
                sysbench_ids.append(sysbench['id'])
        self._troveClient.deleteAllTrove(sysbench_ids)

    def freeHeat(self,heat_array):
        heat_ids=[]
        for floatIp in heat_array:
            if floatIp['id']:
                heat_ids.append(floatIp['id'])
        self._heatClient.deleteAllHeat(heat_ids)

    def freeObejectstore(self):
        if not self._os_project_id:
            return False
        self._objectstoreClient.deleteAllBuckets(self._os_project_id)

    def freeAccount(self):
        if not self._os_userid or not self._os_project_id:
            return False
        self._keystoneClient.deleteAccount(self._os_userid.encode('utf-8'),self._os_project_id.encode('utf-8'))





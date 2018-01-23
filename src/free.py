#!-*- coding:utf8 -*-
from src.clients.novaClient import NovaClient
from src.clients.neutronClient import NeutronClient
from src.clients.cinderClient import CinderClient
from src.clients.keystoneClient import KeystoneClient
from src.clients.loadbalancerClient import LoadbalancerClient
from src.clients.troveClient import TroveClient
from src.clients.heatClient import HeatClient

class Free():
    def __init__(self,account_dict):
        self._os_tenant_name=account_dict['os_tenant_name']
        self._os_project_name=account_dict['os_project_name']
        self._os_project_id = account_dict['os_project_id']
        self._os_username=account_dict['os_username']
        self._os_userid=account_dict['os_userid']
        self._os_password=account_dict['os_password']

        self._novaClient=NovaClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._neutronClient=NeutronClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._cinderClient=CinderClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._loadbalancerClient = LoadbalancerClient(self._os_tenant_name, self._os_project_name, self._os_username,self._os_password)
        self._keystoneClient=KeystoneClient()
        self._troveClient=TroveClient(self._os_tenant_name,self._os_project_name,self._os_username,self._os_password)
        self._heatClient = HeatClient(self._os_tenant_name, self._os_project_name, self._os_username,self._os_password)

    def freeCompute(self,computes_array):
        compute_ids=[]
        for compute in computes_array:
            compute_ids.append(compute['id'])
        self._novaClient.deleteAllCompute(compute_ids)

    def freeVolume(self,volumes_array):
        volume_ids=[]
        for volume in volumes_array:
            volume_ids.append(volume['id'])
        self._cinderClient.deleteAllVolume(volume_ids)

    def freeLoadbalancer(self,loadbalancers_array):
        loadbalancer_ids=[]
        for loadbalancer in loadbalancers_array:
            loadbalancer_ids.append(loadbalancer['id'])
        self._loadbalancerClient.deleteLoadbalancer(loadbalancer_ids)

    def freeRouter(self,routers_array):
        router_ids=[]
        for router in routers_array:
            router_ids.append(router['id'])
        self._neutronClient.deleteAllRouter(router_ids)

    def freeNet(self,nets_array):
        net_ids=[]
        for net in nets_array:
            net_ids.append(net['id'])
        self._neutronClient.deleteAllNet(net_ids)

    def freeFloatIp(self,floatIps_array):
        floatIp_ids=[]
        for floatIp in floatIps_array:
            floatIp_ids.append(floatIp['id'])
        self._neutronClient.deleteAllFloatIp(floatIp_ids)

    def freeSecgroup(self,secgruop_array):
        pass

    def freeSysbench(self,sysbench_array):
        sysbench1_ids=[]
        sysbench_ids = []
        for sysbench1 in sysbench_array:
            sysbench1_ids.append(sysbench1[1])
        for sysbench in sysbench1_ids:
            sysbench_ids.append(sysbench['id'])
        self._troveClient.deleteAllTrove(sysbench_ids)

    def freeHeat(self,heat_array):
        heat_ids=[]
        for floatIp in heat_array:
            heat_ids.append(floatIp['id'])
        self._heatClient.deleteAllHeat(heat_ids)


    def freeAccount(self):
        if not self._os_userid or not self._os_project_id:
            return False
        self._keystoneClient.deleteUser(self._os_userid.encode('utf-8'),self._os_project_id.encode('utf-8'))


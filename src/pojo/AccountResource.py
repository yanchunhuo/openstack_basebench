#!-*- coding:utf8 -*-
from src.pojo.Account import Account

class AccountResource():
    def __init__(self):
        self._secgroups=[]
        self._nets=[]
        self._adminNets=[]
        self._flavors=[]
        self._images=[]
        self._volumeTypes=[]
        self._routers=[]
        self._zones=[]
        self._volumes=[]
        self._computes=[]
        self._floatIps=[]
        self._iperfComputePairs=[]
        self._fioComputes=[]
        self._unixbenchComputes=[]
        self._memtesterComputes=[]
        self._loadbalancers = []
        self._account=Account()
        self._sysbenchComputePairs=[]
        self._heatComputes = []
        self._objectstorage =[]

    def get_secgroups(self):
        return self._secgroups

    def add_secgroup(self,secgroup_obj):
        self._secgroups.append(secgroup_obj)

    def get_nets(self):
        return self._nets

    def add_net(self,net_obj):
        self._nets.append(net_obj)

    def get_adminNets(self):
        return self._adminNets

    def add_adminNet(self,adminNet_obj):
        self._adminNets.append(adminNet_obj)

    def get_flavors(self):
        return self._flavors

    def add_flavor(self, flavor_obj):
        self._flavors.append(flavor_obj)

    def get_images(self):
        return self._images

    def add_image(self,image_obj):
        self._images.append(image_obj)

    def get_volumeTypes(self):
        return self._volumeTypes

    def add_volumeType(self,volumeType_obj):
        self._volumeTypes.append(volumeType_obj)

    def get_routers(self):
        return self._routers

    def add_router(self,router_obj):
        return self._routers.append(router_obj)

    def get_zones(self):
        return self._zones

    def add_zone(self,zone_array):
        self._zones=zone_array

    def get_volumes(self):
        return self._volumes

    def add_volume(self,volume_obj):
        self._volumes.append(volume_obj)

    def get_computes(self):
        return self._computes

    def add_compute(self,compute_obj):
        self._computes.append(compute_obj)

    def get_account(self):
        return self._account

    def add_account(self,account_obj):
        self._account=account_obj

    def get_floatIps(self):
        return self._floatIps

    def add_floatIp(self,floatIp_obj):
        self._floatIps.append(floatIp_obj)

    def add_iperfComputePair(self,computePair):
        self._iperfComputePairs.append(computePair)

    def get_iperfComputeParis(self):
        return self._iperfComputePairs

    def add_fioCompute(self,compute_obj):
        self._fioComputes.append(compute_obj)

    def get_fioComputes(self):
        return self._fioComputes

    def add_unixbenchCompute(self,compute_obj):
        self._unixbenchComputes.append(compute_obj)

    def get_unixbenchComputes(self):
        return self._unixbenchComputes

    def add_memtesterCompute(self,compute_obj):
        self._memtesterComputes.append(compute_obj)

    def get_memtesterComputes(self):
        return self._memtesterComputes

    def add_sysbenchComputePair(self,computePair):
        self._sysbenchComputePairs.append(computePair)

    def get_sysbenchComputeParis(self):
        return self._sysbenchComputePairs

    def add_loadbalancer(self,compute_obj):
        self._loadbalancers.append(compute_obj)

    def get_loadbalancers(self):
        return self._loadbalancers

    def add_heatCompute(self,compute_obj):
        self._heatComputes.append(compute_obj)

    def get_heatComputes(self):
        return self._heatComputes

    def add_objectstorageCompute(self,compute_obj):
        self._objectstorage.append(compute_obj)

    def get_objectstorageCompute(self):
        return self._objectstorage

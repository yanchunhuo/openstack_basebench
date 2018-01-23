#!-*- coding:utf8 -*-
import threading
from src.common import readJsonFromFile
from src.free import Free
import os

class FreeAccountResource(threading.Thread):
    def __init__(self,accountResourceFilePath,logger):
        threading.Thread.__init__(self,name='freeAccountResource')
        self._accountResourceFIlePath=accountResourceFilePath
        self._logger=logger

    def run(self):
        accountResource=readJsonFromFile(self._accountResourceFIlePath)
        account_dict = accountResource['_account']
        computes_array=accountResource['_computes']
        volumes_array= accountResource['_volumes']
        floatIps_array = accountResource['_floatIps']
        routers_array=accountResource['_routers']
        nets_array=accountResource['_nets']
        secgroup_array=accountResource['_secgroups']
        loadbalancers_array = accountResource['_loadbalancers']
        sysbench_array = accountResource['_sysbenchComputePairs']
        heat_array = accountResource['_heatComputes']

        self._free=Free(account_dict)
        self._logger.info('释放数据库实例资源')
        self._free.freeSysbench(sysbench_array)
        self._logger.info('释放伸缩资源')
        self._free.freeHeat(heat_array)
        self._logger.info('释放云主机资源')
        self._free.freeCompute(computes_array)
        self._logger.info('释放负载均衡器资源')
        self._free.freeLoadbalancer(loadbalancers_array)
        self._logger.info('释放云硬盘资源')
        self._free.freeVolume(volumes_array)
        self._logger.info('释放浮动IP资源')
        self._free.freeFloatIp(floatIps_array)
        self._logger.info('释放路由器资源')
        self._free.freeRouter(routers_array)
        self._logger.info('释放网络资源')
        self._free.freeNet(nets_array)
        self._logger.info('释放安全组资源')
        self._free.freeSecgroup(secgroup_array)
        self._logger.info('释放账户')
        self._free.freeAccount()

        self._logger.info('删除账户资源文件'+self._accountResourceFIlePath)
        os.remove(self._accountResourceFIlePath)
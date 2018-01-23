#!-*- coding:utf8 -*-
from src.testBasePerformance.tests import Tests
from src.testBasePerformance.initResource import InitResource
from src.logger import basePerformanceLogger
from src.common import readJsonFromFile
from src.free import Free
from config.config import IS_TEST_FIO
from config.config import IS_TEST_UNIXBENCH
from config.config import IS_TEST_IPERF
import os

class TestBasePerformance():
    def __init__(self):
        pass


    def free(self):
        if not os.path.exists('dbs/basePerformanceTestAccountResource.dbs'):
            return
        basePerformanceLogger.info('读取文件' + 'dbs/basePerformanceTestAccountResource.dbs')
        accountResource=readJsonFromFile('dbs/basePerformanceTestAccountResource.dbs')
        account_dict = accountResource['_account']
        computes_array=accountResource['_computes']
        volumes_array= accountResource['_volumes']
        floatIps_array = accountResource['_floatIps']
        routers_array=accountResource['_routers']
        nets_array=accountResource['_nets']

        basePerformanceLogger.info('释放账号' + account_dict['os_username'].encode('utf-8') + '资源')
        self._free=Free(account_dict)
        basePerformanceLogger.info('释放账号' + account_dict['os_username'].encode('utf-8') + '的云主机资源')
        self._free.freeCompute(computes_array)
        basePerformanceLogger.info('释放账号' + account_dict['os_username'].encode('utf-8') + '的云硬盘资源')
        self._free.freeVolume(volumes_array)
        basePerformanceLogger.info('释放账号' + account_dict['os_username'].encode('utf-8') + '的路由器资源')
        self._free.freeRouter(routers_array)
        basePerformanceLogger.info('释放账号' + account_dict['os_username'].encode('utf-8') + '的网络资源')
        self._free.freeNet(nets_array)
        basePerformanceLogger.info('释放账号' + account_dict['os_username'].encode('utf-8') + '的浮动IP资源')
        self._free.freeFloatIp(floatIps_array)
        basePerformanceLogger.info('释放账号' + account_dict['os_username'].encode('utf-8') + '账号')
        self._free.freeAccount()

        basePerformanceLogger.info('删除文件dbs/basePerformanceTestAccountResource.dbs')
        os.remove('dbs/basePerformanceTestAccountResource.dbs')

    def start(self):
        basePerformanceLogger.info('===开始基准测试===')
        self._tests=Tests()
        self._accountresource=InitResource().getBasePerformanceAccountResource()

        #fio测试
        if IS_TEST_FIO:
            fio_computes = self._accountresource.get_fioComputes()
            for compute in fio_computes:
                self._tests.testFio(compute)

        #unixbench测试
        if IS_TEST_UNIXBENCH:
            unixbench_computes=self._accountresource.get_unixbenchComputes()
            for compute in unixbench_computes:
                self._tests.testUinxbench(compute)

        # iperf测试
        if IS_TEST_IPERF:
            test_iperf_ComputePairs=self._accountresource.get_iperfComputeParis()
            for iperf_computePair in test_iperf_ComputePairs:
                compute_client=iperf_computePair[0]
                compute_server=iperf_computePair[1]
                self._tests.testIperf(compute_client,compute_server)

        basePerformanceLogger.info('===完成基准测试===')



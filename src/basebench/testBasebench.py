#!-*- coding:utf8 -*-
from src.basebench.tests import Tests
from src.basebench.initResource import InitResource
from src.readConfig import ReadConfig
from src.common.fileTool import FileTool
from src.loggers import Loggers
from src.free import Free
import os

class TestBasebench:
    def __init__(self):
        self._loggers=Loggers()
        self._readConfig=ReadConfig()
        self._tests = Tests()
        self._accountresource=None

    def free(self):
        if not os.path.exists('dbs/basebenchTestAccountResource.dbs'):
            return
        self._loggers.basebenchLogger.info('读取文件' + 'dbs/basebenchTestAccountResource.dbs')
        accountResource=FileTool.readJsonFromFile('dbs/basebenchTestAccountResource.dbs')
        account_dict = accountResource['_account']
        computes_array=accountResource['_computes']
        volumes_array= accountResource['_volumes']
        floatIps_array = accountResource['_floatIps']
        routers_array=accountResource['_routers']
        nets_array=accountResource['_nets']

        self._loggers.basebenchLogger.info('释放账号' + account_dict['os_username'].encode('utf-8') + '资源')
        free=Free(account_dict)
        self._loggers.basebenchLogger.info('释放账号' + account_dict['os_username'].encode('utf-8') + '的云主机资源')
        free.freeCompute(computes_array)
        self._loggers.basebenchLogger.info('释放账号' + account_dict['os_username'].encode('utf-8') + '的云硬盘资源')
        free.freeVolume(volumes_array)
        self._loggers.basebenchLogger.info('释放账号' + account_dict['os_username'].encode('utf-8') + '的浮动IP资源')
        free.freeFloatIp(floatIps_array)
        self._loggers.basebenchLogger.info('释放账号' + account_dict['os_username'].encode('utf-8') + '的路由器资源')
        free.freeRouter(routers_array)
        self._loggers.basebenchLogger.info('释放账号' + account_dict['os_username'].encode('utf-8') + '的网络资源')
        free.freeNet(nets_array)
        self._loggers.basebenchLogger.info('释放账号' + account_dict['os_username'].encode('utf-8') + '账号')
        free.freeAccount()

        self._loggers.basebenchLogger.info('删除文件dbs/basebenchTestAccountResource.dbs')
        os.remove('dbs/basebenchTestAccountResource.dbs')

    def start(self):
        self._loggers.basebenchLogger.info('===开始基准测试===')
        self._accountresource=InitResource().getBasebenchTestAccountResource()

        #fio测试
        if self._readConfig.executeTest.is_basebench_test_fio.lower()=='true':
            fio_computes = self._accountresource.get_fioComputes()
            for compute in fio_computes:
                self._tests.testFio(compute)

        #unixbench测试
        if self._readConfig.executeTest.is_basebench_test_unixbench.lower()=='true':
            unixbench_computes=self._accountresource.get_unixbenchComputes()
            for compute in unixbench_computes:
                self._tests.testUinxbench(compute)

        # iperf测试
        if self._readConfig.executeTest.is_basebench_test_iperf.lower()=='true':
            test_iperf_ComputePairs=self._accountresource.get_iperfComputeParis()
            for iperf_computePair in test_iperf_ComputePairs:
                compute_client=iperf_computePair[0]
                compute_server=iperf_computePair[1]
                self._tests.testIperf(compute_client,compute_server)

        self._loggers.basebenchLogger.info('===完成基准测试===')



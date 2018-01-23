#!-*- coding:utf8 -*-
from src.logger import stabilityLoadbalancerLogger
from config.config import IS_STABILITY_TEST_MEMTESTER
from config.config import IS_STABILITY_TEST_IPERF
from config.config import IS_STABILITY_TEST_FIO
from config.config import IS_STABILITY_TEST_SYSBENCH
from config.config import IS_STABILITY_TEST_UNIXBENCH
from config.config import IS_STABILITY_TEST_LOADBALANCER
from config.config import IS_STABILITY_TEST_JMETER
from config.config import IS_STABILITY_TEST_HEAT
from config.config import IS_STABILITY_TEST_OBJECTSTORAGE
from src.logger import stabilityIperfLogger
from src.logger import stabilitySysbenchLogger
from src.logger import stabilityHeatLogger
from src.logger import stabilityMemtesterLogger
from src.logger import stabilityUnixbenchLogger
from src.logger import stabilityFioLogger
from src.logger import stabilityObjectStorageLogger
from src.startThread.startMemtester import StartMemtester
from src.stopThread.stopMemtester import StopMemtester
from src.restartThread.reStartMemtester import ReStartMemtester
from src.startThread.startIperf import StartIperf
from src.stopThread.stopIperf import StopIperf
from src.restartThread.reStartIperf import ReStartIperf
from src.startThread.startFio import StartFio
from src.stopThread.stopFio import StopFio
from src.restartThread.reStartFio import ReStartFio
from src.startThread.startObjectstorage import StartObjectStorage
from src.stopThread.stopObjectstorage import StopObjectStorage
from src.restartThread.reStartObjectStorage import RestartObjectStorage
from src.startThread.startSysbench import StartSysbench
from src.stopThread.stopSysbench import StopSysbench
from src.restartThread.reStartSysbench import ReStartSysbench
from src.startThread.startUnixbench import StartUnixbench
from src.stopThread.stopUnixbench import StopUnixbench
from src.restartThread.reStartUnixbench import ReStartUnixbench
from src.startThread.startLoadbalancer import StartLoadbalancer
from src.stopThread.stopLoadbalancer import StopLoadbalancer
from src.restartThread.reStartLoadbalancer import ReStartLoadbalancer
from src.startThread.startHeat import StartHeat
from src.freeThread.freeAccountResource import FreeAccountResource
import os

class TestStability():
    def __init__(self):
        pass


    def free(self):
        """
        每种类型启动一个线程
        :return:
        """

        if os.path.exists('dbs/stabilityMemtesterTestAccountResource.dbs'):
            stabilityMemtesterLogger.info('释放memtester账户资源')
            freeMemtesterAccountResource=FreeAccountResource('dbs/stabilityMemtesterTestAccountResource.dbs',stabilityMemtesterLogger)
            freeMemtesterAccountResource.start()

        if os.path.exists('dbs/stabilityIperfTestAccountResource.dbs'):
            stabilityIperfLogger.info('释放iperf账户资源')
            freeIperfAccountResource = FreeAccountResource('dbs/stabilityIperfTestAccountResource.dbs',stabilityIperfLogger)
            freeIperfAccountResource.start()

        # 释放fio账户资源
        if os.path.exists('dbs/stabilityFioTestAccountResource.dbs'):
            stabilityFioLogger.info('释放fio账户资源')
            freeFioAccountResource = FreeAccountResource('dbs/stabilityFioTestAccountResource.dbs',stabilityFioLogger)
            freeFioAccountResource.start()

        # 释放sysbench账户资源
        if os.path.exists('dbs/stabilitySysbenchTestAccountResource.dbs'):
            stabilitySysbenchLogger.info('释放sysbench账户资源')
            freeSysbenchAccountResource = FreeAccountResource('dbs/stabilitySysbenchTestAccountResource.dbs',stabilitySysbenchLogger)
            freeSysbenchAccountResource.start()

        # 释放unixbench账户资源
        if os.path.exists('dbs/stabilityUnixbenchTestAccountResource.dbs'):
            freeUnixbenchAccountResource = FreeAccountResource('dbs/stabilityUnixbenchTestAccountResource.dbs',stabilityUnixbenchLogger)
            freeUnixbenchAccountResource.start()

        # 释放loadbalancer账户资源
        if os.path.exists('dbs/stabilityLoadbalancerTestAccountResource.dbs'):
            freeLoadbalancerAccountResource = FreeAccountResource('dbs/stabilityLoadbalancerTestAccountResource.dbs',stabilityLoadbalancerLogger)
            freeLoadbalancerAccountResource.start()

        # 释放heat账户资源
        if os.path.exists('dbs/stabilityHeatTestAccountResource.dbs'):
            stabilityHeatLogger.info('释放heat账户资源')
            freeHeatAccountResource = FreeAccountResource('dbs/stabilityHeatTestAccountResource.dbs',stabilityHeatLogger)
            freeHeatAccountResource.start()

        # 释放对象存储账户资源
        if os.path.exists('dbs/stabilityObjectStorageTestAccountResource.dbs'):
            stabilityObjectStorageLogger.info('释放heat账户资源')
            freeobjectstorageAccountResource = FreeAccountResource('dbs/stabilityObjectStorageTestAccountResource.dbs',stabilityObjectStorageLogger)
            freeobjectstorageAccountResource.start()

    def start(self):
        """
        每种类型启动一个线程
        :return:
        """

        if IS_STABILITY_TEST_MEMTESTER:
            stabilityMemtesterLogger.info('开始memtester稳定性测试')
            startMemtester=StartMemtester()
            startMemtester.start()

        if IS_STABILITY_TEST_IPERF:
            stabilityIperfLogger.info('开始iperf稳定性测试')
            startIperf=StartIperf()
            startIperf.start()

        # fio测试
        if IS_STABILITY_TEST_FIO:
            startFio = StartFio()
            startFio.start()

        #sysbench测试
        if IS_STABILITY_TEST_SYSBENCH:
            stabilitySysbenchLogger.info('开始sysbench稳定性测试')
            startSysbench=StartSysbench()
            startSysbench.start()

        # unixbench测试
        if IS_STABILITY_TEST_UNIXBENCH:
            startUnixbench = StartUnixbench()
            startUnixbench.start()

        #loadbalancer测试
        if IS_STABILITY_TEST_LOADBALANCER and IS_STABILITY_TEST_JMETER:
            startLoadbalancer = StartLoadbalancer()
            startLoadbalancer.start()

        # heat测试
        if IS_STABILITY_TEST_HEAT :
            stabilityHeatLogger.info('开始heat稳定性测试')
            startHeat = StartHeat()
            startHeat.start()

        # 对象存储测试
        if IS_STABILITY_TEST_OBJECTSTORAGE :
            stabilityObjectStorageLogger.info('开始heat稳定性测试')
            startObjectstorage = StartObjectStorage()
            startObjectstorage.start()


    def stop(self):
        """
        每种类型启动一个线程
        :return:
        """

        if os.path.exists('dbs/stabilityMemtesterTestAccountResource.dbs'):
            stabilityMemtesterLogger.info('停止memtester稳定性测试')
            stopMemtester=StopMemtester('dbs/stabilityMemtesterTestAccountResource.dbs')
            stopMemtester.start()

        if os.path.exists('dbs/stabilityIperfTestAccountResource.dbs'):
            stabilityIperfLogger.info('停止iperf稳定性测试')
            stopIperf=StopIperf('dbs/stabilityIperfTestAccountResource.dbs')
            stopIperf.start()

        #停止fio测试
        if os.path.exists('dbs/stabilityFioTestAccountResource.dbs'):
            stabilityFioLogger.info('停止fio稳定性测试')
            stopFio = StopFio('dbs/stabilityFioTestAccountResource.dbs')
            stopFio.start()

        #停止sysbench测试
        if os.path.exists('dbs/stabilitySysbenchTestAccountResource.dbs'):
            stabilitySysbenchLogger.info('停止sysbench稳定性测试')
            stopSysbench=StopSysbench('dbs/stabilitySysbenchTestAccountResource.dbs')
            stopSysbench.start()

        # 停止unixbench测试
        if os.path.exists('dbs/stabilityUnixbenchTestAccountResource.dbs'):
            stopUnixbench = StopUnixbench('dbs/stabilityUnixbenchTestAccountResource.dbs')
            stopUnixbench.start()

        # 停止loadbalancer测试
        if os.path.exists('dbs/stabilityLoadbalancerTestAccountResource.dbs'):
            stopLoadbalancer = StopLoadbalancer('dbs/stabilityLoadbalancerTestAccountResource.dbs')
            stopLoadbalancer.start()

        # 停止对象存储测试
        if os.path.exists('dbs/stabilityObjectStorageTestAccountResource.dbs'):
            stabilityObjectStorageLogger.info('停止对象存储稳定性测试')
            stopObjectstorage = StopObjectStorage('dbs/stabilityObjectStorageTestAccountResource.dbs')
            stopObjectstorage.start()

    def restart(self):
        """
        稳定性测试重启程序
        :return:
        """

        if os.path.exists('dbs/stabilityIperfTestAccountResource.dbs'):
            stabilityIperfLogger.info('重启iperf稳定性测试')
            reStartIperf=ReStartIperf('dbs/stabilityIperfTestAccountResource.dbs')
            reStartIperf.start()

        # 重启memtester测试
        if os.path.exists('dbs/stabilityMemtesterTestAccountResource.dbs'):
            stabilityMemtesterLogger.info('重启memtester稳定性测试')
            reStartUnixbench = ReStartMemtester('dbs/stabilityMemtesterTestAccountResource.dbs')
            reStartUnixbench.start()

        # 重启sysbench测试
        if os.path.exists('dbs/stabilitySysbenchTestAccountResource.dbs'):
            stabilitySysbenchLogger.info('重启sysbench稳定性测试')
            reStartSysbench = ReStartSysbench('dbs/stabilitySysbenchTestAccountResource.dbs')
            reStartSysbench.start()

        # 重启unixbench测试
        if os.path.exists('dbs/stabilityUnixbenchTestAccountResource.dbs'):
            stabilityUnixbenchLogger.info('重启unixbench稳定性测试')
            reStartUnixbench = ReStartUnixbench('dbs/stabilityUnixbenchTestAccountResource.dbs')
            reStartUnixbench.start()

        # 重启loadbalancer测试
        if os.path.exists('dbs/stabilityLoadbalancerTestAccountResource.dbs'):
            stabilityLoadbalancerLogger.info('重启loadbalancer稳定性测试')
            reStartLoadbalancer = ReStartLoadbalancer('dbs/stabilityLoadbalancerTestAccountResource.dbs')
            reStartLoadbalancer.start()

        # 重启fio测试
        if os.path.exists('dbs/stabilityFioTestAccountResource.dbs'):
            stabilityFioLogger.info('重启fio稳定性测试')
            reStartFio = ReStartFio('dbs/stabilityFioTestAccountResource.dbs')
            reStartFio.start()

        # 重启对象存储测试
        if os.path.exists('dbs/stabilityObjectStorageTestAccountResource.dbs'):
            stabilityObjectStorageLogger.info('重启对象存储测试')
            reStartObjectStorage = RestartObjectStorage('dbs/stabilityObjectStorageTestAccountResource.dbs')
            reStartObjectStorage.start()

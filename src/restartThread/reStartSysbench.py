#!-*- coding:utf8 -*-
import threading
from src.testStability.testSysbench import TestSysbench
from src.common import readJsonFromFile
from src.pojo.Compute import Compute



class ReStartSysbench(threading.Thread):
    def __init__(self,accountResourceFilePath):
        threading.Thread.__init__(self,name='reStartSysbench')
        self._accountResourceFilePath=accountResourceFilePath

    def run(self):
        testSysbench = TestSysbench()
        sysbenchAccountResource=readJsonFromFile(self._accountResourceFilePath)
        sysbench_pair_array=sysbenchAccountResource['_sysbenchComputePairs']
        for sysbench_pair in sysbench_pair_array:
            compute_client=Compute()
            trove_server=Compute()
            compute_client.__dict__ = sysbench_pair[0]
            trove_server.__dict__ = sysbench_pair[1]
            testSysbench.reStart(compute_client,trove_server)
#!-*- coding:utf8 -*-
from src.common.fileTool import FileTool
from src.pojo.Compute import Compute
from src.testStability.testSysbench import TestSysbench
import threading

class StopSysbench(threading.Thread):
    def __init__(self,accountResourceFilePath):
        threading.Thread.__init__(self,name='stopSysbench')
        self._accountResourceFilePath=accountResourceFilePath

    def run(self):
        testSysbench = TestSysbench()
        sysbenchAccountResource=FileTool.readJsonFromFile(self._accountResourceFilePath)
        compute_pair_array=sysbenchAccountResource['_sysbenchComputePairs']
        for compute_pair in compute_pair_array:
            compute_client=Compute()
            compute_server=Compute()
            compute_client.__dict__ = compute_pair[0]
            compute_server.__dict__ = compute_pair[1]
            testSysbench.stop(compute_client)
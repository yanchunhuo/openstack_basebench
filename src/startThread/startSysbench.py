#!-*- coding:utf8 -*-
import threading
from src.testStability.testSysbench import TestSysbench
from src.testStability.initSysbenchResource import InitSysbenchResource

class StartSysbench(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self,name='startSysbench')

    def run(self):
        testSysbench=TestSysbench()
        sysbenchAccountResource=InitSysbenchResource().getStabilitySysbenchAccountResource()
        test_sysbench_ComputePairs = sysbenchAccountResource.get_sysbenchComputeParis()
        for sysbench_computePair in test_sysbench_ComputePairs:
            compute_client = sysbench_computePair[0]
            trove_server = sysbench_computePair[1]
            testSysbench.start(compute_client, trove_server)
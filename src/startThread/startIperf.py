#!-*- coding:utf8 -*-
from src.testStability.testIperf import TestIperf
from src.testStability.initIperfResource import InitIperfResource
import threading

class StartIperf(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self,name='startIperf')

    def run(self):
        testIperf=TestIperf()
        iperfAccountResource=InitIperfResource().getStabilityIperfAccountResource()
        test_iperf_ComputePairs = iperfAccountResource.get_iperfComputeParis()
        for iperf_computePair in test_iperf_ComputePairs:
            compute_client = iperf_computePair[0]
            compute_server = iperf_computePair[1]
            testIperf.start(compute_client, compute_server)

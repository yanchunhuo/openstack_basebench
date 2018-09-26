#!-*- coding:utf8 -*-
from src.testStability.testUnixbench import TestUnixbench
from src.testStability.initUnixbenchResource import InitUnixbenchResource
import threading

class StartUnixbench(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self,name='startUnixbench')

    def run(self):
        testUnixbench = TestUnixbench()
        stabilityAccountResouce = InitUnixbenchResource().getStabilityUnixbenchAccountResource()
        unixbench_computes = stabilityAccountResouce.get_unixbenchComputes()
        for compute in unixbench_computes:
            testUnixbench.start(compute)
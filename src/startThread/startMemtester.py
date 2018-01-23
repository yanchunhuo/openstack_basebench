#!-*- coding:utf8 -*-
import threading
from src.testStability.testMemtester import TestMemtester
from src.testStability.initMemtesterResource import InitMemtesterResource

class StartMemtester(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self,name='startMemtester')

    def run(self):
        testMemtester = TestMemtester()
        stabilityAccountResouce = InitMemtesterResource().getStabilityMemtesterAccountResource()
        memtester_computes = stabilityAccountResouce.get_memtesterComputes()
        for compute in memtester_computes:
            testMemtester.start(compute)
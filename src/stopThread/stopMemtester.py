#!-*- coding:utf8 -*-
import threading
import os
from src.testStability.testMemtester import TestMemtester
from src.common import readJsonFromFile
from src.pojo.Compute import Compute


class StopMemtester(threading.Thread):
    def __init__(self,accountResourceFilePath):
        threading.Thread.__init__(self,name='stopMemtester')
        self._accountResourceFilePath=accountResourceFilePath

    def run(self):
        testMemtester = TestMemtester()
        memtesterAccountResource=readJsonFromFile(self._accountResourceFilePath)
        compute_array=memtesterAccountResource['_memtesterComputes']
        for compute in compute_array:
            tmp_compute=Compute()
            tmp_compute.__dict__=compute
            testMemtester.stop(tmp_compute)
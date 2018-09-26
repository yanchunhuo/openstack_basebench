#!-*- coding:utf8 -*-
from src.testStability.testMemtester import TestMemtester
from src.common.fileTool import FileTool
from src.pojo.Compute import Compute
import threading

class ReStartMemtester(threading.Thread):
    def __init__(self,accountResourceFilePath):
        threading.Thread.__init__(self,name='reStartMemtester')
        self._accountResourceFilePath=accountResourceFilePath

    def run(self):
        testMemtester = TestMemtester()
        memtesterAccountResource=FileTool.readJsonFromFile(self._accountResourceFilePath)
        compute_array=memtesterAccountResource['_memtesterComputes']
        for compute in compute_array:
            tmp_compute=Compute()
            tmp_compute.__dict__=compute
            testMemtester.reStart(tmp_compute)
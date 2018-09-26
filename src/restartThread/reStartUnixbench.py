#!-*- coding:utf8 -*-
from src.testStability.testUnixbench import TestUnixbench
from src.common.fileTool import FileTool
from src.pojo.Compute import Compute
import threading

class ReStartUnixbench(threading.Thread):
    def __init__(self,accountResourceFilePath):
        threading.Thread.__init__(self,name='reStartUnixbench')
        self._accountResourceFilePath=accountResourceFilePath

    def run(self):
        testUnixbench = TestUnixbench()
        unixbenchAccountResource=FileTool.readJsonFromFile(self._accountResourceFilePath)
        compute_array=unixbenchAccountResource['_unixbenchComputes']
        for compute in compute_array:
            tmp_compute=Compute()
            tmp_compute.__dict__=compute
            testUnixbench.reStart(tmp_compute)
#!-*- coding:utf8 -*-
from src.common.fileTool import FileTool
from src.pojo.Compute import Compute
from src.testStability.testFio import TestFio
import threading

class StopFio(threading.Thread):
    def __init__(self,accountResourceFilePath):
        threading.Thread.__init__(self,name='stopFio')
        self._accountResourceFilePath = accountResourceFilePath

    def run(self):
        testfio = TestFio()
        fioAccountResource = FileTool.readJsonFromFile(self._accountResourceFilePath)
        compute_array = fioAccountResource['_fioComputes']
        for compute in compute_array:
            tmp_compute=Compute()
            tmp_compute.__dict__=compute
            testfio.stop(tmp_compute)
#!-*- coding:utf8 -*-
import threading
from src.testStability.testFio import TestFio
from src.common import readJsonFromFile
from src.pojo.Compute import Compute


class StopFio(threading.Thread):
    def __init__(self,accountResourceFilePath):
        threading.Thread.__init__(self,name='stopFio')
        self._accountResourceFilePath = accountResourceFilePath

    def run(self):
        testfio = TestFio()
        fioAccountResource = readJsonFromFile(self._accountResourceFilePath)
        compute_array = fioAccountResource['_fioComputes']
        for compute in compute_array:
            tmp_compute=Compute()
            tmp_compute.__dict__=compute
            testfio.stop(tmp_compute)
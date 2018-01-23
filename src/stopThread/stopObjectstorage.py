#!-*- coding:utf8 -*-
import threading
from src.testStability.testObjectstore import TestObjectstore
from src.common import readJsonFromFile
from src.pojo.Compute import Compute

class StopObjectStorage(threading.Thread):
    def __init__(self,accountResourceFilePath):
        threading.Thread.__init__(self,name='stopObjectStorage')
        self._accountResourceFilePath = accountResourceFilePath

    def run(self):
        testobjectstore = TestObjectstore()
        objectstoreAccountResource = readJsonFromFile(self._accountResourceFilePath)
        compute_array = objectstoreAccountResource['_objectstorage']
        for compute in compute_array:
            tmp_compute=Compute()
            tmp_compute.__dict__=compute
            testobjectstore.stop(tmp_compute)
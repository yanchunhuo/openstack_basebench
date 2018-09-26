#!-*- coding:utf8 -*-
from src.common.fileTool import FileTool
from src.pojo.Compute import Compute
from src.testStability.testObjectstore import TestObjectstore
import threading

class StopObjectStorage(threading.Thread):
    def __init__(self,accountResourceFilePath):
        threading.Thread.__init__(self,name='stopObjectStorage')
        self._accountResourceFilePath = accountResourceFilePath

    def run(self):
        testobjectstore = TestObjectstore()
        objectstoreAccountResource = FileTool.readJsonFromFile(self._accountResourceFilePath)
        compute_array = objectstoreAccountResource['_objectstorage']
        for compute in compute_array:
            tmp_compute=Compute()
            tmp_compute.__dict__=compute
            testobjectstore.stop(tmp_compute)
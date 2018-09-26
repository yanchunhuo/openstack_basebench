#!-*- coding:utf8 -*-
from src.testStability.testObjectstore import TestObjectstore
from src.common.fileTool import FileTool
from src.pojo.Compute import Compute
import threading

class RestartObjectStorage(threading.Thread):
    def __init__(self,accountResourceFilePath):
        threading.Thread.__init__(self,name='reStartObjectStorage')
        self._accountResourceFilePath=accountResourceFilePath

    def run(self):
        testobjectstorage = TestObjectstore()
        objectstoreAccountResource = FileTool.readJsonFromFile(self._accountResourceFilePath)
        compute_array = objectstoreAccountResource['_objectstorage']
        for compute in compute_array:
            tmp_compute = Compute()
            tmp_compute.__dict__=compute
            testobjectstorage.reStart(tmp_compute)

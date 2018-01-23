#!-*- coding:utf8 -*-

import threading
from src.testStability.testObjectstore import TestObjectstore
from src.testStability.initObjectstoreResource import InitObjectStoreResource

class StartObjectStorage(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self,name='startObjectstorage')

    def run(self):
        testoss = TestObjectstore()
        objectstoreAccountResource = InitObjectStoreResource().getStableObjectstoreResource()
        oss_comuputes = objectstoreAccountResource.get_objectstorageCompute()
        for compute in oss_comuputes:
            account = objectstoreAccountResource.get_account()
            project_name = account.os_project_name
            testoss.start(compute,project_name)
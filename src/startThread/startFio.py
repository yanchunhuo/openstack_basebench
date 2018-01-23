#!-*- coding:utf8 -*-
import threading
from src.testStability.testFio import TestFio
from src.testStability.initFioResource import InitFioResource

class StartFio(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self,name='startFio')

    def run(self):
        testfio = TestFio()
        fioAccountResource = InitFioResource().getStabilityPerformanceAccountResource()
        fio_comuputes = fioAccountResource.get_fioComputes()
        for compute in fio_comuputes:
            testfio.start(compute)
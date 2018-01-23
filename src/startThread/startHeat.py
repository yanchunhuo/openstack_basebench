#!-*- coding:utf8 -*-
import threading

from src.testStability.initHeatResource import InitHeatResource

class StartHeat(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self,name='startHeat')

    def run(self):
        InitHeatResource().getStabilityheatAccountResource()

#!-*- coding:utf8 -*-
from src.common.fileTool import FileTool
from src.pojo.LoadBalancer import LoadBalancer
from src.testStability.testLoadbalancer import TestLoadbalancer
import threading

class StopLoadbalancer(threading.Thread):
    def __init__(self,accountResourceFilePath):
        threading.Thread.__init__(self,name='stopLoadbalancer')
        self._accountResourceFilePath=accountResourceFilePath

    def run(self):
        testLoadbalancer=TestLoadbalancer()
        loadbalancerAccountResource=FileTool.readJsonFromFile(self._accountResourceFilePath)
        loadbalancers=loadbalancerAccountResource['_loadbalancers']

        for loadbalancer in loadbalancers:
            loadbalancer_jmeter=LoadBalancer()
            loadbalancer_jmeter.__dict__=loadbalancer['load_compute']
            testLoadbalancer.stop(loadbalancer_jmeter)
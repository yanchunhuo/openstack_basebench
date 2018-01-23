#!-*- coding:utf8 -*-
import threading
from src.testStability.testLoadbalancer import TestLoadbalancer
from src.common import readJsonFromFile
from src.pojo.LoadBalancer import LoadBalancer


class ReStartLoadbalancer(threading.Thread):
    def __init__(self,accountResourceFilePath):
        threading.Thread.__init__(self,name='reStartLoadbalancer')
        self._accountResourceFilePath=accountResourceFilePath

    def run(self):
        testLoadbalancer=TestLoadbalancer()
        loadbalancerAccountResource=readJsonFromFile(self._accountResourceFilePath)
        loadbalancers=loadbalancerAccountResource['_loadbalancers']

        for loadbalancer in loadbalancers:
            loadbalancer_jmeter=LoadBalancer()
            loadbalancer_jmeter.__dict__=loadbalancer['load_compute']
            testLoadbalancer.reStart(loadbalancer_jmeter)
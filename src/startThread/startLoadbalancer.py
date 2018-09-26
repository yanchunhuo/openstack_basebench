#!-*- coding:utf8 -*-
from src.testStability.testLoadbalancer import TestLoadbalancer
from src.testStability.initLoadbalancerResource import InitLoadbalancerResource
import threading

class StartLoadbalancer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self,name='startLoadbalancer')

    def run(self):
        testLoadbalancer=TestLoadbalancer()
        loadbalancerAccountResource=InitLoadbalancerResource().getStabilityLoadbalancerAccountResource()
        test_loadbalancers = loadbalancerAccountResource.get_loadbalancers()
        for loadbalancer in test_loadbalancers:
            testLoadbalancer.start(loadbalancer)

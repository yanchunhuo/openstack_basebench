#!-*- coding:utf8 -*-

class Trove:
    def __init__(self):
        self.name=None
        self.id=None
        self.ip=None
        self.testType=None


    @property
    def name(self):
        return self.name

    @name.setter
    def name(self,name):
        self.name=name

    @property
    def id(self):
        return self.id

    @id.setter
    def id(self,id):
        self.id=id

    @property
    def ip(self):
        return self.ip

    @ip.setter
    def ip(self,ip):
        self.ip=ip


    @property
    def testType(self):
        return self.testType

    @testType.setter
    def testType(self,testType):
        self.testType=testType


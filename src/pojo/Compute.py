#!-*- coding:utf8 -*-

class Compute:
    def __init__(self):
        self.name=None
        self.id=None
        self.ip=None
        self.float_ip=None
        self.testType=None
        self.volumeName=None
        self.volumeId=None

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
    def float_ip(self):
        return self.float_ip

    @float_ip.setter
    def float_ip(self,float_ip):
        self.float_ip=float_ip

    @property
    def testType(self):
        return self.testType

    @testType.setter
    def testType(self,testType):
        self.testType=testType

    @property
    def volumeName(self):
        return self.volumeName

    @volumeName.setter
    def volumeName(self,volumeName):
        self.volumeName=volumeName

    @property
    def volumeId(self):
        return self.volumeId

    @volumeId.setter
    def volumeId(self,volumeId):
        self.volumeId=volumeId
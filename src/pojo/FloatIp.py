#!-*- coding:utf8 -*-
class FloatIp:
    def __init__(self):
        self.id=None
        self.ip=None

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
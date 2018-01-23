#!-*- coding:utf8 -*-

class Net():
    def __init__(self):
        self.id=None
        self.name=None
        self.cidr=None

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
    def cidr(self):
        return self.cidr

    @cidr.setter
    def cidr(self,cidr):
        self.cidr=cidr

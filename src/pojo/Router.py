#!-*- coding:utf8 -*-

class Router():
    def __init__(self):
        self.id=None
        self.name=None
        self.gw=None

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, name):
        self.name = name

    @property
    def id(self):
        return self.id

    @id.setter
    def id(self, id):
        self.id = id

    @property
    def gw(self):
        return self.gw

    @gw.setter
    def gw(self,gw):
        self.gw=gw
#!-*- coding:utf8 -*-

class AdminNet:
    def __init__(self):
        self.id=None
        self.name=None

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

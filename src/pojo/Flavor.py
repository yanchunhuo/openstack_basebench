#!-*- coding:utf8 -*-

class Flavor():
    def __init__(self):
        self.id = None
        self.name = None
        self.type=None

    @property
    def type(self):
        return self.type

    @type.setter
    def type(self,type):
        self.type=type

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
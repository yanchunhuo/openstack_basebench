#!-*- coding:utf8 -*-

class Volume:
    def __init__(self):
        self.id = None
        self.name = None
        self.type=None
        self.size=None

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
    def type(self):
        return self.type

    @type.setter
    def type(self,type):
        self.type=type

    @property
    def size(self):
        return self.size

    @size.setter
    def size(self,size):
        if isinstance(size,str):
            self.size=int(size)
        if isinstance(size,int):
            self.size=size
#!-*- coding:utf8 -*-

class Router:
    def __init__(self):
        self.id=None
        self.name=None
        self.gw=None
        # 路由器端口
        self.subnet_ids=[]

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

    def add_subnet_id(self,subnet_id):
        self.subnet_ids.append(subnet_id)

    def get_subnet_ids(self):
        return self.subnet_ids
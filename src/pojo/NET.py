#!-*- coding:utf8 -*-

class Net:
    def __init__(self):
        self.id=None
        self.name=None
        self.cidr=None
        # 网络子网
        self.subnet_ids = []

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

    def add_subnet_id(self,subnet_id):
        self.subnet_ids.append(subnet_id)

    def get_subnet_ids(self):
        return self.subnet_ids

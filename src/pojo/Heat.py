#!-*- coding:utf8 -*-
class Heat:
    def __init__(self):
        self.id=None
        self.name=None
        self.net=None
        self.members = []

    @property
    def id(self):
        return self.id

    @id.setter
    def id(self,id):
        self.id=id

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self,name):
        self.name=name

    @property
    def net(self):
        return self.net

    @net.setter
    def net(self,net_obj):
        self.net=net_obj

    def add_member(self,compute_obj):
        self.members.append(compute_obj)

    def get_members(self):
        return self.members
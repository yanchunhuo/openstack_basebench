#!-*- coding:utf8 -*-
class LoadBalancer():
    def __init__(self):
        self.id=None
        self.name=None
        self.virtual_ip=None
        self.port=None
        self.net=None
        #对均衡负载器加压的云主机
        self.load_compute=None
        #均衡负载器的后端云主机
        self.members=[]

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
    def virtual_ip(self):
        return self.virtual_ip

    @virtual_ip.setter
    def virtual_ip(self,virtual_ip):
        self.virtual_ip=virtual_ip

    @property
    def port(self):
        return self.port

    @port.setter
    def port(self,port):
        self.port=port

    @property
    def net(self):
        return self.net

    @net.setter
    def net(self,net_obj):
        self.net=net_obj

    @property
    def load_compute(self):
        return self.load_compute

    @load_compute.setter
    def load_compute(self,compute_obj):
        self.load_compute=compute_obj

    def add_member(self,compute_obj):
        self.members.append(compute_obj)

    def get_members(self):
        return self.members
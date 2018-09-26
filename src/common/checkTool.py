#!-*- coding:utf8 -*-
from src.timeoutThread.checkComputeOnline import CheckComputeOnline
from src.timeoutThread.checkRemoteServiceOK import CheckRemoteServiceOK

class CheckTool:
    def __init__(self):
        pass

    @classmethod
    def is_compute_online(cls,compute_ip):
        """
        判断主机能否连通，超时时间为3000秒
        :param compute_ip:
        :return:
        """
        checkComputeOnline = CheckComputeOnline(compute_ip)
        checkComputeOnline.start()
        checkComputeOnline.join(300)
        is_online = checkComputeOnline.getIsOnline()
        if not is_online:
            checkComputeOnline.setIsOnline(True)
            return False
        elif is_online:
            return True

    @classmethod
    def is_remoteService_OK(cls,remote_ip,port):
        """
        检测服务器端口是否可用
        :param remote_ip:
        :param port:
        :return:
        """
        checkRemoteServiceOK=CheckRemoteServiceOK(remote_ip,port)
        checkRemoteServiceOK.start()
        checkRemoteServiceOK.join(300)
        is_OK=checkRemoteServiceOK.getIsOK()
        if not is_OK:
            checkRemoteServiceOK.setIsOK(True)
            return False
        elif is_OK:
            return True

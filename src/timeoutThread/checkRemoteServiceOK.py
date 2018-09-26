#!-*- coding:utf8 -*-
import socket
import threading
import time

class CheckRemoteServiceOK(threading.Thread):
    def __init__(self,remote_ip,port):
        threading.Thread.__init__(self,name='checkRemoteServiceOK')
        self.setDaemon(True)
        self._remote_ip=remote_ip
        self._port=port
        self._is_OK=False
        self._sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        while not self._is_OK:
            time.sleep(0.5)
            try:
                self._sk.connect((self._remote_ip, int(self._port)))
                self._is_OK=True
                self._sk.close()
            except Exception:
                pass

    def setIsOK(self,is_OK):
        self._is_OK=is_OK

    def getIsOK(self):
        return self._is_OK

#!-*- coding:utf8 -*-
import threading
import time
import subprocess

class CheckComputeOnline(threading.Thread):
    def __init__(self,compute_ip):
        threading.Thread.__init__(self,name='checkComputeOnline')
        self.setDaemon(True)
        self._compute_ip=compute_ip
        self._is_online=False

    def run(self):
        command = "ping -c 10 "+self._compute_ip+"|grep -i '10 received'|wc -l"
        while not self._is_online:
            time.sleep(0.5)
            tmp_result= subprocess.check_output(command, shell=True)
            tmp_result = tmp_result.strip()
            if tmp_result == '1':
                self._is_online = True


    def setIsOnline(self,is_online):
        self._is_online=is_online

    def getIsOnline(self):
        return self._is_online
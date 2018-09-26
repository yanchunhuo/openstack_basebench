#!-*- coding:utf8 -*-
import subprocess
import threading
import time

class CheckComputeRunSucc(threading.Thread):
    def __init__(self,compute_id,command):
        threading.Thread.__init__(self,name='checkComputeRun')
        self.setDaemon(True)
        self._compute_id=compute_id
        self._command=command
        self._is_succ=False

    def run(self):
        while not self._is_succ:
            time.sleep(0.5)
            tmp_result= subprocess.check_output(self._command, shell=True)
            tmp_result=tmp_result.strip()
            if tmp_result=='ACTIVE':
                self._is_succ=True

    def setIsSucc(self,is_succ):
        self._is_succ=is_succ

    def getIsSucc(self):
        return self._is_succ

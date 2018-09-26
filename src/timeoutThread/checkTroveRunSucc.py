#!-*- coding:utf8 -*-
import threading
import time
import subprocess

class CheckTroveRunSucc(threading.Thread):
    def __init__(self,trove_id,command):
        threading.Thread.__init__(self,name='checkTroveRunSucc')
        self.setDaemon(True)
        self._trove_id=trove_id
        self._command=command
        self._is_succ=False

    def run(self):
        while not self._is_succ:
            time.sleep(5)
            tmp_result= subprocess.check_output(self._command, shell=True)
            tmp_result=tmp_result.strip()
            if tmp_result=='ACTIVE':
                self._is_succ=True

    def setIsSucc(self,is_succ):
        self._is_succ=is_succ

    def getIsSucc(self):
        return self._is_succ
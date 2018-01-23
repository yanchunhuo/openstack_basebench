#!-*- coding:utf8 -*-
import threading
import time
import subprocess

class CheckTroveDel(threading.Thread):
    def __init__(self,trove_id,command):
        threading.Thread.__init__(self,name='checkTroveDel')
        self.setDaemon(True)
        self._trove_id=trove_id
        self._command=command
        self._is_succ=False

    def run(self):
        while not self._is_succ:
            time.sleep(0.5)
            has_trove = subprocess.check_output(self._command, shell=True)
            has_trove=has_trove.strip()
            if not has_trove:
                self._is_succ=True

    def setIsSucc(self,is_succ):
        self._is_succ=is_succ

    def getIsSucc(self):
        return self._is_succ
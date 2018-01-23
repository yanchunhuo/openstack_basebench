#!-*- coding:utf8 -*-
import threading
import time
import subprocess

class CheckAllComputeDel(threading.Thread):
    def __init__(self,compute_ids,command):
        threading.Thread.__init__(self,name='checkAllComputeDel')
        self.setDaemon(True)
        self._compute_ids=compute_ids
        self._command=command
        self._is_succ=False

    def run(self):
        while not self._is_succ:
            time.sleep(0.5)
            has_compute = subprocess.check_output(self._command, shell=True)
            has_compute=has_compute.strip()
            if not has_compute:
                self._is_succ=True

    def setIsSucc(self,is_succ):
        self._is_succ=is_succ

    def getIsSucc(self):
        return self._is_succ





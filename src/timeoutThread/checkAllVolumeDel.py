#!-*- coding:utf8 -*-
import threading
import time
import subprocess

class CheckAllVolumeDel(threading.Thread):
    def __init__(self,volume_ids,command):
        threading.Thread.__init__(self,name='checkAllVolumeDel')
        self.setDaemon(True)
        self._volume_ids=volume_ids
        self._command=command
        self._is_succ=False

    def run(self):
        while not self._is_succ:
            time.sleep(0.5)
            has_volume = subprocess.check_output(self._command, shell=True)
            has_volume=has_volume.strip()
            if not has_volume:
                self._is_succ=True

    def setIsSucc(self,is_succ):
        self._is_succ=is_succ

    def getIsSucc(self):
        return self._is_succ





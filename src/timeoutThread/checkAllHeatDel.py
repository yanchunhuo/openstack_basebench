#!-*- coding:utf8 -*-
import threading
import time
import subprocess

class CheckAllHeatDel(threading.Thread):

    def __init__(self,heat_ids,command):
        """
        :param heat_ids:
        :param command:
        """
        threading.Thread.__init__(self,name='checkAllHeatDel')
        self.setDaemon(True)
        self._heat_ids = heat_ids
        self._command = command
        self._is_succ = False

    def run(self):
        while not self._is_succ:
            time.sleep(0.5)
            has_heat = subprocess.check_output(self._command, shell=True)
            has_heat=has_heat.strip()
            if not has_heat:
                self._is_succ=True

    def setIsSucc(self,is_succ):
        self._is_succ=is_succ

    def getIsSucc(self):
        return self._is_succ

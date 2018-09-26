#!-*- coding:utf8 -*-
import threading
import time
import subprocess

class CheckAllHeatRunSucc(threading.Thread):

    def __init__(self,heat_id,commad):
        """
        :param heat_id:
        :param commad:
        """
        threading.Thread.__init__(self,name='checkHeatRun')
        self.setDaemon(True)
        self._heat_id = heat_id
        self._commad = commad
        self._is_succ = False

    def run(self):
        while not self._is_succ:
            time.sleep(0.5)
            tmp_result = subprocess.check_output(self._commad,shell=True)
            tmp_result = tmp_result.strip()
            if tmp_result == 'CREATE_COMPLETE':
                self._is_succ = True

    def setIsSucc(self,is_succ):
        self._is_succ = is_succ

    def getIsSucc(self):
        return self._is_succ

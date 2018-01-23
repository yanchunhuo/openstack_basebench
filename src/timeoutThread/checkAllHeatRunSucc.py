#!-*- coding:utf8 -*-
import threading
import time
import subprocess
from src.logger import logger

class CheckAllHeatRunSucc(threading.Thread):

    def __init__(self,heat_id,commad):
        '''
        :param heat_id:
        :param commad:
        '''
        threading.Thread.__init__(self,name='checkHeatRun')
        self.setDaemon(True)
        self._heat_id = heat_id
        self._commad = commad
        self._is_succ = False

    def run(self):
        while not self._is_succ:
            logger.info('检测伸缩组'+self._heat_id+'是否处于运行状态...')
            time.sleep(0.5)
            try:
                tmp_result = subprocess.check_output(self._commad,shell=True)
                tmp_result = tmp_result.strip()
                if tmp_result == 'CREATE_COMPLETE':
                    logger.info('伸缩组' + self._heat_id + '处于运行状态!')
                    self._is_succ = True
            except Exception,e:
                logger.info('未知异常,无法检测伸缩组'+self._heat_id+'运行状态'+'\r\n'+e.message)

    def setIsSucc(self,is_succ):
        self._is_succ = is_succ

    def getIsSucc(self):
        return self._is_succ

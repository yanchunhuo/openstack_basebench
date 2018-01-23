#!-*- coding:utf8 -*-
import threading
import time
import subprocess
from src.logger import logger

class CheckAllHeatDel(threading.Thread):

    def __init__(self,heat_ids,command):
        '''
        :param heat_ids:
        :param command:
        '''
        threading.Thread.__init__(self,name='checkAllHeatDel')
        self.setDaemon(True)
        self._heat_ids = heat_ids
        self._command = command
        self._is_succ = False

    def run(self):
        while not self._is_succ:
            logger.info('检测伸缩组' + self._heat_ids.__str__() + '是否已全部删除完成...')
            time.sleep(0.5)
            try:
                has_heat = subprocess.check_output(self._command, shell=True)
                has_heat=has_heat.strip()
                if not has_heat:
                    logger.info('伸缩组'+self._heat_ids.__str__() + '已全部删除完成')
                    self._is_succ=True
            except Exception,e:
                logger.error('未知异常，无法检测伸缩组' +self._heat_ids.__str__() + '删除完成情况' + '\r\n' + e.message)

    def setIsSucc(self,is_succ):
        self._is_succ=is_succ

    def getIsSucc(self):
        return self._is_succ

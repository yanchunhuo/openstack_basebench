#!-*- coding:utf8 -*-
from src.clients.sshClient import SSHClient
from src.common import is_compute_online
from src.logger import stabilityMemtesterLogger
from config.config import STABILITY_TEST_MEMTESTER_MEM
from config.config import STABILITY_TEST_MEMTESTER_TIMES


class TestMemtester():
    def __init__(self):
        pass

    def start(self,compute_obj):
        """
        对云主机进行memtester测试
        :param compute_obj:
        :return:
        """
        if not compute_obj.float_ip:
            stabilityMemtesterLogger.error('云主机'+compute_obj.name+'的浮动ip为空,无法进行memtester测试')
            return
        compute_float_ip=compute_obj.float_ip
        compute_name=compute_obj.name

        stabilityMemtesterLogger.info('开始检测云主机'+compute_name+'的ip:'+compute_float_ip+'是否可连通')
        is_online=is_compute_online(compute_float_ip)
        if not is_online:
            return

        #获得ssh连接对象
        sshclient=SSHClient(compute_float_ip)

        stabilityMemtesterLogger.info('开始memtester测试,云主机' + compute_name)
        test_command = 'nohup memtester '+str(STABILITY_TEST_MEMTESTER_MEM)+' '+str(STABILITY_TEST_MEMTESTER_TIMES)+' >nohup.out 2>&1 &'
        stdin, stdout, stderr, exit_code=sshclient.ssh_exec_command(command=test_command, timeout=20)
        if exit_code:
            stabilityMemtesterLogger.error('memster测试云主机' + compute_name + '启动失败' + '\r\n' + stderr.read())

        # 关闭ssh
        sshclient.closeSSHAndSFTP()

    def stop(self,compute_obj):
        """
        停止云主机的memtester测试
        :param compute_obj:
        :return:
        """
        if not compute_obj.float_ip:
            stabilityMemtesterLogger.error('云主机'+compute_obj.name.encode('utf-8')+'的浮动ip为空,无法停止memtester测试')
            return
        compute_float_ip = compute_obj.float_ip.encode('utf-8')
        compute_name = compute_obj.name.encode('utf-8')

        stabilityMemtesterLogger.info('开始检测云主机' + compute_name + '的ip:' + compute_float_ip + '是否可连通')
        is_online = is_compute_online(compute_float_ip)
        if not is_online:
            return

        # 获得ssh连接对象
        sshclient = SSHClient(compute_float_ip)

        stabilityMemtesterLogger.info('开始停止memtester测试,云主机' + compute_name)
        stop_command = "kill -9 `ps -A |grep memtester|awk '{print $1}'`"
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command=stop_command, timeout=20)
        if exit_code:
            stabilityMemtesterLogger.error('停止云主机' + compute_name + 'memtester测试失败' + '\r\n' + stderr.read())

        # 关闭ssh
        sshclient.closeSSHAndSFTP()


    def reStart(self,compute_obj):
        """
        对云主机进行memtester测试
        :param compute_obj:
        :return:
        """
        if not compute_obj.float_ip:
            stabilityMemtesterLogger.error('云主机'+compute_obj.name.encode('utf-8')+'的浮动ip为空,无法重启memtester测试')
            return
        compute_float_ip=compute_obj.float_ip.encode('utf-8')
        compute_name=compute_obj.name.encode('utf-8')

        stabilityMemtesterLogger.info('开始检测云主机'+compute_name+'的ip:'+compute_float_ip+'是否可连通')
        is_online=is_compute_online(compute_float_ip)
        if not is_online:
            return

        #获得ssh连接对象
        sshclient=SSHClient(compute_float_ip)

        stabilityMemtesterLogger.info('重启memtester测试,云主机' + compute_name)
        test_command = 'nohup memtester '+str(STABILITY_TEST_MEMTESTER_MEM)+' '+str(STABILITY_TEST_MEMTESTER_TIMES)+' >nohup.out 2>&1 &'
        stdin, stdout, stderr, exit_code=sshclient.ssh_exec_command(command=test_command, timeout=20)
        if exit_code:
            stabilityMemtesterLogger.error('memster测试云主机' + compute_name + '重启失败' + '\r\n' + stderr.read())

        # 关闭ssh
        sshclient.closeSSHAndSFTP()

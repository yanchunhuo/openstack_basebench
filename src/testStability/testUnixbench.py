#!-*- coding:utf8 -*-
from src.clients.sshClient import SSHClient
from src.common import is_compute_online
from src.logger import stabilityUnixbenchLogger
from config.config import STABILITY_TEST_UNIXBENCH_CPU
from config.config import STABILITY_TEST_UNIXBENCH_TIMES


class TestUnixbench():
    def __init__(self):
        pass

    def start(self,compute_obj):
        """
        对云主机进行unixbench测试
        :param compute_obj:
        :return:
        """
        if not compute_obj.float_ip:
            stabilityUnixbenchLogger.error('云主机'+compute_obj.name+'的浮动ip为空,无法进行unixbench测试')
            return
        compute_float_ip=compute_obj.float_ip
        compute_name=compute_obj.name

        stabilityUnixbenchLogger.info('开始检测云主机'+compute_name+'的ip:'+compute_float_ip+'是否可连通')
        try:
            is_online=is_compute_online(compute_float_ip)
        except Exception,e:
            stabilityUnixbenchLogger.error('检测云主机' + compute_name + '的ip:' + compute_float_ip + '无法连通'+ '\r\n' + e.message)
            return

        #获得ssh连接对象
        sshclient=SSHClient(compute_float_ip)

        stabilityUnixbenchLogger.info('开始unixbench测试,云主机' + compute_name)
        test_command = 'cd /root/soft/unixbench;nohup ./Run -c ' + str(STABILITY_TEST_UNIXBENCH_CPU) + ' -i ' + str(STABILITY_TEST_UNIXBENCH_TIMES) + ' >nohup.out 2>&1 &'
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command=test_command, timeout=20)
        if exit_code:
            stabilityUnixbenchLogger.error('unixbench测试云主机' + compute_name + '启动失败' + '\r\n' + stderr.read())

        # 关闭ssh
        sshclient.closeSSHAndSFTP()

    def stop(self,compute_obj):
        """
        停止云主机的unixbench测试
        :param compute_obj:
        :return:
        """
        if not compute_obj.float_ip:
            stabilityUnixbenchLogger.error('云主机'+compute_obj.name+'的浮动ip为空,无法停止unixbench测试')
            return
        compute_float_ip = compute_obj.float_ip.encode('utf-8')
        compute_name = compute_obj.name.encode('utf-8')

        stabilityUnixbenchLogger.info('开始检测云主机' + compute_name + '的ip:' + compute_float_ip + '是否可连通')
        try:
            is_online = is_compute_online(compute_float_ip)
        except Exception,e:
            stabilityUnixbenchLogger.error('检测云主机' + compute_name + '的ip:' + compute_float_ip + '无法连通'+ '\r\n' + e.message)
            return

        # 获得ssh连接对象
        sshclient = SSHClient(compute_float_ip)

        stabilityUnixbenchLogger.info('开始停止unixbench测试,云主机' + compute_name)
        stop_command = "cd /root/soft/unixbench/tmp;./kill_run"
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command=stop_command, timeout=20)
        if exit_code:
            stabilityUnixbenchLogger.error('停止云主机' + compute_name + 'unixbench测试失败' + '\r\n' + stderr.read())

        # 关闭ssh
        sshclient.closeSSHAndSFTP()

    def reStart(self,compute_obj):
        """
        对云主机进行unixbench测试
        :param compute_obj:
        :return:
        """
        if not compute_obj.float_ip:
            stabilityUnixbenchLogger.error('云主机'+compute_obj.name+'的浮动ip为空,无法重启unixbench测试')
            return
        compute_float_ip=compute_obj.float_ip.encode('utf-8')
        compute_name=compute_obj.name.encode('utf-8')

        stabilityUnixbenchLogger.info('开始检测云主机'+compute_name+'的ip:'+compute_float_ip+'是否可连通')
        try:
            is_online=is_compute_online(compute_float_ip)
        except Exception,e:
            stabilityUnixbenchLogger.info('检测云主机' + compute_name + '的ip:' + compute_float_ip + '无法连通'+ '\r\n' + e.message)
            return

        #获得ssh连接对象
        sshclient=SSHClient(compute_float_ip)

        stabilityUnixbenchLogger.info('重启unixbench测试,云主机' + compute_name)
        test_command = 'cd /root/soft/unixbench;nohup ./Run -c ' + str(STABILITY_TEST_UNIXBENCH_CPU) + ' -i ' + str(STABILITY_TEST_UNIXBENCH_TIMES) + ' >nohup.out 2>&1 &'
        stdin, stdout, stderr, exit_code=sshclient.ssh_exec_command(command=test_command, timeout=20)
        if exit_code:
            stabilityUnixbenchLogger.error('unixbench测试云主机' + compute_name + '重启失败' + '\r\n' + stderr.read())

        # 关闭ssh
        sshclient.closeSSHAndSFTP()


#!-*- coding:utf8 -*-
from src.clients.sshClient import SSHClient
from src.common.checkTool import CheckTool
from src.loggers import Loggers
from src.readConfig import ReadConfig

class TestUnixbench:
    def __init__(self):
        self._loggers=Loggers()
        self._readConfig=ReadConfig()

    def start(self,compute_obj):
        """
        对云主机进行unixbench测试
        :param compute_obj:
        :return:
        """
        if not compute_obj.float_ip:
            self._loggers.stabilityUnixbenchLogger.error('云主机'+compute_obj.name+'的浮动ip为空,无法进行unixbench测试')
            return
        compute_float_ip=compute_obj.float_ip
        compute_name=compute_obj.name

        self._loggers.stabilityUnixbenchLogger.info('开始检测云主机'+compute_name+'浮动ip:'+compute_float_ip+'是否可连通')
        is_online=CheckTool.is_compute_online(compute_float_ip)
        if not is_online:
            self._loggers.stabilityUnixbenchLogger.error('检测到云主机' + compute_name + '浮动ip:' + compute_float_ip + '无法连通')
            return

        # 检测云主机22端口是否可用
        is_port_OK = CheckTool.is_remoteService_OK(compute_float_ip, 22)
        if not is_port_OK:
            self._loggers.stabilityUnixbenchLogger.error('检测到云主机' + compute_name + '浮动ip:' + compute_float_ip + '的22端口不可用!')
            return

        #获得ssh连接对象
        sshclient=SSHClient(compute_float_ip)

        self._loggers.stabilityUnixbenchLogger.info('开始unixbench测试,云主机' + compute_name)
        test_command = 'cd /root/soft/unixbench;nohup ./Run -c ' + self._readConfig.executeTest.stability_test_unixbench_cpu + ' -i ' + self._readConfig.executeTest.stability_test_unixbench_times + ' >nohup.out 2>&1 &'
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command=test_command, timeout=20)
        if exit_code:
            self._loggers.stabilityUnixbenchLogger.error('unixbench测试云主机' + compute_name + '启动失败' + '\r\n' + stderr.read())

        # 关闭ssh
        sshclient.closeSSHAndSFTP()

    def stop(self,compute_obj):
        """
        停止云主机的unixbench测试
        :param compute_obj:
        :return:
        """
        if not compute_obj.float_ip:
            self._loggers.stabilityUnixbenchLogger.error('云主机'+compute_obj.name+'的浮动ip为空,无法停止unixbench测试')
            return
        compute_float_ip = compute_obj.float_ip.encode('utf-8')
        compute_name = compute_obj.name.encode('utf-8')

        self._loggers.stabilityUnixbenchLogger.info('开始检测云主机' + compute_name + '的浮动ip:' + compute_float_ip + '是否可连通')
        is_online = CheckTool.is_compute_online(compute_float_ip)
        if not is_online:
            self._loggers.stabilityUnixbenchLogger.error('检测到云主机' + compute_name + '的浮动ip:' + compute_float_ip + '无法连通')
            return

        # 检测云主机22端口是否可用
        is_port_OK = CheckTool.is_remoteService_OK(compute_float_ip, 22)
        if not is_port_OK:
            self._loggers.stabilityUnixbenchLogger.error('检测到云主机' + compute_name + '浮动ip:' + compute_float_ip + '的22端口不可用!')
            return

        # 获得ssh连接对象
        sshclient = SSHClient(compute_float_ip)

        self._loggers.stabilityUnixbenchLogger.info('开始停止unixbench测试,云主机' + compute_name)
        stop_command = "cd /root/soft/unixbench/tmp;./kill_run"
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command=stop_command, timeout=20)
        if exit_code:
            self._loggers.stabilityUnixbenchLogger.error('停止云主机' + compute_name + 'unixbench测试失败' + '\r\n' + stderr.read())

        # 关闭ssh
        sshclient.closeSSHAndSFTP()

    def reStart(self,compute_obj):
        """
        对云主机进行unixbench测试
        :param compute_obj:
        :return:
        """
        if not compute_obj.float_ip:
            self._loggers.stabilityUnixbenchLogger.error('云主机'+compute_obj.name+'的浮动ip为空,无法重启unixbench测试')
            return
        compute_float_ip=compute_obj.float_ip.encode('utf-8')
        compute_name=compute_obj.name.encode('utf-8')

        self._loggers.stabilityUnixbenchLogger.info('开始检测云主机'+compute_name+'浮动ip:'+compute_float_ip+'是否可连通')
        is_online=CheckTool.is_compute_online(compute_float_ip)
        if not is_online:
            self._loggers.stabilityUnixbenchLogger.error('检测到云主机' + compute_name + '浮动ip:' + compute_float_ip + '无法连通')
            return

        # 检测云主机22端口是否可用
        is_port_OK = CheckTool.is_remoteService_OK(compute_float_ip, 22)
        if not is_port_OK:
            self._loggers.stabilityUnixbenchLogger.error('检测到云主机' + compute_name + '浮动ip:' + compute_float_ip + '的22端口不可用!')
            return

        #获得ssh连接对象
        sshclient=SSHClient(compute_float_ip)

        self._loggers.stabilityUnixbenchLogger.info('重启unixbench测试,云主机' + compute_name)
        test_command = 'cd /root/soft/unixbench;nohup ./Run -c ' + self._readConfig.executeTest.stability_test_unixbench_cpu + ' -i ' + self._readConfig.executeTest.stability_test_unixbench_times + ' >nohup.out 2>&1 &'
        stdin, stdout, stderr, exit_code=sshclient.ssh_exec_command(command=test_command, timeout=20)
        if exit_code:
            self._loggers.stabilityUnixbenchLogger.error('unixbench测试云主机' + compute_name + '重启失败' + '\r\n' + stderr.read())

        # 关闭ssh
        sshclient.closeSSHAndSFTP()


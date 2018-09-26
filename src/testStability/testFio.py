#!-*- coding:utf8 -*-
from src.clients.sshClient import SSHClient
from src.common.checkTool import CheckTool
from src.loggers import Loggers
from src.readConfig import ReadConfig

class TestFio:
    def __init__(self):
        self._loggers=Loggers()
        self._readConfig=ReadConfig()

    def start(self,compute_obj):
        """
        启动fio测试
        :param compute_obj:
        :return:
        """
        if not compute_obj.float_ip:
            self._loggers.stabilityFioLogger.error('云主机' + compute_obj.name + '的浮动ip为空,无法重启fio测试')
            return
        compute_float_ip = compute_obj.float_ip
        compute_name = compute_obj.name
        compute_testType=compute_obj.testType

        self._loggers.stabilityFioLogger.info('开始检测云主机'+compute_name+'浮动ip:'+compute_float_ip+'是否可连通')
        is_online = CheckTool.is_compute_online(compute_float_ip)
        if not is_online:
            self._loggers.stabilityFioLogger.error('检测到云主机' + compute_name + '浮动ip:' + compute_float_ip + '无法连通')
            return

        # 检测云主机22端口是否可用
        is_port_OK = CheckTool.is_remoteService_OK(compute_float_ip,22)
        if not is_port_OK:
            self._loggers.stabilityFioLogger.error('检测到云主机' + compute_name + '浮动ip:' + compute_float_ip + '的22端口不可用!')
            return

        # 获得ssh连接对象
        sshclient = SSHClient(compute_float_ip)

        # 格式化云硬盘
        self._loggers.stabilityFioLogger.info('格式化云主机' + compute_name + '的云硬盘/dev/vdc')
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command='mkfs -t ext4 /dev/vdc', timeout=1200)
        if exit_code:
            self._loggers.stabilityFioLogger.error('格式化云主机' + compute_name + '的云硬盘/dev/vdc失败!' + '\r\n' + stderr.read())
            return

        # 创建挂载目录
        self._loggers.stabilityFioLogger.info('创建云主机'+compute_name+'云硬盘的挂载目录/root/test')
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command='mkdir -p /root/test')
        if exit_code:
            self._loggers.stabilityFioLogger.error('创建云主机云' + compute_name + '硬盘挂载目录/root/test失败!' + '\r\n' + stderr.read())
            return

        # 挂载云硬盘
        self._loggers.stabilityFioLogger.info('为云主机' + compute_name + '挂载云硬盘/dev/vdc')
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command='mount /dev/vdc /root/test',timeout=20)
        if exit_code:
            self._loggers.stabilityFioLogger.error('为云主机' + compute_name + '挂载云硬盘/dev/vdc失败!+\r\n' + stderr.read())
            return

        # 创建测试结果保存目录
        self._loggers.stabilityFioLogger.info('在云主机' + compute_name + '里创建结果保存目录/root/result')
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command='mkdir -p /root/result')
        if exit_code:
            self._loggers.stabilityFioLogger.error('在云主机' + compute_name + '里创建结果保存目录/root/result失败!' + '\r\n' + stderr.read())
            return

        # 执行命令
        self._loggers.stabilityFioLogger.info('开始fio稳定性测试,云主机' + compute_name + ',测试类型' + compute_testType )
        test_command = 'cd /root/test/;nohup fio -filename=test' + compute_testType + ' -direct=1 -iodepth 128 -thread -rw=' + compute_testType + ' -ioengine=libaio -bs=4k -size=' + \
                       self._readConfig.executeTest.stability_test_fio_volume_size + 'G -numjobs=10 -runtime='+self._readConfig.executeTest.stability_test_fio_seconds + ' -name=' + compute_testType + '-libaio -group_reporting --output /root/result/'+ compute_name+'_output.html > nohup.out 2>&1 &'
        stdin,stdin,stderr,exit_code = sshclient.ssh_exec_command(command=test_command,timeout=20)
        if exit_code:
            self._loggers.stabilityFioLogger.error('fio测试云主机' + compute_name + '测试' + compute_testType + '失败!' + '\r\n' + stderr.read())

        # 关闭ssh
        sshclient.closeSSHAndSFTP()

    def stop(self,compute_obj):
        """
        停止fio测试
        :param compute_obj:
        :return:
        """
        if not compute_obj.float_ip:
            self._loggers.stabilityFioLogger.error('云主机' + compute_obj.name + '的浮动ip为空,无法重启fio测试')
            return
        compute_float_ip = compute_obj.float_ip.encode('utf-8')
        compute_name = compute_obj.name.encode('utf-8')

        self._loggers.stabilityFioLogger.info('开始检测云主机' + compute_name + '浮动ip:' + compute_float_ip + '是否可连通')
        is_online = CheckTool.is_compute_online(compute_float_ip)
        if not is_online:
            self._loggers.stabilityFioLogger.error('检测到云主机' + compute_name + '浮动ip:' + compute_float_ip + '无法连通')
            return

        # 检测云主机22端口是否可用
        is_port_OK = CheckTool.is_remoteService_OK(compute_float_ip, 22)
        if not is_port_OK:
            self._loggers.stabilityFioLogger.error('检测到云主机' + compute_name + '浮动ip:' + compute_float_ip + '的22端口不可用!')
            return

        # 获得ssh连接对象
        sshclient = SSHClient(compute_float_ip)

        self._loggers.stabilityFioLogger.info('开始停止fio测试,云主机' + compute_name)
        stop_command = "kill -9 `ps -A |grep fio|awk '{print $1}'`"
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command=stop_command, timeout=20)
        if exit_code:
            self._loggers.stabilityFioLogger.error('停止云主机' + compute_name + 'fio测试失败' + '\r\n' + stderr.read())

        # 关闭ssh
        sshclient.closeSSHAndSFTP()

    def reStart(self, compute_obj):
        """
        重启fio测试
        :param compute_obj:
        :return:
        """
        if not compute_obj.float_ip:
            self._loggers.stabilityFioLogger.error('云主机' + compute_obj.name + '的浮动ip为空,无法重启fio测试')
            return
        compute_float_ip = compute_obj.float_ip.encode('utf-8')
        compute_name = compute_obj.name.encode('utf-8')
        compute_testType = compute_obj.testType.encode('utf-8')

        self._loggers.stabilityFioLogger.info('开始检测云主机' + compute_name + '浮动ip:' + compute_float_ip + '是否可连通')
        is_online = CheckTool.is_compute_online(compute_float_ip)
        if not is_online:
            self._loggers.stabilityFioLogger.error('检测到云主机' + compute_name + '浮动ip:' + compute_float_ip + '无法连通')
            return

        # 检测云主机22端口是否可用
        is_port_OK = CheckTool.is_remoteService_OK(compute_float_ip, 22)
        if not is_port_OK:
            self._loggers.stabilityFioLogger.error('检测到云主机' + compute_name + '浮动ip:' + compute_float_ip + '的22端口不可用!')
            return

        # 获得ssh连接对象
        sshclient = SSHClient(compute_float_ip)

        self._loggers.stabilityFioLogger.info('重启fio测试,云主机' + compute_name)
        # 删除测试文件
        del_command = 'cd /root/test/;rm -rf test*'
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command=del_command, timeout=3600)
        if exit_code:
            self._loggers.stabilityFioLogger.error('fio测试后删除云主机' + compute_name + '的测试文件' + compute_testType + '失败!' + '\r\n' + stderr.read())

        # 卸载云硬盘
        umount_command = 'cd /root;umount /dev/vdc'
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command=umount_command, timeout=20)
        if exit_code:
            self._loggers.stabilityFioLogger.error('卸载云主机' + compute_name + '的云硬盘/dev/vdc失败!' + '\r\n' + stderr.read())

        # 格式化云硬盘
        self._loggers.stabilityFioLogger.info('格式化云主机' + compute_name + '的云硬盘/dev/vdc')
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command='mkfs -t ext4 /dev/vdc', timeout=3600)
        if exit_code:
            self._loggers.stabilityFioLogger.error('格式化云主机' + compute_name + '的云硬盘/dev/vdc失败!' + '\r\n' + stderr.read())
            return

        # 挂载云硬盘
        self._loggers.stabilityFioLogger.info('为云主机' + compute_name + '挂载云硬盘/dev/vdc')
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command='mount /dev/vdc /root/test', timeout=20)
        if exit_code:
            self._loggers.stabilityFioLogger.error('为云主机' + compute_name + '挂载云硬盘/dev/vdc失败!+\r\n' + stderr.read())
            return

        # 执行测试
        self._loggers.stabilityFioLogger.info('重启fio稳定性测试,云主机' + compute_name + ',测试类型' + compute_testType)
        test_command = 'cd /root/test/;nohup fio -filename=test' + compute_testType + ' -direct=1 -iodepth 128 -thread -rw=' + compute_testType + ' -ioengine=libaio -bs=4k -size=' + \
                       self._readConfig.executeTest.stability_test_fio_volume_size + 'G -numjobs=10 -runtime=' + self._readConfig.executeTest.stability_test_fio_seconds + ' -name=' + compute_testType + '-libaio -group_reporting --output /root/result/' + compute_name + '_output.html > nohup.out 2>&1 &'
        stdin, stdin, stderr, exit_code = sshclient.ssh_exec_command(command=test_command, timeout=20)
        if exit_code:
            self._loggers.stabilityFioLogger.error('fio测试云主机' + compute_name + '测试' + compute_testType + '失败!' + '\r\n' + stderr.read())

        # 关闭ssh
        sshclient.closeSSHAndSFTP()

#!-*- coding:utf8 -*-
from src.clients.sshClient import SSHClient
from src.common.checkTool import CheckTool
from src.loggers import Loggers
from src.readConfig import ReadConfig


class TestSysbench:
    def __init__(self):
        self._loggers=Loggers()
        self._readConfig=ReadConfig()

    def start(self,compute_client,trove_server):
        """
        对两台云主机进行sysbench测试
        :param compute_client:
        :param trove_server:
        :return:
        """

        if not compute_client.float_ip:
            self._loggers.stabilitySysbenchLogger.error('云主机' + compute_client.name + '的浮动ip为空,无法进行sysbench测试')
            return

        compute_client_float_ip=compute_client.float_ip
        #compute_server_float_ip=trove_server.float_ip
        #compute_client_ip=compute_client.ip
        trove_server_ip=trove_server.ip
        compute_client_name=compute_client.name
        trove_server_name=trove_server.name
        compute_testType=compute_client.testType

        self._loggers.stabilitySysbenchLogger.info('开始检测云主机'+compute_client_name+'浮动ip:'+compute_client_float_ip+'是否可连通')
        is_client_online=CheckTool.is_compute_online(compute_client_float_ip)

        if not is_client_online :
            self._loggers.stabilitySysbenchLogger.error('检测到云主机' + compute_client_name + '浮动ip:' + compute_client_float_ip + '无法连通')
            return

        # 检测云主机22端口是否可用
        is_port_OK = CheckTool.is_remoteService_OK(compute_client_float_ip, 22)
        if not is_port_OK:
            self._loggers.stabilitySysbenchLogger.error('检测到云主机' + compute_client_name + '浮动ip:' + compute_client_float_ip + '的22端口不可用!')
            return

        sysbench_client_sshclient=SSHClient(compute_client_float_ip)

        #关闭防火墙
        self._loggers.stabilitySysbenchLogger.info('关闭云主机'+compute_client_name+'的防火墙')
        sysbench_client_sshclient.ssh_exec_command('service iptables stop',30)

        self._loggers.stabilitySysbenchLogger.info('开始测试sysbench,测试类型'+compute_testType)
        #启动客户端开始测试
        stdin,stdout,stderr,exit_code=sysbench_client_sshclient.ssh_exec_command(command='nohup sysbench /usr/local/share/sysbench/oltp_read_write.lua --db-driver=mysql --threads=100 --tables=20 --table_size=100000000  --mysql-user=test --mysql-password=123456..  --mysql-host='+trove_server_ip+' --mysql-port=3306 --mysql-db=sbtest prepare >nohup.out 2>&1 &',timeout=20)
        if exit_code:
            self._loggers.stabilitySysbenchLogger.error('使用sysbench测试'+trove_server_name+'失败!')
            return

        # 关闭ssh
        sysbench_client_sshclient.closeSSHAndSFTP()


    def stop(self,compute_client):
        """
        停止两台云主机进行sysbench测试
        :param compute_client:
        :return:
        """
        if not compute_client.float_ip:
            self._loggers.stabilitySysbenchLogger.error('云主机' + compute_client.name + '的浮动ip为空,无法停止sysbench测试')
            return

        compute_client_float_ip=compute_client.float_ip.encode('utf-8')
        compute_client_name=compute_client.name.encode('utf-8')
        #trove_server_name=trove_server.name.encode('utf-8')

        self._loggers.stabilitySysbenchLogger.info('开始检测数据库实例'+compute_client_name+'浮动ip:'+compute_client_float_ip+'是否可连通')
        is_client_online=CheckTool.is_compute_online(compute_client_float_ip)

        if not is_client_online :
            self._loggers.stabilitySysbenchLogger.error('检测到云主机' + compute_client_name + '浮动ip:' + compute_client_float_ip + '无法连通')
            return

        # 检测云主机22端口是否可用
        is_port_OK = CheckTool.is_remoteService_OK(compute_client_float_ip, 22)
        if not is_port_OK:
            self._loggers.stabilitySysbenchLogger.error('检测到云主机' + compute_client_name + '浮动ip:' + compute_client_float_ip + '的22端口不可用!')
            return

        sysbench_client_sshclient=SSHClient(compute_client_float_ip)

        #关闭防火墙
        self._loggers.stabilitySysbenchLogger.info('关闭云主机'+compute_client_name+'的防火墙')
        sysbench_client_sshclient.ssh_exec_command('service iptables stop',30)


        #关闭客户端程序
        self._loggers.stabilitySysbenchLogger.info('停止sysbench测试')
        stdin, stdout, stderr, exit_code=sysbench_client_sshclient.ssh_exec_command(command="kill -9 `ps -A |grep sysbench| awk '{print $1}'`",timeout=10)
        if exit_code:
            self._loggers.stabilitySysbenchLogger.error('关闭sysbench客户端进程失败')

        # 关闭ssh
        sysbench_client_sshclient.closeSSHAndSFTP()


    def reStart(self,compute_client,trove_server):
        """
        对两台云主机进行sysbench测试
        :param compute_client:
        :param trove_server:
        :return:
        """
        if not compute_client.float_ip:
            self._loggers.stabilitySysbenchLogger.error('云主机' + compute_client.name + '的浮动ip为空,无法进行重启sysbench测试')
            return

        compute_client_float_ip = compute_client.float_ip.encode('utf-8')
        # compute_server_float_ip=trove_server.float_ip
        # compute_client_ip=compute_client.ip
        trove_server_ip = trove_server.ip.encode('utf-8')
        compute_client_name = compute_client.name.encode('utf-8')
        trove_server_name = trove_server.name.encode('utf-8')
        compute_testType = compute_client.testType.encode('utf-8')

        self._loggers.stabilitySysbenchLogger.info('开始检测云主机' + compute_client_name + '浮动ip:' + compute_client_float_ip + '是否可连通')
        is_client_online = CheckTool.is_compute_online(compute_client_float_ip)

        if not is_client_online:
            self._loggers.stabilitySysbenchLogger.error('检测到云主机' + compute_client_name + '浮动ip:' + compute_client_float_ip + '无法连通')
            return

        # 检测云主机22端口是否可用
        is_port_OK = CheckTool.is_remoteService_OK(compute_client_float_ip, 22)
        if not is_port_OK:
            self._loggers.stabilitySysbenchLogger.error('检测到云主机' + compute_client_name + '浮动ip:' + compute_client_float_ip + '的22端口不可用!')
            return

        sysbench_client_sshclient = SSHClient(compute_client_float_ip)

        # 关闭防火墙
        self._loggers.stabilitySysbenchLogger.info('关闭云主机' + compute_client_name + '的防火墙')
        sysbench_client_sshclient.ssh_exec_command('service iptables stop', 30)



        self._loggers.stabilitySysbenchLogger.info('清空数据库实例' + trove_server_name + '中的数据库sbtest的数据')
        stdin, stdout, stderr, exit_code = sysbench_client_sshclient.ssh_exec_command(command='mysql -h'+ trove_server_ip + ' -utest -p123456.. -e "drop database sbtest;CREATE DATABASE  sbtest CHARACTER SET utf8 COLLATE utf8_general_ci"', timeout=100)
        if exit_code:
            self._loggers.stabilitySysbenchLogger.error('删除数据库实例' + trove_server_name + '的数据库sbtest失败!')
            return

        self._loggers.stabilitySysbenchLogger.info('重新开始测试sysbench,测试类型' + compute_testType)
        # 启动客户端开始测试
        stdin, stdout, stderr, exit_code = sysbench_client_sshclient.ssh_exec_command(command='nohup sysbench /usr/local/share/sysbench/oltp_read_write.lua --db-driver=mysql --threads=100 --tables=20 --table_size=100000000  --mysql-user=test --mysql-password=123456..  --mysql-host=' + trove_server_ip + ' --mysql-port=3306 --mysql-db=sbtest prepare >nohup.out 2>&1 &',timeout=20)
        if exit_code:
            self._loggers.stabilitySysbenchLogger.error('使用sysbench测试' + trove_server_name + '失败!')
            return

        # 关闭ssh
        sysbench_client_sshclient.closeSSHAndSFTP()
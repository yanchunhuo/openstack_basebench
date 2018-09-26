#!-*- coding:utf8 -*-
from src.clients.sshClient import SSHClient
from src.common.checkTool import CheckTool
from src.loggers import Loggers
from src.readConfig import ReadConfig

class TestIperf:
    def __init__(self):
        self._loggers=Loggers()
        self._readConfig=ReadConfig()

    def start(self,compute_client,compute_server):
        """
        对两台云主机进行iperf测试
        :param compute_client:
        :param compute_server:
        :return:
        """
        if not compute_client.float_ip or not compute_server.float_ip:
            self._loggers.stabilityIperfLogger.error('云主机'+compute_client.name+'的浮动ip或云主机'+compute_server.name+'的浮动ip为空,无法进行iperf测试')
            return
        compute_client_float_ip=compute_client.float_ip
        compute_server_float_ip=compute_server.float_ip
        #compute_client_ip=compute_client.ip
        compute_server_ip=compute_server.ip
        compute_client_name=compute_client.name
        compute_server_name=compute_server.name
        compute_testType=compute_client.testType

        self._loggers.stabilityIperfLogger.info('开始检测云主机'+compute_client_name+'浮动ip:'+compute_client_float_ip+'是否可连通')
        is_client_online=CheckTool.is_compute_online(compute_client_float_ip)
        self._loggers.stabilityIperfLogger.info('开始检测云主机' + compute_server_name + '浮动ip:' + compute_server_float_ip + '是否可连通')
        is_server_online = CheckTool.is_compute_online(compute_server_float_ip)
        if not (is_client_online and is_server_online):
            self._loggers.stabilityIperfLogger.error('检测到云主机' + compute_server_name +"或"+compute_client_name + '的浮动ip:' + compute_server_float_ip +"或"+compute_client_float_ip+ '无法连通')
            return

        # 检测iperf服务端22端口是否可用
        is_serverport_OK = CheckTool.is_remoteService_OK(compute_server_float_ip, 22)
        if not is_serverport_OK:
            self._loggers.stabilityIperfLogger.error('检测到云主机' + compute_server_name + '浮动ip:' + compute_server_float_ip + '的22端口不可用!')
            return

        # 检测iperf客户端22端口是否可用
        is_clientport_OK = CheckTool.is_remoteService_OK(compute_client_float_ip, 22)
        if not is_clientport_OK:
            self._loggers.stabilityIperfLogger.error('检测到云主机' + compute_client_name + '浮动ip:' + compute_client_float_ip + '的22端口不可用!')
            return

        iperf_client_sshclient=SSHClient(compute_client_float_ip)
        iperf_server_sshclient=SSHClient(compute_server_float_ip)

        #关闭防火墙
        self._loggers.stabilityIperfLogger.info('关闭云主机'+compute_client_name+'和云主机'+compute_server_name+'的防火墙')
        iperf_client_sshclient.ssh_exec_command('service iptables stop',30)
        iperf_server_sshclient.ssh_exec_command('service iptables stop', 30)

        self._loggers.stabilityIperfLogger.info('开始测试iperf,测试类型'+compute_testType)
        #启动服务端
        stdin,stdout,stderr,exit_code=iperf_server_sshclient.ssh_exec_command(command='nohup iperf3 -s -p 8100 -i 1 > nohup.out 2>&1 &',timeout=20)
        if exit_code:
            self._loggers.stabilityIperfLogger.error('在云主机'+compute_server_name+'启动iperf服务端失败!')
            return
        #检测服务端启动是否可用
        is_service_OK=CheckTool.is_remoteService_OK(compute_server_float_ip,8100)
        if not is_service_OK:
            self._loggers.stabilityIperfLogger.error('检测到云主机' + compute_server_name + '浮动ip:' + compute_server_float_ip + '的8100端口不存在!')
            return
        #启动客户端开始测试
        stdin, stdout, stderr, exit_code = iperf_client_sshclient.ssh_exec_command(command='nohup iperf3 -c '+compute_server_ip+' -p 8100 -i 1 -t '+self._readConfig.executeTest.stability_test_iperf_seconds+' -P 10 >nohup.out 2>&1 &',timeout=20)
        if exit_code:
            self._loggers.stabilityIperfLogger.error('测试云主机'+compute_client_name+'和云主机'+compute_server_name+'的iperf失败!')

        # 关闭ssh
        iperf_client_sshclient.closeSSHAndSFTP()
        iperf_server_sshclient.closeSSHAndSFTP()

    def stop(self,compute_client,compute_server):
        """
        停止两台云主机进行iperf测试
        :param compute_client:
        :param compute_server:
        :return:
        """
        if not compute_client.float_ip or not compute_server.float_ip:
            self._loggers.stabilityIperfLogger.error('云主机'+compute_client.name.encode('utf-8')+'的浮动ip或云主机'+compute_server.name.encode('utf-8')+'的浮动ip为空,无法停止iperf测试')
            return
        compute_client_float_ip=compute_client.float_ip.encode('utf-8')
        compute_server_float_ip=compute_server.float_ip.encode('utf-8')
        compute_client_name=compute_client.name.encode('utf-8')
        compute_server_name=compute_server.name.encode('utf-8')

        self._loggers.stabilityIperfLogger.info('开始检测云主机'+compute_client_name+'的ip:'+compute_client_float_ip+'是否可连通')
        is_client_online=CheckTool.is_compute_online(compute_client_float_ip)
        self._loggers.stabilityIperfLogger.info('开始检测云主机' + compute_server_name + '的ip:' + compute_server_float_ip + '是否可连通')
        is_server_online = CheckTool.is_compute_online(compute_server_float_ip)
        if not (is_client_online and is_server_online):
            self._loggers.stabilityIperfLogger.error('检测到云主机' + compute_server_name + "或" + compute_client_name + '浮动ip:' + compute_server_float_ip + "或" + compute_client_float_ip + '无法连通')
            return

        # 检测iperf服务端22端口是否可用
        is_serverport_OK = CheckTool.is_remoteService_OK(compute_server_float_ip, 22)
        if not is_serverport_OK:
            self._loggers.stabilityIperfLogger.error('检测到云主机' + compute_server_name + '浮动ip:' + compute_server_float_ip + '的22端口不可用!')
            return

        # 检测iperf客户端22端口是否可用
        is_clientport_OK = CheckTool.is_remoteService_OK(compute_client_float_ip, 22)
        if not is_clientport_OK:
            self._loggers.stabilityIperfLogger.error('检测到云主机' + compute_client_name + '浮动ip:' + compute_client_float_ip + '的22端口不可用!')
            return

        iperf_client_sshclient=SSHClient(compute_client_float_ip)
        iperf_server_sshclient=SSHClient(compute_server_float_ip)

        # 关闭防火墙
        iperf_client_sshclient.ssh_exec_command('service iptables stop',30)
        iperf_server_sshclient.ssh_exec_command('service iptables stop', 30)

        #关闭客户端程序
        stdin, stdout, stderr, exit_code=iperf_client_sshclient.ssh_exec_command(command="kill -9 `ps -ef |grep iperf3|grep -v grep|awk '{print $2}'`",timeout=10)
        if exit_code:
            self._loggers.stabilityIperfLogger.error('关闭iperf客户端进程失败')

        #关闭服务端程序
        stdin, stdout, stderr, exit_code=iperf_server_sshclient.ssh_exec_command(command="kill -9 `ps -ef |grep iperf3|grep -v grep|awk '{print $2}'`",timeout=10)
        if exit_code:
            self._loggers.stabilityIperfLogger.error('关闭iperf服务端进程失败')
        # 关闭ssh
        iperf_client_sshclient.closeSSHAndSFTP()
        iperf_server_sshclient.closeSSHAndSFTP()


    def reStart(self,compute_client,compute_server):
        """
        对两台云主机进行iperf测试
        :param compute_client:
        :param compute_server:
        :return:
        """
        if not compute_client.float_ip or not compute_server.float_ip:
            self._loggers.stabilityIperfLogger.error('云主机'+compute_client.name.encode('utf-8')+'的浮动ip或云主机'+compute_server.name.encode('utf-8')+'的浮动ip为空,无法重启iperf测试')
            return
        compute_client_float_ip=compute_client.float_ip.encode('utf-8')
        compute_server_float_ip=compute_server.float_ip.encode('utf-8')
        #compute_client_ip=compute_client.ip.encode('utf-8')
        compute_server_ip=compute_server.ip.encode('utf-8')
        compute_client_name=compute_client.name.encode('utf-8')
        compute_server_name=compute_server.name.encode('utf-8')
        compute_testType=compute_client.testType.encode('utf-8')

        self._loggers.stabilityIperfLogger.info('开始检测云主机'+compute_client_name+'的ip:'+compute_client_float_ip+'是否可连通')
        is_client_online=CheckTool.is_compute_online(compute_client_float_ip)
        self._loggers.stabilityIperfLogger.info('开始检测云主机' + compute_server_name + '的ip:' + compute_server_float_ip + '是否可连通')
        is_server_online = CheckTool.is_compute_online(compute_server_float_ip)
        if not (is_client_online and is_server_online):
            self._loggers.stabilityIperfLogger.error('检测到云主机' + compute_server_name + "或" + compute_client_name + '浮动ip:' + compute_server_float_ip + "或" + compute_client_float_ip + '无法连通')
            return

        # 检测iperf服务端22端口是否可用
        is_serverport_OK = CheckTool.is_remoteService_OK(compute_server_float_ip, 22)
        if not is_serverport_OK:
            self._loggers.stabilityIperfLogger.error('检测到云主机' + compute_server_name + '浮动ip:' + compute_server_float_ip + '的22端口不可用!')
            return

        # 检测iperf客户端22端口是否可用
        is_clientport_OK = CheckTool.is_remoteService_OK(compute_client_float_ip, 22)
        if not is_clientport_OK:
            self._loggers.stabilityIperfLogger.error('检测到云主机' + compute_client_name + '浮动ip:' + compute_client_float_ip + '的22端口不可用!')
            return

        iperf_client_sshclient=SSHClient(compute_client_float_ip)
        iperf_server_sshclient=SSHClient(compute_server_float_ip)

        self._loggers.stabilityIperfLogger.info('开始重启测试iperf,测试类型'+compute_testType)
        #启动服务端
        stdin,stdout,stderr,exit_code=iperf_server_sshclient.ssh_exec_command(command='nohup iperf3 -s -p 8100 -i 1 > nohup.out 2>&1 &',timeout=20)
        if exit_code:
            self._loggers.stabilityIperfLogger.error('在云主机'+compute_server_name+'启动iperf服务端失败!')
            return
        #检测服务端启动是否可用
        is_service_OK=CheckTool.is_remoteService_OK(compute_server_float_ip,8100)
        if not is_service_OK:
            self._loggers.stabilityIperfLogger.error('检测到云主机' + compute_server_name + '浮动ip:' + compute_server_float_ip + '的8100端口不存在!')
            return
        #启动客户端开始测试
        stdin, stdout, stderr, exit_code = iperf_client_sshclient.ssh_exec_command(command='nohup iperf3 -c '+compute_server_ip+' -p 8100 -i 1 -t '+self._readConfig.executeTest.stability_test_iperf_seconds+' -P 10 >nohup.out 2>&1 &',timeout=20)
        if exit_code:
            self._loggers.stabilityIperfLogger.error('测试云主机'+compute_client_name+'和云主机'+compute_server_name+'的iperf失败!')

        # 关闭ssh
        iperf_client_sshclient.closeSSHAndSFTP()
        iperf_server_sshclient.closeSSHAndSFTP()
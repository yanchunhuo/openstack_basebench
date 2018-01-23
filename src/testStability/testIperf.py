#!-*- coding:utf8 -*-
from config.config import STABILITY_TEST_IPERF_TIME
from src.clients.sshClient import SSHClient
from src.common import is_compute_online
from src.logger import stabilityIperfLogger
from src.common import is_remoteService_OK

class TestIperf():
    def __init__(self):
        pass

    def start(self,compute_client,compute_server):
        """
        对两台云主机进行iperf测试
        :param compute_client:
        :param compute_server:
        :return:
        """
        if not compute_client.float_ip or not compute_server.float_ip:
            stabilityIperfLogger.error('云主机'+compute_client.name+'的浮动ip或云主机'+compute_server.name+'的浮动ip为空,无法进行iperf测试')
            return
        compute_client_float_ip=compute_client.float_ip
        compute_server_float_ip=compute_server.float_ip
        #compute_client_ip=compute_client.ip
        compute_server_ip=compute_server.ip
        compute_client_name=compute_client.name
        compute_server_name=compute_server.name
        compute_testType=compute_client.testType

        stabilityIperfLogger.info('开始检测云主机'+compute_client_name+'的ip:'+compute_client_float_ip+'是否可连通')
        is_client_online=is_compute_online(compute_client_float_ip)
        stabilityIperfLogger.info('开始检测云主机' + compute_server_name + '的ip:' + compute_server_float_ip + '是否可连通')
        is_server_online = is_compute_online(compute_server_float_ip)
        if not (is_client_online and is_server_online):
            return

        iperf_client_sshclient=SSHClient(compute_client_float_ip)
        iperf_server_sshclient=SSHClient(compute_server_float_ip)

        #关闭防火墙
        stabilityIperfLogger.info('关闭云主机'+compute_client_name+'和云主机'+compute_server_name+'的防火墙')
        iperf_client_sshclient.ssh_exec_command('service iptables stop',30)
        iperf_server_sshclient.ssh_exec_command('service iptables stop', 30)

        stabilityIperfLogger.info('开始测试iperf,测试类型'+compute_testType)
        #启动服务端
        stdin,stdout,stderr,exit_code=iperf_server_sshclient.ssh_exec_command(command='nohup iperf3 -s -p 8100 -i 1 > nohup.out 2>&1 &',timeout=20)
        if exit_code:
            stabilityIperfLogger.error('在云主机'+compute_server_name+'启动iperf服务端失败!')
            return
        #检测服务端启动是否可用
        is_service_OK=is_remoteService_OK(compute_server_float_ip,8100)
        if not is_service_OK:
            return
        #启动客户端开始测试
        stdin, stdout, stderr, exit_code = iperf_client_sshclient.ssh_exec_command(command='nohup iperf3 -c '+compute_server_ip+' -p 8100 -i 1 -t '+str(STABILITY_TEST_IPERF_TIME)+' -P 10 >nohup.out 2>&1 &',timeout=20)
        if exit_code:
            stabilityIperfLogger.error('测试云主机'+compute_client_name+'和云主机'+compute_server_name+'的iperf失败!')

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
            stabilityIperfLogger.error('云主机'+compute_client.name.encode('utf-8')+'的浮动ip或云主机'+compute_server.name.encode('utf-8')+'的浮动ip为空,无法停止iperf测试')
            return
        compute_client_float_ip=compute_client.float_ip.encode('utf-8')
        compute_server_float_ip=compute_server.float_ip.encode('utf-8')
        compute_client_name=compute_client.name.encode('utf-8')
        compute_server_name=compute_server.name.encode('utf-8')

        stabilityIperfLogger.info('开始检测云主机'+compute_client_name+'的ip:'+compute_client_float_ip+'是否可连通')
        is_client_online=is_compute_online(compute_client_float_ip)
        stabilityIperfLogger.info('开始检测云主机' + compute_server_name + '的ip:' + compute_server_float_ip + '是否可连通')
        is_server_online = is_compute_online(compute_server_float_ip)
        if not (is_client_online and is_server_online):
            return

        iperf_client_sshclient=SSHClient(compute_client_float_ip)
        iperf_server_sshclient=SSHClient(compute_server_float_ip)

        #关闭防火墙
        stabilityIperfLogger.info('关闭云主机'+compute_client_name+'和云主机'+compute_server_name+'的防火墙')
        iperf_client_sshclient.ssh_exec_command('service iptables stop',30)
        iperf_server_sshclient.ssh_exec_command('service iptables stop', 30)

        #关闭客户端程序
        stdin, stdout, stderr, exit_code=iperf_client_sshclient.ssh_exec_command(command="kill -9 `ps -A |grep iperf3| awk '{print $1}'`",timeout=10)
        if exit_code:
            stabilityIperfLogger.error('关闭iperf客户端进程失败')

        #关闭服务端程序
        stdin, stdout, stderr, exit_code=iperf_server_sshclient.ssh_exec_command(command="kill -9 `ps -A |grep iperf3| awk '{print $1}'`",timeout=10)
        if exit_code:
            stabilityIperfLogger.error('关闭iperf服务端进程失败')
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
            stabilityIperfLogger.error('云主机'+compute_client.name.encode('utf-8')+'的浮动ip或云主机'+compute_server.name.encode('utf-8')+'的浮动ip为空,无法重启iperf测试')
            return
        compute_client_float_ip=compute_client.float_ip.encode('utf-8')
        compute_server_float_ip=compute_server.float_ip.encode('utf-8')
        #compute_client_ip=compute_client.ip.encode('utf-8')
        compute_server_ip=compute_server.ip.encode('utf-8')
        compute_client_name=compute_client.name.encode('utf-8')
        compute_server_name=compute_server.name.encode('utf-8')
        compute_testType=compute_client.testType.encode('utf-8')

        stabilityIperfLogger.info('开始检测云主机'+compute_client_name+'的ip:'+compute_client_float_ip+'是否可连通')
        is_client_online=is_compute_online(compute_client_float_ip)
        stabilityIperfLogger.info('开始检测云主机' + compute_server_name + '的ip:' + compute_server_float_ip + '是否可连通')
        is_server_online = is_compute_online(compute_server_float_ip)
        if not (is_client_online and is_server_online):
            return

        iperf_client_sshclient=SSHClient(compute_client_float_ip)
        iperf_server_sshclient=SSHClient(compute_server_float_ip)

        stabilityIperfLogger.info('开始重启测试iperf,测试类型'+compute_testType)
        #启动服务端
        stdin,stdout,stderr,exit_code=iperf_server_sshclient.ssh_exec_command(command='nohup iperf3 -s -p 8100 -i 1 > nohup.out 2>&1 &',timeout=20)
        if exit_code:
            stabilityIperfLogger.error('在云主机'+compute_server_name+'启动iperf服务端失败!')
            return
        #检测服务端启动是否可用
        is_service_OK=is_remoteService_OK(compute_server_float_ip,8100)
        if not is_service_OK:
            return
        #启动客户端开始测试
        stdin, stdout, stderr, exit_code = iperf_client_sshclient.ssh_exec_command(command='nohup iperf3 -c '+compute_server_ip+' -p 8100 -i 1 -t '+str(STABILITY_TEST_IPERF_TIME)+' -P 10 >nohup.out 2>&1 &',timeout=20)
        if exit_code:
            stabilityIperfLogger.error('测试云主机'+compute_client_name+'和云主机'+compute_server_name+'的iperf失败!')

        # 关闭ssh
        iperf_client_sshclient.closeSSHAndSFTP()
        iperf_server_sshclient.closeSSHAndSFTP()
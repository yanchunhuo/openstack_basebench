#!-*- coding:utf8 -*-
from src.clients.sshClient import SSHClient
from src.common import is_compute_online
from src.logger import stabilitySysbenchLogger
import time



class TestSysbench():
    def __init__(self):
        pass

    def start(self,compute_client,trove_server):
        """
        对两台云主机进行sysbench测试
        :param compute_client:
        :param trove_server:
        :return:
        """

        if not compute_client.float_ip:
            stabilitySysbenchLogger.error('云主机' + compute_client.name + '的浮动ip为空,无法进行sysbench测试')
            return

        compute_client_float_ip=compute_client.float_ip
        #compute_server_float_ip=trove_server.float_ip
        #compute_client_ip=compute_client.ip
        trove_server_ip=trove_server.ip
        compute_client_name=compute_client.name
        trove_server_name=trove_server.name
        compute_testType=compute_client.testType
        stabilitySysbenchLogger.info('等待300秒')
        time.sleep(300)

        stabilitySysbenchLogger.info('开始检测云主机'+compute_client_name+'的ip:'+compute_client_float_ip+'是否可连通')
        is_client_online=is_compute_online(compute_client_float_ip)

        if not is_client_online :
            return

        sysbench_client_sshclient=SSHClient(compute_client_float_ip)

        #关闭防火墙
        stabilitySysbenchLogger.info('关闭云主机'+compute_client_name+'的防火墙')
        sysbench_client_sshclient.ssh_exec_command('service iptables stop',30)

        stabilitySysbenchLogger.info('开始测试sysbench,测试类型'+compute_testType)
        #启动客户端开始测试
        stdin,stdout,stderr,exit_code=sysbench_client_sshclient.ssh_exec_command(command='nohup sysbench /usr/local/share/sysbench/oltp_read_write.lua --db-driver=mysql --threads=100 --tables=20 --table_size=100000000  --mysql-user=test --mysql-password=123456..  --mysql-host='+trove_server_ip+' --mysql-port=3306 --mysql-db=sbtest prepare >nohup.out 2>&1 &',timeout=20)
        if exit_code:
            stabilitySysbenchLogger.error('使用sysbench测试'+trove_server_name+'失败!')
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
            stabilitySysbenchLogger.error('云主机' + compute_client.name + '的浮动ip为空,无法停止sysbench测试')
            return

        compute_client_float_ip=compute_client.float_ip.encode('utf-8')
        compute_client_name=compute_client.name.encode('utf-8')
        #trove_server_name=trove_server.name.encode('utf-8')

        stabilitySysbenchLogger.info('开始检测数据库实例'+compute_client_name+'的ip:'+compute_client_float_ip+'是否可连通')
        is_client_online=is_compute_online(compute_client_float_ip)

        if not is_client_online :
            return

        sysbench_client_sshclient=SSHClient(compute_client_float_ip)

        #关闭防火墙
        stabilitySysbenchLogger.info('关闭云主机'+compute_client_name+'的防火墙')
        sysbench_client_sshclient.ssh_exec_command('service iptables stop',30)


        #关闭客户端程序
        stabilitySysbenchLogger.info('停止sysbench测试')
        stdin, stdout, stderr, exit_code=sysbench_client_sshclient.ssh_exec_command(command="kill -9 `ps -A |grep sysbench| awk '{print $1}'`",timeout=10)
        if exit_code:
            stabilitySysbenchLogger.error('关闭sysbench客户端进程失败')

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
            stabilitySysbenchLogger.error('云主机' + compute_client.name + '的浮动ip为空,无法进行重启sysbench测试')
            return

        compute_client_float_ip = compute_client.float_ip.encode('utf-8')
        # compute_server_float_ip=trove_server.float_ip
        # compute_client_ip=compute_client.ip
        trove_server_ip = trove_server.ip.encode('utf-8')
        compute_client_name = compute_client.name.encode('utf-8')
        trove_server_name = trove_server.name.encode('utf-8')
        compute_testType = compute_client.testType.encode('utf-8')



        stabilitySysbenchLogger.info('开始检测云主机' + compute_client_name + '的ip:' + compute_client_float_ip + '是否可连通')
        is_client_online = is_compute_online(compute_client_float_ip)

        if not is_client_online:
            return

        sysbench_client_sshclient = SSHClient(compute_client_float_ip)

        # 关闭防火墙
        stabilitySysbenchLogger.info('关闭云主机' + compute_client_name + '的防火墙')
        sysbench_client_sshclient.ssh_exec_command('service iptables stop', 30)



        stabilitySysbenchLogger.info('清空数据库实例' + trove_server_name + '中的数据库sbtest的数据')
        stdin, stdout, stderr, exit_code = sysbench_client_sshclient.ssh_exec_command(command='mysql -h'+ trove_server_ip + ' -utest -p123456.. -e "drop database sbtest;CREATE DATABASE  sbtest CHARACTER SET utf8 COLLATE utf8_general_ci"', timeout=100)
        if exit_code:
            stabilitySysbenchLogger.error('删除数据库实例' + trove_server_name + '的数据库sbtest失败!')
            return


        stabilitySysbenchLogger.info('重新开始测试sysbench,测试类型' + compute_testType)
        # 启动客户端开始测试
        stdin, stdout, stderr, exit_code = sysbench_client_sshclient.ssh_exec_command(command='nohup sysbench /usr/local/share/sysbench/oltp_read_write.lua --db-driver=mysql --threads=100 --tables=20 --table_size=100000000  --mysql-user=test --mysql-password=123456..  --mysql-host=' + trove_server_ip + ' --mysql-port=3306 --mysql-db=sbtest prepare >nohup.out 2>&1 &',timeout=20)
        if exit_code:
            stabilitySysbenchLogger.error('使用sysbench测试' + trove_server_name + '失败!')
            return

        # 关闭ssh
        sysbench_client_sshclient.closeSSHAndSFTP()
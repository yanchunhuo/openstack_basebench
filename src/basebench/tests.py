#!-*- coding:utf8 -*-
from src.clients.sshClient import SSHClient
from src.common.checkTool import CheckTool
from src.loggers import Loggers
from src.readConfig import ReadConfig

class Tests:
    def __init__(self):
        self._loggers = Loggers()
        self._readConfig = ReadConfig()

    def testFio(self,compute_obj):
        """
        对云主机进行测试
        :param compute_obj:
        :return:
        """
        if not compute_obj.float_ip:
            self._loggers.basebenchLogger.error('云主机'+compute_obj.name+'的浮动ip为空,无法进行FIO测试')
            return
        compute_float_ip=compute_obj.float_ip
        compute_name=compute_obj.name
        compute_testType=compute_obj.testType

        self._loggers.basebenchLogger.info('开始检测云主机'+compute_name+'浮动ip:'+compute_float_ip+'是否可连通')
        is_online=CheckTool.is_compute_online(compute_float_ip)
        if not is_online:
            self._loggers.basebenchLogger.error('检测到云主机' + compute_name + '浮动ip:' + compute_float_ip + '无法连通')
            return

        # 检测云主机22端口是否可用
        is_fioport_OK = CheckTool.is_remoteService_OK(compute_float_ip, 22)
        if not is_fioport_OK:
            self._loggers.basebenchLogger.error('检测到云主机' + compute_name + '浮动ip:' + compute_float_ip + '的22端口不可用!')
            return

        #获得ssh连接对象
        self._loggers.basebenchLogger.info('开始获得云主机'+compute_float_ip+'的ssh连接')
        sshclient=SSHClient(compute_float_ip)

        self._loggers.basebenchLogger.info('格式化云主机' + compute_name + '的云硬盘/dev/vdc')
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command('mkfs -t ext4 /dev/vdc', timeout=1200)
        if exit_code:
            self._loggers.basebenchLogger.error('格式化云主机' + compute_name + '的云硬盘/dev/vdc失败!' + '\r\n' + stderr.read())
            return

        # 创建磁盘挂载目录
        self._loggers.basebenchLogger.info('创建云主机云' + compute_name + '硬盘挂载目录/root/test')
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command='mkdir -p /root/test')
        if exit_code:
            self._loggers.basebenchLogger.error('创建云主机云' + compute_name + '硬盘挂载目录/root/test失败!' + '\r\n' + stderr.read())
            return

        # 挂载云硬盘
        self._loggers.basebenchLogger.info('为云主机' + compute_name + '挂载云硬盘/dev/vdc')
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command='mount /dev/vdc /root/test', timeout=20)
        if exit_code:
            self._loggers.basebenchLogger.error('为云主机' + compute_name + '挂载云硬盘/dev/vdc失败!+\r\n' + stderr.read())
            return

        # 创建测试结果保存目录
        self._loggers.basebenchLogger.info('在云主机' + compute_name + '里创建结果保存目录/root/result')
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command='mkdir -p /root/result')
        if exit_code:
            self._loggers.basebenchLogger.error('在云主机' + compute_name + '里创建结果保存目录/root/result失败!' + '\r\n' + stderr.read())
            return

        test_fio_volume_types=self._readConfig.executeTest.basebench_test_fio_volume_types.split('||')
        test_fio_types=self._readConfig.executeTest.basebench_test_fio_types.split('||')
        for test_fio_volume_type in test_fio_volume_types:
            for test_fio_type in test_fio_types:
                testType = test_fio_type + test_fio_volume_type
                if testType == compute_testType:
                    self._loggers.basebenchLogger.info('开始fio测试,云主机' + compute_name + ',测试类型' + testType)
                    test_command = 'cd /root/test/;fio -filename=test' + testType + '  -direct=1 -iodepth 128 -thread -rw=' + test_fio_type + ' -ioengine=libaio -bs=4k -size=' + self._readConfig.executeTest.basebench_test_fio_volume_size + 'G -numjobs=10 -runtime=60 -name=' + testType + '-libaio -group_reporting --output /root/result/fio_' + testType + '_output.html'
                    stdin, stdout, stderr, exit_code=sshclient.ssh_exec_command(command=test_command, timeout=3600)
                    if exit_code:
                        self._loggers.basebenchLogger.error('fio测试云主机' + compute_name + '测试' + testType + '失败!' + '\r\n' + stderr.read())
                    # 获取结果文件
                    sshclient.sftp_get('/root/result/fio_' + testType + '_output.html',
                                       'output/fio/fio_' + testType + '_output.html')
                    #删除测试文件
                    del_command='cd /root/test/;rm -rf test' + testType
                    stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command=del_command, timeout=3600)
                    if exit_code:
                        self._loggers.basebenchLogger.error('fio测试后删除云主机'+compute_name+'的文件test'+testType+'失败!'+'\r\n'+stderr.read())
        #关闭ssh
        sshclient.closeSSHAndSFTP()

    def testUinxbench(self,compute_obj):
        """
        对云主机进行测试
        :param compute_obj:
        :return:
        """
        if not compute_obj.float_ip:
            self._loggers.basebenchLogger.error('云主机'+compute_obj.name+'的浮动ip为空,无法进行Unixbench测试')
            return
        compute_float_ip = compute_obj.float_ip
        compute_name = compute_obj.name
        compute_testType = compute_obj.testType

        self._loggers.basebenchLogger.info('开始检测云主机'+compute_name+'浮动ip:'+compute_float_ip+'是否可连通')
        is_online=CheckTool.is_compute_online(compute_float_ip)
        if not is_online:
            self._loggers.basebenchLogger.error('检测到云主机' + compute_name + '浮动ip:' + compute_float_ip + '无法连通')
            return

        # 检测云主机22端口是否可用
        is_unixbenchport_OK = CheckTool.is_remoteService_OK(compute_float_ip, 22)
        if not is_unixbenchport_OK:
            self._loggers.basebenchLogger.error('检测到云主机' + compute_name + '浮动ip:' + compute_float_ip + '的22端口不可用!')
            return

        #获得ssh连接对象
        sshclient = SSHClient(compute_float_ip)

        self._loggers.basebenchLogger.info('开始进行unixbench测试,云主机' + compute_name + ',测试类型' + compute_testType)
        test_command = 'cd /root/soft/unixbench;./Run'
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command=test_command, timeout=3600)
        if exit_code:
            self._loggers.basebenchLogger.error('unixbench测试云主机' + compute_name + '测试失败!' + '\r\n' + stderr.read())
        # 获取结果文件
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command='cd /root/soft/unixbench;tar -zcvf ' + compute_testType + '_result.tar.gz results/', timeout=3600)
        if exit_code:
            self._loggers.basebenchLogger.error('unixbench测试云主机' + compute_name + '压缩结果文件失败!' + '\r\n' + stderr.read())
        sshclient.sftp_get('/root/soft/unixbench/' + compute_testType + '_result.tar.gz','output/unixbench/'+ compute_testType + '_result.tar.gz')

        # 关闭ssh
        sshclient.closeSSHAndSFTP()


    def testIperf(self,compute_client,compute_server):
        """
        对两台云主机进行iperf测试
        :param compute_client:
        :param compute_server:
        :return:
        """
        if not compute_client.float_ip or not compute_server.float_ip:
            self._loggers.basebenchLogger.error('云主机'+compute_client.name+'的浮动ip或云主机'+compute_server.name+'的浮动ip为空,无法进行iperf测试')
            return
        compute_client_float_ip=compute_client.float_ip
        compute_server_float_ip=compute_server.float_ip
        #compute_client_ip=compute_client.ip
        compute_server_ip=compute_server.ip
        compute_client_name=compute_client.name
        compute_server_name=compute_server.name
        compute_testType=compute_client.testType

        self._loggers.basebenchLogger.info('开始检测云主机'+compute_client_name+'的ip:'+compute_client_float_ip+'是否可连通')
        is_client_online=CheckTool.is_compute_online(compute_client_float_ip)
        self._loggers.basebenchLogger.info('开始检测云主机' + compute_server_name + '的ip:' + compute_server_float_ip + '是否可连通')
        is_server_online = CheckTool.is_compute_online(compute_server_float_ip)
        if not (is_client_online and is_server_online):
            self._loggers.basebenchLogger.error('检测到云主机'+ compute_server_name + "或" + compute_client_name + '浮动ip:' + compute_server_float_ip + "或" + compute_client_float_ip + '无法连通')
            return
        # 检测iperf服务端22端口是否可用
        is_iperfserviceport_OK = CheckTool.is_remoteService_OK(compute_server_float_ip, 22)
        if not is_iperfserviceport_OK:
            self._loggers.basebenchLogger.error('检测到云主机' + compute_server_name  + '浮动ip:' + compute_server_float_ip + '的22端口不可用!')
            return
        # 检测iperf客户端22端口是否可用
        is_iperfclientport_OK = CheckTool.is_remoteService_OK(compute_client_float_ip, 22)
        if not is_iperfclientport_OK:
            self._loggers.basebenchLogger.error('检测到云主机' + compute_client_name  + '浮动ip:' + compute_client_float_ip+ '的22端口不可用!')
            return
        iperf_client_sshclient=SSHClient(compute_client_float_ip)
        iperf_server_sshclient=SSHClient(compute_server_float_ip)

        #关闭防火墙
        self._loggers.basebenchLogger.info('关闭云主机'+compute_client_name+'和云主机'+compute_server_name+'的防火墙')
        iperf_client_sshclient.ssh_exec_command('service iptables stop',30)
        iperf_server_sshclient.ssh_exec_command('service iptables stop', 30)

        # 创建测试结果保存目录
        self._loggers.basebenchLogger.info('在iperf客户端云主机' + compute_client_name + '里创建结果保存目录/root/result')
        stdin, stdout, stderr, exit_code = iperf_client_sshclient.ssh_exec_command(command='mkdir -p /root/result')
        if exit_code:
            self._loggers.basebenchLogger.error('在云主机' + compute_client_name + '里创建结果保存目录/root/result失败!' + '\r\n' + stderr.read())
            return

        self._loggers.basebenchLogger.info('开始测试iperf,测试类型'+compute_testType)
        #启动服务端
        stdin,stdout,stderr,exit_code=iperf_server_sshclient.ssh_exec_command(command='nohup iperf3 -s -p 8100 -i 1 > nohup.out 2>&1 &',timeout=10)
        if exit_code:
            self._loggers.basebenchLogger.error('在云主机'+compute_server_name+'启动iperf服务端失败!')
            return
        #检测服务端启动是否可用
        is_service_OK=CheckTool.is_remoteService_OK(compute_server_float_ip,8100)
        if not is_service_OK:
            self._loggers.basebenchLogger.error('检测到云主机' + compute_server_name + '浮动ip:' + compute_server_float_ip + '的8100端口不存在!')
            return
        #启动客户端开始测试
        stdin, stdout, stderr, exit_code = iperf_client_sshclient.ssh_exec_command(command='iperf3 -c '+compute_server_ip+' -p 8100 -i 1 -t 60 -P 10 >/root/result/'+compute_testType+'_result.txt',timeout=180)
        if exit_code:
            self._loggers.basebenchLogger.error('测试云主机'+compute_client_name+'和云主机'+compute_server_name+'的iperf失败!')
        #下载测试结果
        iperf_client_sshclient.sftp_get('/root/result/'+compute_testType+'_result.txt','output/iperf/'+compute_testType+'_result.txt')
        #关闭服务端程序
        stdin, stdout, stderr, exit_code=iperf_server_sshclient.ssh_exec_command(command="kill -9 `ps -A |grep iperf3| awk '{print $1}'`",timeout=10)
        if exit_code:
            self._loggers.basebenchLogger.error('关闭iperf服务端进程失败')
        # 关闭ssh
        iperf_client_sshclient.closeSSHAndSFTP()
        iperf_server_sshclient.closeSSHAndSFTP()

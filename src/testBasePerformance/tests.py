#!-*- coding:utf8 -*-
from config.config import IS_TEST_FIO
from config.config import IS_TEST_UNIXBENCH
from config.config import TEST_FIO_VOLUME_TYPE
from config.config import TEST_UNIXBENCH_FLAVOR
from config.config import TEST_FIO_SIZE
from config.config import WHAT_FIO_TEST
from src.clients.sshClient import SSHClient
from src.common import is_compute_online
from src.common import is_remoteService_OK
from src.logger import basePerformanceLogger

class Tests():
    def __init__(self):
        self._fio_compute_testTypes=[]
        self._unixbench_compute_testTypes=[]
        self._init()

    def _init(self):
        if IS_TEST_FIO:
            for test_fio_volume_type in TEST_FIO_VOLUME_TYPE:
                for test_fio_type in WHAT_FIO_TEST:
                    self._fio_compute_testTypes.append(test_fio_type+test_fio_volume_type)
            basePerformanceLogger.info('确定需要测试的fio类型,包括:'+self._fio_compute_testTypes.__str__())

        if IS_TEST_UNIXBENCH:
            for test_unixbench_flavor_type in TEST_UNIXBENCH_FLAVOR:
                self._unixbench_compute_testTypes.append('unixbench_'+test_unixbench_flavor_type)
            basePerformanceLogger.info('确定需要测试的unixbench云主机类型,包括:'+self._unixbench_compute_testTypes.__str__())

    def testFio(self,compute_obj):
        """
        对云主机进行测试
        :param compute_obj:
        :return:
        """
        if not compute_obj.float_ip:
            basePerformanceLogger.error('云主机'+compute_obj.name+'的浮动ip为空,无法进行FIO测试')
            return
        compute_float_ip=compute_obj.float_ip
        compute_name=compute_obj.name
        compute_testType=compute_obj.testType

        basePerformanceLogger.info('开始检测云主机'+compute_name+'的ip:'+compute_float_ip+'是否可连通')
        is_online=is_compute_online(compute_float_ip)
        if not is_online:
            return

        #获得ssh连接对象
        basePerformanceLogger.info('开始获得云主机'+compute_float_ip+'的ssh连接')
        sshclient=SSHClient(compute_float_ip)

        basePerformanceLogger.info('格式化云主机' + compute_name + '的云硬盘/dev/vdb')
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command('mkfs -t ext4 /dev/vdb', timeout=1200)
        if exit_code:
            basePerformanceLogger.error('格式化云主机' + compute_name + '的云硬盘/dev/vdb失败!' + '\r\n' + stderr.read())
            return

        # 创建磁盘挂载目录
        basePerformanceLogger.info('创建云主机云' + compute_name + '硬盘挂载目录/root/test')
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command='mkdir -p /root/test')
        if exit_code:
            basePerformanceLogger.error('创建云主机云' + compute_name + '硬盘挂载目录/root/test失败!' + '\r\n' + stderr.read())
            return

        # 挂载云硬盘
        basePerformanceLogger.info('为云主机' + compute_name + '挂载云硬盘/dev/vdb')
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command='mount /dev/vdb /root/test', timeout=20)
        if exit_code:
            basePerformanceLogger.error('为云主机' + compute_name + '挂载云硬盘/dev/vdb失败!+\r\n' + stderr.read())
            return

        # 创建测试结果保存目录
        basePerformanceLogger.info('在云主机' + compute_name + '里创建结果保存目录/root/result')
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command='mkdir -p /root/result')
        if exit_code:
            basePerformanceLogger.error('在云主机' + compute_name + '里创建结果保存目录/root/result失败!' + '\r\n' + stderr.read())
            return

        for test_fio_volume_type in TEST_FIO_VOLUME_TYPE:
            for test_fio_type in WHAT_FIO_TEST:
                testType = test_fio_type + test_fio_volume_type
                if testType == compute_testType:
                    basePerformanceLogger.info('开始fio测试,云主机' + compute_name + ',测试类型' + testType)
                    test_command = 'cd /root/test/;fio -filename=test' + testType + '  -direct=1 -iodepth 128 -thread -rw=' + test_fio_type + ' -ioengine=libaio -bs=4k -size=' + str(TEST_FIO_SIZE) + 'G -numjobs=10 -runtime=60 -name=' + testType + '-libaio -group_reporting --output /root/result/fio_' + testType + '_output.html'
                    stdin, stdout, stderr, exit_code=sshclient.ssh_exec_command(command=test_command, timeout=3600)
                    if exit_code:
                        basePerformanceLogger.error('fio测试云主机' + compute_name + '测试' + testType + '失败!' + '\r\n' + stderr.read())
                    # 获取结果文件
                    sshclient.sftp_get('/root/result/fio_' + testType + '_output.html',
                                       'output/fio/fio_' + testType + '_output.html')
                    #删除测试文件
                    del_command='cd /root/test/;rm -rf test' + testType
                    stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command=del_command, timeout=3600)
                    if exit_code:
                        basePerformanceLogger.error('fio测试后删除云主机'+compute_name+'的文件test'+testType+'失败!'+'\r\n'+stderr.read())
        #关闭ssh
        sshclient.closeSSHAndSFTP()



    def testUinxbench(self,compute_obj):
        """
        对云主机进行测试
        :param compute_obj:
        :return:
        """
        if not compute_obj.float_ip:
            basePerformanceLogger.error('云主机'+compute_obj.name+'的浮动ip为空,无法进行Unixbench测试')
            return
        compute_float_ip = compute_obj.float_ip
        compute_name = compute_obj.name
        compute_testType = compute_obj.testType

        basePerformanceLogger.info('开始检测云主机'+compute_name+'的ip:'+compute_float_ip+'是否可连通')
        is_online=is_compute_online(compute_float_ip)
        if not is_online:
            return

        #获得ssh连接对象
        sshclient = SSHClient(compute_float_ip)

        basePerformanceLogger.info('开始进行unixbench测试,云主机' + compute_name + ',测试类型' + compute_testType)
        test_command = 'cd /root/soft/unixbench;./Run'
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command=test_command, timeout=3600)
        if exit_code:
            basePerformanceLogger.error('unixbench测试云主机' + compute_name + '测试失败!' + '\r\n' + stderr.read())
        # 获取结果文件
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command='cd /root/soft/unixbench;tar -zcvf ' + compute_testType + '_result.tar.gz results/', timeout=3600)
        if exit_code:
            basePerformanceLogger.error('unixbench测试云主机' + compute_name + '压缩结果文件失败!' + '\r\n' + stderr.read())
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
            basePerformanceLogger.error('云主机'+compute_client.name+'的浮动ip或云主机'+compute_server.name+'的浮动ip为空,无法进行iperf测试')
            return
        compute_client_float_ip=compute_client.float_ip
        compute_server_float_ip=compute_server.float_ip
        #compute_client_ip=compute_client.ip
        compute_server_ip=compute_server.ip
        compute_client_name=compute_client.name
        compute_server_name=compute_server.name
        compute_testType=compute_client.testType

        basePerformanceLogger.info('开始检测云主机'+compute_client_name+'的ip:'+compute_client_float_ip+'是否可连通')
        is_client_online=is_compute_online(compute_client_float_ip)
        basePerformanceLogger.info('开始检测云主机' + compute_server_name + '的ip:' + compute_server_float_ip + '是否可连通')
        is_server_online = is_compute_online(compute_server_float_ip)
        if not (is_client_online and is_server_online):
            return

        iperf_client_sshclient=SSHClient(compute_client_float_ip)
        iperf_server_sshclient=SSHClient(compute_server_float_ip)

        #关闭防火墙
        basePerformanceLogger.info('关闭云主机'+compute_client_name+'和云主机'+compute_server_name+'的防火墙')
        iperf_client_sshclient.ssh_exec_command('service iptables stop',30)
        iperf_server_sshclient.ssh_exec_command('service iptables stop', 30)

        # 创建测试结果保存目录
        basePerformanceLogger.info('在iperf客户端云主机' + compute_client_name + '里创建结果保存目录/root/result')
        stdin, stdout, stderr, exit_code = iperf_client_sshclient.ssh_exec_command(command='mkdir -p /root/result')
        if exit_code:
            basePerformanceLogger.error('在云主机' + compute_client_name + '里创建结果保存目录/root/result失败!' + '\r\n' + stderr.read())
            return

        basePerformanceLogger.info('开始测试iperf,测试类型'+compute_testType)
        #启动服务端
        stdin,stdout,stderr,exit_code=iperf_server_sshclient.ssh_exec_command(command='nohup iperf3 -s -p 8100 -i 1 > nohup.out 2>&1 &',timeout=10)
        if exit_code:
            basePerformanceLogger.error('在云主机'+compute_server_name+'启动iperf服务端失败!')
            return
        #检测服务端启动是否可用
        is_service_OK=is_remoteService_OK(compute_server_float_ip,8100)
        if not is_service_OK:
            return
        #启动客户端开始测试
        stdin, stdout, stderr, exit_code = iperf_client_sshclient.ssh_exec_command(command='iperf3 -c '+compute_server_ip+' -p 8100 -i 1 -t 60 -P 10 >/root/result/'+compute_testType+'_result.txt',timeout=180)
        if exit_code:
            basePerformanceLogger.error('测试云主机'+compute_client_name+'和云主机'+compute_server_name+'的iperf失败!')
        #下载测试结果
        iperf_client_sshclient.sftp_get('/root/result/'+compute_testType+'_result.txt','output/iperf/'+compute_testType+'_result.txt')
        #关闭服务端程序
        stdin, stdout, stderr, exit_code=iperf_server_sshclient.ssh_exec_command(command="kill -9 `ps -A |grep iperf3| awk '{print $1}'`",timeout=10)
        if exit_code:
            basePerformanceLogger.error('关闭iperf服务端进程失败')
        # 关闭ssh
        iperf_client_sshclient.closeSSHAndSFTP()
        iperf_server_sshclient.closeSSHAndSFTP()

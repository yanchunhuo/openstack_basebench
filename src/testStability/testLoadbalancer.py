#!-*- coding:utf8 -*-
from src.clients.sshClient import SSHClient
from src.common import is_compute_online
from src.logger import stabilityLoadbalancerLogger

class TestLoadbalancer():
    def __init__(self):
        pass

    def start(self,loadbalancer_obj):
        """
        对loadbalancer进行请求测试
        :param loadbalancer_compute_obj:
        :return:
        """
        jmeter_compute_obj=loadbalancer_obj.load_compute
        if not (jmeter_compute_obj.float_ip and loadbalancer_obj.virtual_ip):
            stabilityLoadbalancerLogger.error('加压云主机'+jmeter_compute_obj.name+'或负载均衡器'+loadbalancer_obj.name+'的浮动ip为空,无法进行loadbalancer测试')
            return
        jmeter_compute_float_ip=jmeter_compute_obj.float_ip
        loadbalancer_float_ip=loadbalancer_obj.virtual_ip
        jmeter_compute_name=jmeter_compute_obj.name
        loadbalancer_name=loadbalancer_obj.name
        loadbalancer_port=loadbalancer_obj.port
        loadbalancer_members=loadbalancer_obj.get_members()
        for loadbalancer_member in loadbalancer_members:
            if not loadbalancer_member.float_ip:
                stabilityLoadbalancerLogger.error('后端服务器' + loadbalancer_member.name+ '的浮动ip为空,无法进行loadbalancer测试')
                return
            loadbalancer_member_float_ip=loadbalancer_member.float_ip
            loadbalancer_member_name=loadbalancer_member.name
            stabilityLoadbalancerLogger.info('开始检测后端服务器' + loadbalancer_member_name + '的ip:' + loadbalancer_member_float_ip + '是否可连通')
            try:
                is_member_online = is_compute_online(loadbalancer_member_float_ip)
            except Exception,e:
                stabilityLoadbalancerLogger.info('检测后端服务器' + loadbalancer_member_name + '的ip:' + loadbalancer_member_float_ip + '无法连通'+ '\r\n' + e.message)
                return
            loadbalancer_member_sshclient = SSHClient(loadbalancer_member_float_ip)
            # 关闭防火墙
            stabilityLoadbalancerLogger.info('关闭云主机' + loadbalancer_member_name + '的防火墙')
            loadbalancer_member_sshclient.ssh_exec_command('service iptables stop', 30)

            stabilityLoadbalancerLogger.info('启动后端服务器的nginx')
            # 启动服务
            stdin, stdout, stderr, exit_code = loadbalancer_member_sshclient.ssh_exec_command(command='cd /usr/local/nginx/sbin;nohup ./nginx > nohup.out 2>&1 &')
            if exit_code:
                stabilityLoadbalancerLogger.error('在云主机' + loadbalancer_member_name + '启动后端服务器的nginx失败!')
                return
            loadbalancer_member_sshclient.closeSSHAndSFTP()
        stabilityLoadbalancerLogger.info('开始检测负载均衡器' + loadbalancer_name + '的ip:' + loadbalancer_float_ip + '是否可连通')
        try:
            is_loadbalancer_online = is_compute_online(loadbalancer_float_ip)
        except Exception,e:
            stabilityLoadbalancerLogger.error('检测负载均衡器' + loadbalancer_name + '的ip:' + loadbalancer_float_ip + '无法连通'+ '\r\n' + e.message)
            return
        stabilityLoadbalancerLogger.info('开始检测对均衡负载器加压云主机' + jmeter_compute_name + '的ip:' + jmeter_compute_float_ip + '是否可连通')
        try:
            is_jmeter_online = is_compute_online(jmeter_compute_float_ip)
        except Exception,e:
            stabilityLoadbalancerLogger.error('开始检测对均衡负载器加压云主机' + jmeter_compute_name + '的ip:' + jmeter_compute_float_ip + '无法连通'+ '\r\n' + e.message)
            return
        jmeter_sshclient=SSHClient(jmeter_compute_float_ip)
        stabilityLoadbalancerLogger.info('开始对负载均衡器' + loadbalancer_name + '进行请求')
        test_command = 'cd /root/soft/jmeter/projects/LB;nohup sed -i "s/ip,port/' + loadbalancer_float_ip + ',' + loadbalancer_port + '/g" lb_test.txt' + ' >nohup.out 2>&1 &'
        stdin, stdout, stderr, exit_code = jmeter_sshclient.ssh_exec_command(command=test_command, timeout=20)
        if exit_code:
            stabilityLoadbalancerLogger.error('对均衡负载器加压云主机' + jmeter_compute_name + '修改配置文件失败' + '\r\n' + stderr.read())
        test_command = 'source /etc/profile;cd /root/soft/jmeter/bin;nohup ./jmeter -n -t /root/soft/jmeter/projects/LB/lb_forever.jmx -l logfile.jtl >nohup.out 2>&1 &'
        stdin, stdout, stderr, exit_code = jmeter_sshclient.ssh_exec_command(command=test_command, timeout=20)
        if exit_code:
            stabilityLoadbalancerLogger.error('对均衡负载器加压云主机' + jmeter_compute_name + '启动失败' + '\r\n' + stderr.read())

        # 关闭ssh
        jmeter_sshclient.closeSSHAndSFTP()

    def stop(self,jmeter_compute_obj):
        """
        停止均衡负载器loadbalancer加压
        :param compute_obj:
        :return:
        """
        if not jmeter_compute_obj.float_ip:
            stabilityLoadbalancerLogger.error('加压云主机'+jmeter_compute_obj.name+'的浮动ip为空,无法停止loadbalancer测试')
            return
        jmeter_compute_float_ip = jmeter_compute_obj.float_ip.encode('utf-8')
        jmeter_compute_name = jmeter_compute_obj.name.encode('utf-8')

        stabilityLoadbalancerLogger.info('开始检测对均衡负载器加压云主机' + jmeter_compute_name + '的ip:' + jmeter_compute_float_ip + '是否可连通')
        try:
            is_jmeter_online = is_compute_online(jmeter_compute_float_ip)
        except Exception,e:
            stabilityLoadbalancerLogger.error('检测对均衡负载器加压云主机' + jmeter_compute_name + '的ip:' + jmeter_compute_float_ip + '无法连通'+ '\r\n' + e.message)
            return

        # 获得ssh连接对象
        sshclient = SSHClient(jmeter_compute_float_ip)

        stabilityLoadbalancerLogger.info('开始停止loadbalance加压测试,云主机' + jmeter_compute_name)
        stop_jmeter_command = "killall -9 java"
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command=stop_jmeter_command, timeout=20)
        if exit_code:
            stabilityLoadbalancerLogger.error('停止对均衡负载器加压云主机' + jmeter_compute_name + 'loadbalancer测试失败' + '\r\n' + stderr.read())

        # 关闭ssh
        sshclient.closeSSHAndSFTP()


    def reStart(self,jmeter_compute_obj):
        """
        停止均衡负载器loadbalancer加压
        :param compute_obj:
        :return:
        """
        if not jmeter_compute_obj.float_ip:
            stabilityLoadbalancerLogger.error('加压云主机'+jmeter_compute_obj.name+'的浮动ip为空,无法重启loadbalancer测试')
            return
        jmeter_compute_float_ip = jmeter_compute_obj.float_ip.encode('utf-8')
        jmeter_compute_name = jmeter_compute_obj.name.encode('utf-8')

        stabilityLoadbalancerLogger.info('开始检测对均衡负载器加压云主机' + jmeter_compute_name + '的ip:' + jmeter_compute_float_ip + '是否可连通')
        try:
            is_jmeter_online = is_compute_online(jmeter_compute_float_ip)
        except Exception, e:
            stabilityLoadbalancerLogger.error('检测对均衡负载器加压云主机' + jmeter_compute_name + '的ip:' + jmeter_compute_float_ip + '无法连通'+ '\r\n' + e.message)
            return

        # 获得ssh连接对象
        jmeter_sshclient = SSHClient(jmeter_compute_float_ip)
        stabilityLoadbalancerLogger.info('重启加压云主机'+jmeter_compute_name+'对loadbalance进行加压测试')
        test_command = 'source /etc/profile;cd /root/soft/jmeter/bin;nohup ./jmeter -n -t /root/soft/jmeter/projects/LB/lb_forever.jmx -l logfile.jtl >nohup.out 2>&1 &'
        stdin, stdout, stderr, exit_code = jmeter_sshclient.ssh_exec_command(command=test_command, timeout=20)
        if exit_code:
            stabilityLoadbalancerLogger.error('对均衡负载器加压云主机' + jmeter_compute_name + '重启失败' + '\r\n' + stderr.read())

        # 关闭ssh
        jmeter_sshclient.closeSSHAndSFTP()

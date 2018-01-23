#!-*- coding:utf8 -*-
import subprocess
from src.logger import stabilityObjectStorageLogger
from src.clients.objectstoreClient import ObjectStoreClient
from src.clients.keystoneClient import KeystoneClient
from src.clients.sshClient import SSHClient
from src.common import is_compute_online

class TestObjectstore():
    def __init__(self):
        pass

    def start(self,compute_obj,project_name):
        '''
        测试对象存储
        :param computes_obj:
        :param project_name:
        :return:
        '''
        if not compute_obj.float_ip:
            stabilityObjectStorageLogger.error('云主机'+compute_obj.name+'的浮动ip为空,无法重启对象存储测试')
            return
        compute_float_ip = compute_obj.float_ip
        compute_name = compute_obj.name
        stabilityObjectStorageLogger.info('开始检测云主机' + compute_name + '的ip:' + compute_float_ip + '是否可连通')
        is_online = is_compute_online(compute_float_ip)
        if not is_online:
            return

        # 获得ssh连接对象
        sshclient = SSHClient(compute_float_ip)

        # 上传本地所有文件到Jmeter客户端
        stabilityObjectStorageLogger.info('===从本地上传测试文件到Jmeter客户端===')
        sshclient.sftp_put_dir('/root/testfile','/root/soft/jmeter/projects/baiwucloud_s3/file')

        stabilityObjectStorageLogger.info('===参数化设置===')
        keystoneclient = KeystoneClient()
        objectstoreclient = ObjectStoreClient()
        project_id = keystoneclient.getProjectId(project_name)
        keys = objectstoreclient.getKeys(project_id)
        access_key = keys[0]
        secret_key = keys[1]
        ip = objectstoreclient.getIp()
        command ='sed -i "s/accesskey,secretkey,endPoint,createBucketPercent,createObjectPercent,deleteBucketPercent,deleteObjectPercent,downloadObjectPercent/'+access_key+','+secret_key+','+ip+',0-0,0-100,0-0,0-0,0-0/g" /root/soft/jmeter/projects/baiwucloud_s3/baiwucloud_s3.txt'
        command = command.encode('utf-8')
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command=command,timeout=180)
        if exit_code:
            stabilityObjectStorageLogger.error('设置'+compute_name+'参数化失败'+ '\r\n' + stderr.read())

        stabilityObjectStorageLogger.info('开始测试对象存储')
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command='source /etc/profile;cd /root/soft/jmeter/bin;nohup ./jmeter -n -t ../projects/baiwucloud_s3/baiwucloud_s3.jmx -l ../projects/baiwucloud_s3/result.jtl >nohup.out 2>&1 &',timeout=60)
        if exit_code:
            stabilityObjectStorageLogger.info('对象存储'+compute_name+'测试失败'+ '\r\n' + stderr.read())

        # 关闭ssh
        sshclient.closeSSHAndSFTP()

    def stop(self,compute_obj):
        """
        停止对象存储测试
        :param compute_obj:
        :return:
        """
        if not compute_obj.float_ip:
            stabilityObjectStorageLogger.error('云主机'+compute_obj.name+'的浮动ip为空,无法重启对象存储测试')
            return
        compute_float_ip = compute_obj.float_ip.encode('utf-8')
        compute_name = compute_obj.name.encode('utf-8')

        stabilityObjectStorageLogger.info('开始检测云主机' + compute_name + '的ip:' + compute_float_ip + '是否可连通')
        is_online = is_compute_online(compute_float_ip)
        if not is_online:
            return

        # 获得ssh连接对象
        sshclient = SSHClient(compute_float_ip)

        stabilityObjectStorageLogger.info('开始停止对象存储测试,云主机' + compute_name)
        stop_command = "kill -9 `ps -A |grep jmeter|awk '{print $1}'`"
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command=stop_command, timeout=20)
        if exit_code:
            stabilityObjectStorageLogger.error('停止云主机' + compute_name + '对象存储测试失败' + '\r\n' + stderr.read())

        # 关闭ssh
        sshclient.closeSSHAndSFTP()

    def reStart(self,compute_obj):
        '''
        重启对象存储
        :param compute_obj:
        :return:
        '''
        if not compute_obj.float_ip:
            stabilityObjectStorageLogger.error('云主机'+compute_obj.name+'的浮动ip为空,无法重启对象存储测试')
            return
        compute_float_ip = compute_obj.float_ip.encode('utf-8')
        compute_name = compute_obj.name.encode('utf-8')

        stabilityObjectStorageLogger.info('开始检测云主机'+compute_name+'的ip:'+compute_float_ip+'是否可连通')
        is_online = is_compute_online(compute_float_ip)
        if not is_online:
            return
        # 获得ssh连接对象
        sshclient = SSHClient(compute_float_ip)

        stabilityObjectStorageLogger.info('重启对象存储测试,云主机' + compute_name)
        test_command = 'source /etc/profile;cd /root/soft/jmeter/bin;nohup ./jmeter -n -t ../projects/baiwucloud_s3/baiwucloud_s3.jmx -l ../projects/baiwucloud_s3/result.jtl >nohup.out 2>&1 &'
        stdin, stdout, stderr, exit_code = sshclient.ssh_exec_command(command=test_command, timeout=20)
        if exit_code:
            stabilityObjectStorageLogger.error('对象存储Jmeter客户端' + compute_name + '重启失败' + '\r\n' + stderr.read())







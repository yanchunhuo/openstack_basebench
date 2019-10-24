#!-*- coding:utf8 -*-
from src.authTool import AuthTool
from src.common.strTool import StrTool
import subprocess
import ujson
import re

class ObjectStoreClient:

    def __init__(self):
        self._authTool=AuthTool()

    @staticmethod
    def getKeys(project_id):
        """
        获取存储密钥
        :param project_id:
        :return:
        """
        getKeys_commad = 'radosgw-admin user info --uid='+ project_id + ' --format=json'
        try:
            tmp_keys = subprocess.check_output(getKeys_commad,shell=True)
            keys = ujson.loads(tmp_keys)
            keys = keys['keys'][0]
            access_key = keys['access_key']
            secret_key = keys['secret_key']
            access_key.strip()
            secret_key.strip()
            if not access_key or not secret_key:
                return None
            return access_key,secret_key
        except Exception:
            return None

    def getIp(self):
        """
        获取存储地址
        :return:
        """
        commad = "openstack endpoint show -f json `openstack  endpoint list | grep swift_s3 | grep public | awk {'print $2'}`"
        commad = self._authTool.insertAdminAuth(commad)
        try:
            tmp_ip = subprocess.check_output(commad,shell=True)
            tmp_ip = ujson.dumps(tmp_ip)
            ip = StrTool.getStringWithLBRB(tmp_ip,'url\\\\": \\\\"http://','\\\\",','all')
            ip = ip[0].strip()
            if not ip:
                return None
            return ip
        except Exception:
            return None

    @staticmethod
    def deleteAllBuckets(project_id):
        """
        删除某账户下所有桶和文件
        :param project_id:
        :return:
        """
        command = "radosgw-admin bucket stats --uid=" + project_id + " -f json"
        tmp_buckets_name = subprocess.check_output(command, shell=True)
        tmp_buckets_name = ujson.loads(tmp_buckets_name)
        for bucketname in tmp_buckets_name:
            bucket_name = bucketname["bucket"]
            del_commad = "radosgw-admin bucket rm --bucket=" + bucket_name + " --purge-objects"
            subprocess.check_output(del_commad, shell=True)
        return True

    @staticmethod
    def deleteAccountBuckets(bucket_name):
        """
        删除符合搜索名称的桶和文件
        :param bucket_name:
        :return:
        """
        command = "radosgw-admin metadata list bucket|grep -i " + bucket_name
        try:
            tmp_buckets_name = subprocess.check_output(command, shell=True)
            pattern = re.compile('"(.*)"')
            buckets_name = pattern.findall(tmp_buckets_name)
            fbsArr = ["$", "(", ")", "*", "+", "[", "]", "?", "^", "{", "}", "|"]
            for bucket_name in buckets_name:
                command = "radosgw-admin  bucket check --bucket=" + bucket_name
                tmp_files_name = subprocess.check_output(command, shell=True)
                files_name = pattern.findall(tmp_files_name)
                for file_name in files_name:
                    for key in fbsArr:
                        if file_name.find(key) >= 0:
                            file_name = file_name.replace(key, "\\" + key)
                    del_file_command="radosgw-admin object rm --bucket=" + bucket_name + " --object=" + file_name
                    subprocess.check_output(del_file_command, shell=True)
                del_bucket_command = "radosgw-admin bucket rm --bucket=" + bucket_name + " --purge-objects"
                subprocess.check_output(del_bucket_command, shell=True)
        except subprocess.CalledProcessError as err:
                print("Command Error:", err)
        return True
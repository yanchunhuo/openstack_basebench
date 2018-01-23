#!-*- coding:utf8 -*-
import subprocess
import json
from src.logger import stabilityObjectStorageLogger
from src import common
from src.common import getStringWithLBRB


class ObjectStoreClient():

    def __init__(self):
        pass

    def getKeys(self,project_id):
        '''
        获取存储密钥
        :param project_id:
        :return:
        '''
        stabilityObjectStorageLogger.info('获取账号'+ project_id +'存储密钥')
        getKeys_commad = 'radosgw-admin user info --uid='+ project_id + ' --format=json'
        try:
            tmp_keys = subprocess.check_output(getKeys_commad,shell=True)
            keys = json.loads(tmp_keys)
            keys = keys['keys'][0]
            access_key = keys['access_key']
            secret_key = keys['secret_key']
            access_key.strip()
            secret_key.strip()
            if not access_key or not secret_key:
                stabilityObjectStorageLogger.error('获取项目'+ project_id +'存储密钥不存在')
                return None
            return access_key,secret_key
        except Exception,e:
            stabilityObjectStorageLogger.info('获取项目'+ project_id +'存储密钥异常'+'\r\n'+e.message)
            return None

    def getIp(self):
        '''
        获取存储地址
        :return:
        '''
        stabilityObjectStorageLogger.info('===获取存储地址===')
        commad = 'openstack endpoint show swift_s3 -f json'
        commad = common.insertAdminAuth(commad)
        try:
            ip = subprocess.check_output(commad,shell=True)
            ip = getStringWithLBRB(ip,'{"Field": "publicurl", "Value": "http://','"}')
            ip = ip.strip()
            if not ip:
                stabilityObjectStorageLogger.error('获取存储地址' + ip + '异常')
                return None
            return ip
        except Exception,e:
            stabilityObjectStorageLogger.error('获取存储地址' + ip + '异常' +'\r\n' +e.message)
            return None



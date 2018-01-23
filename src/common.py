#!-*- coding:utf8 -*-
from config.config import OS_TENANT_NAME
from config.config import OS_USERNAME
from config.config import OS_PASSWORD
from config.config import OS_AUTH_URL
from src.timeoutThread.checkComputeOnline import CheckComputeOnline
from src.timeoutThread.checkRemoteServiceOK import CheckRemoteServiceOK
import json
import re
import uuid



def novaInsertAuth(str,os_tenant_name,os_project_name,os_username,os_password):
    """
    nova相关命令行加入授权信息
    :param str:
    :param os_tenant_name:
    :param os_project_name:
    :param os_username:
    :param os_password:
    :return:
    """
    return str.replace(" ",' --os-username '+os_username+' --os-tenant-name '+os_tenant_name+' --os-project-name '+os_project_name+' --os-password '+os_password+' --os-auth-url '+OS_AUTH_URL+' ',1)

def neutronInsertAuth(str,os_tenant_name,os_username,os_password):
    """
    neutronInsertAuth相关命令行加入授权信息
    :param str:
    :param os_tenant_name:
    :param os_username:
    :param os_password:
    :return:
    """
    return str.replace(" ",' --os-username '+os_username+' --os-tenant-name '+os_tenant_name+' --os-password '+os_password+' --os-auth-url '+OS_AUTH_URL+' ',1)

def heatInsertAuth(str,os_tenant_name,os_project_name,os_username,os_password):
    """
    heatInsertAuth相关命令行加入授权信息
    :param str:
    :param os_tenant_name:
    :param os_project_name:
    :param os_username:
    :param os_password:
    :return:
    """
    return str.replace(" ",' --os-tenant-name '+os_tenant_name+' --os-project-name '+os_project_name+' --os-username '+os_username+' --os-password '+os_password+' --os-auth-url '+OS_AUTH_URL+' ',1)

def troveInsertAuth(str,os_tenant_name,os_project_name,os_username,os_password):
    """
    heatInsertAuth相关命令行加入授权信息
    :param str:
    :param os_tenant_name:
    :param os_project_name:
    :param os_username:
    :param os_password:
    :return:
    """
    return str.replace(" ",' --os-tenant-name '+os_tenant_name+' --os-project-name '+os_project_name+' --os-username '+os_username+' --os-password '+os_password+' --os-auth-url '+OS_AUTH_URL+' ',1)


def insertAdminAuth(str):
    """
    加入admin授权信息
    :param str:
    :return:
    """
    return str.replace(" ",' --os-username ' + OS_USERNAME + ' --os-tenant-name ' + OS_TENANT_NAME + ' --os-password ' + OS_PASSWORD + ' --os-auth-url ' + OS_AUTH_URL + ' ',1)

def getStringWithLBRB(sourceStr,lbStr,rbStr,offset=0):
    """
    根据字符串左右边界获取内容
    offset:要获得匹配的第几个数据,默认第一个
    :param sourceStr:
    :param lbStr:
    :param rbStr:
    :param offset:
    :return:
    """
    regex='([\\s\\S]*?)'
    r=re.compile(lbStr+regex+rbStr)
    result=r.findall(sourceStr)
    if str(offset) == 'all':
        return result
    else:
        return result[offset]

def is_compute_online(compute_ip):
    """
    判断主机能否连通，超时时间为3000秒
    :param compute_ip:
    :return:
    """
    checkComputeOnline = CheckComputeOnline(compute_ip)
    checkComputeOnline.start()
    checkComputeOnline.join(300)
    is_online = checkComputeOnline.getIsOnline()
    if not is_online:
        checkComputeOnline.setIsOnline(True)
        return False
    elif is_online:
        return True


def addUUID(source):
    return source+'_'+str(uuid.uuid4())

def writeObjectIntoFile(obj,filePath):
    """
    将对象转为json字符串，写入到文件
    :param obj:
    :param filePath:
    :return:
    """
    str = json.dumps(obj, default=lambda obj: obj.__dict__)
    with open(filePath,'w') as f:
        f.write(str)
        f.close()

def readJsonFromFile(filePath):
    """
    从文件里读取json字符串
    :param filePath:
    :return:
    """
    with open(filePath,'r') as f:
        result=f.read()
        f.close()
    result=json.loads(result)
    return result

def truncateFile(fielPath):
    """
    清空文件
    :param fielPath:
    :return:
    """
    with open(fielPath,'r+') as f:
        f.truncate()
        f.close()

def getLinesWithSplitWrap(str=''):
    """
    分割换行读取每一行,只读取每一行字符数大于10的行
    :param str:
    :return:
    """
    str=str.strip()
    lines_array=[]
    lines=str.split('\n')
    for line in lines:
        if len(line)>10:
            lines_array.append(line)
    return lines_array

def is_remoteService_OK(remote_ip,port):
    """
    检测服务器端口是否可用
    :param remote_ip:
    :param port:
    :return:
    """
    checkRemoteServiceOK=CheckRemoteServiceOK(remote_ip,port)
    checkRemoteServiceOK.start()
    checkRemoteServiceOK.join(30)
    is_OK=checkRemoteServiceOK.getIsOK()
    if not is_OK:
        checkRemoteServiceOK.setIsOK(True)
        return False
    elif is_OK:
        return True



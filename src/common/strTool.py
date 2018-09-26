#!-*- coding:utf8 -*-
import json
import re
import random
import string
import uuid

class StrTool:

    def __init__(self):
        pass

    @classmethod
    def getStringWithLBRB(cls,sourceStr,lbStr,rbStr,offset=0):
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
            if len(result)>=offset and len(result)!=0:
                return result[offset]
            else:
                return None

    @classmethod
    def addUUID(cls,source):
        """
        字符串加上uuid
        :param source:
        :return:
        """
        return source+'_'+str(uuid.uuid4())

    @classmethod
    def objectToJsonStr(cls,object):
        """
        将类对象转为json字符串
        :param object:
        :return:
        """
        return json.dumps(object, default=lambda obj: obj.__dict__)

    @classmethod
    def getSpecifiedStr(cls,length,char):
        """
        根据字符获取指定长度的字符串
        :param length:
        :param char:
        :return:
        """
        result=''
        for i in range(int(length)):
            result=result+str(char)
        return result

    @classmethod
    def addFix(cls,sourceStr,isPre=False,preStr='',isSuffix=False,suffixStr=''):
        """
        字符串加前后缀
        :param sourceStr:
        :param isPre:
        :param preStr:
        :param isSuffix:
        :param suffixStr:
        :return:
        """
        preStr=str(preStr).strip()
        suffixStr=str(suffixStr).strip()
        if isPre and isSuffix:
            return '{}{}{}'.format(preStr,sourceStr,suffixStr)
        elif isSuffix:
            return '{}{}'.format(sourceStr,suffixStr)
        elif isPre:
            return '{}{}'.format(preStr,sourceStr)
        else:
            return sourceStr

    @classmethod
    def getRandomChar(cls):
        """
        随机获取a-zA-Z的单个字符
        :return:
        """
        str=string.ascii_letters
        return random.choice(str)

    @classmethod
    def getLinesWithSplitWrap(cls,str=''):
        """
        分割换行读取每一行,只读取每一行字符数大于10的行
        :param str:
        :return:
        """
        str = str.strip()
        lines_array = []
        lines = str.split('\n')
        for line in lines:
            if len(line) > 10:
                lines_array.append(line)
        return lines_array

    @classmethod
    def getStringWithDic(cls,sourceStr, Str):
        """
        获取键值
        :param sourceStr:
        :param Str:
        :return:
        """
        tmp_result = json.loads(sourceStr)
        result = tmp_result[Str].strip()
        return result
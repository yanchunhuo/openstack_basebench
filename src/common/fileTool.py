#!-*- coding:utf8 -*-
import ujson

class FileTool:
    def __init__(self):
        pass

    @classmethod
    def writeObjectIntoFile(cls,obj,filePath):
        """
        将对象转为json字符串，写入到文件
        :param obj:
        :param filePath:
        :return:
        """
        str = ujson.dumps(obj)
        with open(filePath,'w') as f:
            f.write(str)
            f.close()

    @classmethod
    def readJsonFromFile(cls,filePath):
        """
        从文件里读取json字符串
        :param filePath:
        :return:
        """
        with open(filePath,'r') as f:
            result=f.read()
            f.close()
        result=ujson.loads(result)
        return result

    @classmethod
    def truncateFile(cls,fielPath):
        """
        清空文件
        :param fielPath:
        :return:
        """
        with open(fielPath,'r+') as f:
            f.truncate()
            f.close()
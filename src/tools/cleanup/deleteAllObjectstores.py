#!-*- coding:utf8 -*-
from src.clients.objectstoreClient import ObjectStoreClient
from src.readConfig import ReadConfig

class DeleteAllObjectStores:

    def __init__(self):
        self._readConfig = ReadConfig()
        self._objectstoreClient = ObjectStoreClient()

    def deletebuckets(self):
        """
        删除某账户下所有桶和文件
        :return:
        """
        self._objectstoreClient.deleteAccountBuckets(self._readConfig.tools.cleanup_keyword)
        return True
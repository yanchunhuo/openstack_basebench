# -*- coding:utf8 -*-
from src.pojo.LoggersConfig import LoggersConfig
import configparser as ConfigParser
import logging.handlers

class Loggers(object):
    __instance = None
    __inited = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__inited is None:
            self._loggersConfig=self._readConfig()

            self._formatter=logging.Formatter("%(asctime)s %(levelname)s %(message)s")

            self.basebenchLogger=self._initBasebenchLogger()
            self.stabilityFioLogger=self._initStabilityFioLogger()
            self.stabilityHeatLogger = self._initStabilityHeatLogger()
            self.stabilityIperfLogger = self._initStabilityIperfLogger()
            self.stabilityLoadbalancerLogger = self._initStabilityLoadbalancerLogger()
            self.stabilityMemtesterLogger = self._initStabilityMemtesterLogger()
            self.stabilityObjstoreLogger = self._initStabilityObjstoreLogger()
            self.stabilitySysbenchLogger = self._initStabilitySysbenchLogger()
            self.stabilityUnixbenchLogger = self._initStabilityUnixbenchLogger()

        self.__inited = True

    @staticmethod
    def _readConfig():
        config = ConfigParser.ConfigParser()
        config.read("config/loggers.conf")
        loggersConifg=LoggersConfig()
        loggersConifg.basebench_test_log_path=config.get('log_path','basebench_test_log_path')
        loggersConifg.stability_test_fio_log_path=config.get('log_path','stability_test_fio_log_path')
        loggersConifg.stability_test_heat_log_path=config.get('log_path','stability_test_heat_log_path')
        loggersConifg.stability_test_iperf_log_path=config.get('log_path','stability_test_iperf_log_path')
        loggersConifg.stability_test_loadbalancer_log_path=config.get('log_path','stability_test_loadbalancer_log_path')
        loggersConifg.stability_test_memtester_log_path=config.get('log_path','stability_test_memtester_log_path')
        loggersConifg.stability_test_objstore_log_path=config.get('log_path','stability_test_objstore_log_path')
        loggersConifg.stability_test_sysbench_log_path=config.get('log_path','stability_test_sysbench_log_path')
        loggersConifg.stability_test_unixbench_log_path=config.get('log_path','stability_test_unixbench_log_path')
        return loggersConifg

    def _initBasebenchLogger(self):
        basebenchFileHandler = logging.handlers.RotatingFileHandler(self._loggersConfig.basebench_test_log_path, 'a')
        basebenchStreamHandler = logging.StreamHandler()
        basebenchFileHandler.setFormatter(self._formatter)
        basebenchStreamHandler.setFormatter(self._formatter)
        basebenchLogger = logging.getLogger("basebench_logger")
        basebenchLogger.setLevel(logging.INFO)
        basebenchLogger.addHandler(basebenchFileHandler)
        basebenchLogger.addHandler(basebenchStreamHandler)
        return basebenchLogger

    def _initStabilityFioLogger(self):
        stabilityFioFileHandler = logging.handlers.RotatingFileHandler(self._loggersConfig.stability_test_fio_log_path, 'a')
        stabilityFioStreamHandler = logging.StreamHandler()
        stabilityFioFileHandler.setFormatter(self._formatter)
        stabilityFioStreamHandler.setFormatter(self._formatter)
        stabilityFioLogger = logging.getLogger("stability_fio_logger")
        stabilityFioLogger.setLevel(logging.INFO)
        stabilityFioLogger.addHandler(stabilityFioFileHandler)
        stabilityFioLogger.addHandler(stabilityFioStreamHandler)
        return stabilityFioLogger

    def _initStabilityHeatLogger(self):
        stabilityHeatFileHandler = logging.handlers.RotatingFileHandler(self._loggersConfig.stability_test_heat_log_path, 'a')
        stabilityHeatStreamHandler = logging.StreamHandler()
        stabilityHeatFileHandler.setFormatter(self._formatter)
        stabilityHeatStreamHandler.setFormatter(self._formatter)
        stabilityHeatLogger = logging.getLogger("stability_heat_logger")
        stabilityHeatLogger.setLevel(logging.INFO)
        stabilityHeatLogger.addHandler(stabilityHeatFileHandler)
        stabilityHeatLogger.addHandler(stabilityHeatStreamHandler)
        return stabilityHeatLogger

    def _initStabilityIperfLogger(self):
        stabilityIperfFileHandler = logging.handlers.RotatingFileHandler(self._loggersConfig.stability_test_iperf_log_path, 'a')
        stabilityIperfStreamHandler = logging.StreamHandler()
        stabilityIperfFileHandler.setFormatter(self._formatter)
        stabilityIperfStreamHandler.setFormatter(self._formatter)
        stabilityIperfLogger = logging.getLogger("stability_iperf_logger")
        stabilityIperfLogger.setLevel(logging.INFO)
        stabilityIperfLogger.addHandler(stabilityIperfFileHandler)
        stabilityIperfLogger.addHandler(stabilityIperfStreamHandler)
        return stabilityIperfLogger

    def _initStabilityLoadbalancerLogger(self):
        stabilityLoadbalancerFileHandler = logging.handlers.RotatingFileHandler(self._loggersConfig.stability_test_loadbalancer_log_path, 'a')
        stabilityLoadbalancerStreamHandler = logging.StreamHandler()
        stabilityLoadbalancerFileHandler.setFormatter(self._formatter)
        stabilityLoadbalancerStreamHandler.setFormatter(self._formatter)
        stabilityLoadbalancerLogger = logging.getLogger("stability_loadbalancer_logger")
        stabilityLoadbalancerLogger.setLevel(logging.INFO)
        stabilityLoadbalancerLogger.addHandler(stabilityLoadbalancerFileHandler)
        stabilityLoadbalancerLogger.addHandler(stabilityLoadbalancerStreamHandler)
        return stabilityLoadbalancerLogger

    def _initStabilityMemtesterLogger(self):
        stabilityMemtesterFileHandler = logging.handlers.RotatingFileHandler(self._loggersConfig.stability_test_memtester_log_path, 'a')
        stabilityMemtesterStreamHandler = logging.StreamHandler()
        stabilityMemtesterFileHandler.setFormatter(self._formatter)
        stabilityMemtesterStreamHandler.setFormatter(self._formatter)
        stabilityMemtesterLogger = logging.getLogger("stability_memtester_logger")
        stabilityMemtesterLogger.setLevel(logging.INFO)
        stabilityMemtesterLogger.addHandler(stabilityMemtesterFileHandler)
        stabilityMemtesterLogger.addHandler(stabilityMemtesterStreamHandler)
        return stabilityMemtesterLogger

    def _initStabilityObjstoreLogger(self):
        stabilityObjstoreFileHandler = logging.handlers.RotatingFileHandler(self._loggersConfig.stability_test_objstore_log_path, 'a')
        stabilityObjstoreStreamHandler = logging.StreamHandler()
        stabilityObjstoreFileHandler.setFormatter(self._formatter)
        stabilityObjstoreStreamHandler.setFormatter(self._formatter)
        stabilityObjstoreLogger = logging.getLogger("stability_objstore_logger")
        stabilityObjstoreLogger.setLevel(logging.INFO)
        stabilityObjstoreLogger.addHandler(stabilityObjstoreFileHandler)
        stabilityObjstoreLogger.addHandler(stabilityObjstoreStreamHandler)
        return stabilityObjstoreLogger

    def _initStabilitySysbenchLogger(self):
        stabilitySysbenchFileHandler = logging.handlers.RotatingFileHandler(self._loggersConfig.stability_test_sysbench_log_path, 'a')
        stabilitySysbenchStreamHandler = logging.StreamHandler()
        stabilitySysbenchFileHandler.setFormatter(self._formatter)
        stabilitySysbenchStreamHandler.setFormatter(self._formatter)
        stabilitySysbenchLogger = logging.getLogger("stability_sysbench_logger")
        stabilitySysbenchLogger.setLevel(logging.INFO)
        stabilitySysbenchLogger.addHandler(stabilitySysbenchFileHandler)
        stabilitySysbenchLogger.addHandler(stabilitySysbenchStreamHandler)
        return stabilitySysbenchLogger

    def _initStabilityUnixbenchLogger(self):
        stabilityUnixbenchFileHandler = logging.handlers.RotatingFileHandler(self._loggersConfig.stability_test_unixbench_log_path, 'a')
        stabilityUnixbenchStreamHandler = logging.StreamHandler()
        stabilityUnixbenchFileHandler.setFormatter(self._formatter)
        stabilityUnixbenchStreamHandler.setFormatter(self._formatter)
        stabilityUnixbenchLogger = logging.getLogger("stability_unixbench_logger")
        stabilityUnixbenchLogger.setLevel(logging.INFO)
        stabilityUnixbenchLogger.addHandler(stabilityUnixbenchFileHandler)
        stabilityUnixbenchLogger.addHandler(stabilityUnixbenchStreamHandler)
        return stabilityUnixbenchLogger


# -*- coding:utf8 -*-
from src.pojo.AccountsConfig import AccountsConfig
from src.pojo.BaseConfig import BaseConfig
from src.pojo.ExecuteTestConfig import ExcuteTestConfig
from src.pojo.ToolsConfig import ToolsConfig
import configparser as ConfigParser

class ReadConfig(object):
    __instance = None
    __inited = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__inited is None:
            self.accounts = self._readAccountsConfig()
            self.base = self._readBaseConfig()
            self.executeTest = self._readExecuteTestConfig()
            self.tools = self._readToolsConfig()
        self.__inited = True

    @staticmethod
    def _readAccountsConfig():
        config = ConfigParser.ConfigParser()
        config.read('config/accounts.conf')
        accountsConfig = AccountsConfig()

        # [basebench]
        accountsConfig.basebench_os_tenant_name = config.get('basebench','basebench_os_tenant_name')
        accountsConfig.basebench_os_project_name = config.get('basebench','basebench_os_project_name')
        accountsConfig.basebench_os_username = config.get('basebench','basebench_os_username')
        accountsConfig.basebench_os_password = config.get('basebench','basebench_os_password')

        # [stability]
        accountsConfig.stability_fio_os_tenant_name = config.get('stability','stability_fio_os_tenant_name')
        accountsConfig.stability_fio_os_project_name = config.get('stability','stability_fio_os_project_name')
        accountsConfig.stability_fio_os_username = config.get('stability','stability_fio_os_username')
        accountsConfig.stability_fio_os_password = config.get('stability','stability_fio_os_password')

        accountsConfig.stability_unixbench_os_tenant_name = config.get('stability','stability_unixbench_os_tenant_name')
        accountsConfig.stability_unixbench_os_project_name = config.get('stability','stability_unixbench_os_project_name')
        accountsConfig.stability_unixbench_os_username = config.get('stability','stability_unixbench_os_username')
        accountsConfig.stability_unixbench_os_password = config.get('stability','stability_unixbench_os_password')

        accountsConfig.stability_memtester_os_tenant_name = config.get('stability','stability_memtester_os_tenant_name')
        accountsConfig.stability_memtester_os_project_name = config.get('stability','stability_memtester_os_project_name')
        accountsConfig.stability_memtester_os_username = config.get('stability','stability_memtester_os_username')
        accountsConfig.stability_memtester_os_password = config.get('stability','stability_memtester_os_password')

        accountsConfig.stability_iperf_os_tenant_name = config.get('stability','stability_iperf_os_tenant_name')
        accountsConfig.stability_iperf_os_project_name = config.get('stability','stability_iperf_os_project_name')
        accountsConfig.stability_iperf_os_username = config.get('stability','stability_iperf_os_username')
        accountsConfig.stability_iperf_os_password = config.get('stability','stability_iperf_os_password')

        accountsConfig.stability_loadbalancer_os_tenant_name = config.get('stability','stability_loadbalancer_os_tenant_name')
        accountsConfig.stability_loadbalancer_os_project_name = config.get('stability','stability_loadbalancer_os_project_name')
        accountsConfig.stability_loadbalancer_os_username = config.get('stability','stability_loadbalancer_os_username')
        accountsConfig.stability_loadbalancer_os_password = config.get('stability','stability_loadbalancer_os_password')

        accountsConfig.stability_heat_os_tenant_name = config.get('stability','stability_heat_os_tenant_name')
        accountsConfig.stability_heat_os_project_name = config.get('stability','stability_heat_os_project_name')
        accountsConfig.stability_heat_os_username = config.get('stability','stability_heat_os_username')
        accountsConfig.stability_heat_os_password = config.get('stability','stability_heat_os_password')

        accountsConfig.stability_objstore_os_tenant_name = config.get('stability','stability_objstore_os_tenant_name')
        accountsConfig.stability_objstore_os_project_name = config.get('stability','stability_objstore_os_project_name')
        accountsConfig.stability_objstore_os_username = config.get('stability','stability_objstore_os_username')
        accountsConfig.stability_objstore_os_password = config.get('stability','stability_objstore_os_password')

        accountsConfig.stability_sysbench_os_tenant_name = config.get('stability','stability_sysbench_os_tenant_name')
        accountsConfig.stability_sysbench_os_project_name = config.get('stability','stability_sysbench_os_project_name')
        accountsConfig.stability_sysbench_os_username = config.get('stability','stability_sysbench_os_username')
        accountsConfig.stability_sysbench_os_password = config.get('stability','stability_sysbench_os_password')

        return accountsConfig

    @staticmethod
    def _readBaseConfig():
        config = ConfigParser.ConfigParser()
        config.read('config/base.conf')
        baseConfig=BaseConfig()

        # [admin_auth]
        baseConfig.admin_os_tenant_name=config.get('admin_auth','admin_os_tenant_name')
        baseConfig.admin_os_project_name = config.get('admin_auth','admin_os_project_name')
        baseConfig.admin_os_username = config.get('admin_auth','admin_os_username')
        baseConfig.admin_os_password = config.get('admin_auth','admin_os_password')
        baseConfig.os_auth_url = config.get('admin_auth','os_auth_url')

        # [network]
        baseConfig.default_secgroup_name = config.get('network', 'default_secgroup_name')
        baseConfig.admin_float_net_name = config.get('network', 'admin_float_net_name')
        baseConfig.float_ip_qos = config.get('network', 'float_ip_qos')

        # [volume]
        baseConfig.volume_type_names = config.get('volume', 'volume_type_names')

        # [image]
        baseConfig.test_image_name = config.get('image', 'test_image_name')

        # [nova]
        baseConfig.zone_names = config.get('nova', 'zone_names')
        baseConfig.flavor_type_names = config.get('nova', 'flavor_type_names')
        baseConfig.compute_user_name = config.get('nova', 'compute_user_name')
        baseConfig.compute_user_password = config.get('nova', 'compute_user_password')

        return baseConfig

    @staticmethod
    def _readExecuteTestConfig():
        config = ConfigParser.ConfigParser()
        config.read('config/executeTest.conf')
        excuteTestConfig=ExcuteTestConfig()

        # [basebench_test]
        excuteTestConfig.is_basebench_test_fio = config.get('basebench_test', 'is_basebench_test_fio')
        excuteTestConfig.is_basebench_test_unixbench = config.get('basebench_test', 'is_basebench_test_unixbench')
        excuteTestConfig.is_basebench_test_iperf = config.get('basebench_test', 'is_basebench_test_iperf')

        excuteTestConfig.basebench_test_fio_types = config.get('basebench_test', 'basebench_test_fio_types')
        excuteTestConfig.basebench_test_fio_volume_types = config.get('basebench_test', 'basebench_test_fio_volume_types')
        excuteTestConfig.basebench_test_fio_flavor = config.get('basebench_test', 'basebench_test_fio_flavor')
        excuteTestConfig.basebench_test_fio_volume_size = config.get('basebench_test', 'basebench_test_fio_volume_size')
        excuteTestConfig.basebench_test_fio_depth = config.get('basebench_test', 'basebench_test_fio_depth')

        excuteTestConfig.basebench_test_unixbench_flavors = config.get('basebench_test', 'basebench_test_unixbench_flavors')

        excuteTestConfig.basebench_test_iperf_flavor = config.get('basebench_test', 'basebench_test_iperf_flavor')

        # [stability_test]
        excuteTestConfig.is_stability_test_fio = config.get('stability_test', 'is_stability_test_fio')
        excuteTestConfig.is_stability_test_iperf = config.get('stability_test', 'is_stability_test_iperf')
        excuteTestConfig.is_stability_test_unixbench = config.get('stability_test', 'is_stability_test_unixbench')
        excuteTestConfig.is_stability_test_memtester = config.get('stability_test', 'is_stability_test_memtester')
        excuteTestConfig.is_stability_test_sysbench = config.get('stability_test', 'is_stability_test_sysbench')
        excuteTestConfig.is_stability_test_loadbalancer = config.get('stability_test', 'is_stability_test_loadbalancer')
        excuteTestConfig.is_stability_test_heat = config.get('stability_test', 'is_stability_test_heat')
        excuteTestConfig.is_stability_test_objstroe = config.get('stability_test', 'is_stability_test_objstroe')

        excuteTestConfig.stability_test_fio_types = config.get('stability_test', 'stability_test_fio_types')
        excuteTestConfig.stability_test_fio_volume_types_and_num = config.get('stability_test', 'stability_test_fio_volume_types_and_num')
        excuteTestConfig.stability_test_fio_flavor = config.get('stability_test', 'stability_test_fio_flavor')
        excuteTestConfig.stability_test_fio_volume_size = config.get('stability_test', 'stability_test_fio_volume_size')
        excuteTestConfig.stability_test_fio_depth = config.get('stability_test', 'stability_test_fio_depth')
        excuteTestConfig.stability_test_fio_seconds = config.get('stability_test', 'stability_test_fio_seconds')

        excuteTestConfig.stability_test_memtester_num = config.get('stability_test', 'stability_test_memtester_num')
        excuteTestConfig.stability_test_memtester_flavor = config.get('stability_test', 'stability_test_memtester_flavor')
        excuteTestConfig.stability_test_memtester_mem = config.get('stability_test', 'stability_test_memtester_mem')
        excuteTestConfig.stability_test_memtester_times = config.get('stability_test', 'stability_test_memtester_times')

        excuteTestConfig.stability_test_iperf_group_num = config.get('stability_test', 'stability_test_iperf_group_num')
        excuteTestConfig.stability_test_iperf_flavor = config.get('stability_test', 'stability_test_iperf_flavor')
        excuteTestConfig.stability_test_iperf_seconds = config.get('stability_test', 'stability_test_iperf_seconds')

        excuteTestConfig.stability_test_objstore_load_flavor = config.get('stability_test', 'stability_test_objstore_load_flavor')
        excuteTestConfig.stability_test_objstore_files_dir = config.get('stability_test', 'stability_test_objstore_files_dir')

        excuteTestConfig.stability_test_sysbench_group_num = config.get('stability_test', 'stability_test_sysbench_group_num')
        excuteTestConfig.stability_test_sysbench_flavor = config.get('stability_test', 'stability_test_sysbench_flavor')

        excuteTestConfig.stability_test_heat_group_num = config.get('stability_test', 'stability_test_heat_group_num')
        excuteTestConfig.stability_test_heat_flavor = config.get('stability_test', 'stability_test_heat_flavor')


        excuteTestConfig.stability_test_unixbench_num = config.get('stability_test', 'stability_test_unixbench_num')
        excuteTestConfig.stability_test_unixbench_flavor = config.get('stability_test', 'stability_test_unixbench_flavor')
        excuteTestConfig.stability_test_unixbench_cpu = config.get('stability_test', 'stability_test_unixbench_cpu')
        excuteTestConfig.stability_test_unixbench_times = config.get('stability_test', 'stability_test_unixbench_times')

        excuteTestConfig.stability_test_loadbalancer_group_num = config.get('stability_test', 'stability_test_loadbalancer_group_num')
        excuteTestConfig.stability_test_loadbalancer_member_num = config.get('stability_test', 'stability_test_loadbalancer_member_num')
        excuteTestConfig.stability_test_loadbalancer_flavor = config.get('stability_test', 'stability_test_loadbalancer_flavor')
        excuteTestConfig.stability_test_loadbalancer_member_weight = config.get('stability_test', 'stability_test_loadbalancer_member_weight')
        excuteTestConfig.stability_test_loadbalancer_connection_limit = config.get('stability_test', 'stability_test_loadbalancer_connection_limit')
        excuteTestConfig.stability_test_loadbalancer_protocol = config.get('stability_test', 'stability_test_loadbalancer_protocol')
        excuteTestConfig.stability_test_loadbalancer_protocol_port = config.get('stability_test', 'stability_test_loadbalancer_protocol_port')
        excuteTestConfig.stability_test_loadbalancer_lb_algorithmt = config.get('stability_test', 'stability_test_loadbalancer_lb_algorithmt')
        excuteTestConfig.stability_test_loadbalancer_delay_time = config.get('stability_test', 'stability_test_loadbalancer_delay_time')
        excuteTestConfig.stability_test_loadbalancer_max_retries = config.get('stability_test', 'stability_test_loadbalancer_max_retries')
        excuteTestConfig.stability_test_loadbalancer_timeout = config.get('stability_test', 'stability_test_loadbalancer_timeout')
        excuteTestConfig.stability_test_loadbalancer_protocol_type = config.get('stability_test', 'stability_test_loadbalancer_protocol_type')

        return excuteTestConfig

    @staticmethod
    def _readToolsConfig():
        config = ConfigParser.ConfigParser()
        config.read('config/tools.conf')

        toolsConfig=ToolsConfig()

        # [cleanup]
        toolsConfig.cleanup_keyword = config.get('cleanup','cleanup_keyword')

        return toolsConfig
class ExcuteTestConfig:
    def __init__(self):
        self.is_basebench_test_fio = None
        self.is_basebench_test_unixbench = None
        self.is_basebench_test_iperf = None
        self.basebench_test_fio_types = None
        self.basebench_test_fio_volume_types = None
        self.basebench_test_fio_flavor = None
        self.basebench_test_fio_volume_size = None
        self.basebench_test_fio_depth = None
        self.basebench_test_unixbench_flavors = None
        self.basebench_test_iperf_flavor = None

        self.is_stability_test_fio = None
        self.is_stability_test_iperf = None
        self.is_stability_test_unixbench = None
        self.is_stability_test_memtester = None
        self.is_stability_test_sysbench = None
        self.is_stability_test_loadbalancer = None
        self.is_stability_test_heat = None
        self.is_stability_test_objstore = None

        self.stability_test_fio_types = None
        self.stability_test_fio_volume_types_and_num = None
        self.stability_test_fio_flavor = None
        self.stability_test_fio_volume_size = None
        self.stability_test_fio_depth = None
        self.stability_test_fio_seconds = None

        self.stability_test_memtester_num = None
        self.stability_test_memtester_flavor = None
        self.stability_test_memtester_mem = None
        self.stability_test_memtester_times = None

        self.stability_test_iperf_group_num = None
        self.stability_test_iperf_flavor = None
        self.stability_test_iperf_seconds = None

        self.stability_test_objstore_load_flavor = None
        self.stability_test_objstore_files_dir = None

        self.stability_test_sysbench_group_num = None
        self.stability_test_sysbench_flavor = None

        self.stability_test_heat_group_num = None
        self.stability_test_heat_flavor = None

        self.stability_test_unixbench_num = None
        self.stability_test_unixbench_flavor = None
        self.stability_test_unixbench_cpu = None
        self.stability_test_unixbench_times = None

        self.stability_test_loadbalancer_group_num = None
        self.stability_test_loadbalancer_member_num = None
        self.stability_test_loadbalancer_flavor = None
        self.stability_test_loadbalancer_member_weight = None
        self.stability_test_loadbalancer_connection_limit = None
        self.stability_test_loadbalancer_protocol = None
        self.stability_test_loadbalancer_protocol_port = None
        self.stability_test_loadbalancer_lb_algorithmt = None
        self.stability_test_loadbalancer_delay_time = None
        self.stability_test_loadbalancer_max_retries = None
        self.stability_test_loadbalancer_timeout = None
        self.stability_test_loadbalancer_protocol_type = None

    @property
    def stability_test_loadbalancer_protocol_type(self):
        return self.stability_test_loadbalancer_protocol_type

    @stability_test_loadbalancer_protocol_type.setter
    def stability_test_loadbalancer_protocol_type(self, stability_test_loadbalancer_protocol_type):
        self.stability_test_loadbalancer_protocol_type = stability_test_loadbalancer_protocol_type

    @property
    def stability_test_loadbalancer_timeout(self):
        return self.stability_test_loadbalancer_timeout

    @stability_test_loadbalancer_timeout.setter
    def stability_test_loadbalancer_timeout(self, stability_test_loadbalancer_timeout):
        self.stability_test_loadbalancer_timeout = stability_test_loadbalancer_timeout

    @property
    def stability_test_loadbalancer_max_retries(self):
        return self.stability_test_loadbalancer_max_retries

    @stability_test_loadbalancer_max_retries.setter
    def stability_test_loadbalancer_max_retries(self, stability_test_loadbalancer_max_retries):
        self.stability_test_loadbalancer_max_retries = stability_test_loadbalancer_max_retries

    @property
    def stability_test_loadbalancer_delay_time(self):
        return self.stability_test_loadbalancer_delay_time

    @stability_test_loadbalancer_delay_time.setter
    def stability_test_loadbalancer_delay_time(self, stability_test_loadbalancer_delay_time):
        self.stability_test_loadbalancer_delay_time = stability_test_loadbalancer_delay_time

    @property
    def stability_test_loadbalancer_lb_algorithmt(self):
        return self.stability_test_loadbalancer_lb_algorithmt

    @stability_test_loadbalancer_lb_algorithmt.setter
    def stability_test_loadbalancer_lb_algorithmt(self, stability_test_loadbalancer_lb_algorithmt):
        self.stability_test_loadbalancer_lb_algorithmt = stability_test_loadbalancer_lb_algorithmt

    @property
    def stability_test_loadbalancer_protocol_port(self):
        return self.stability_test_loadbalancer_protocol_port

    @stability_test_loadbalancer_protocol_port.setter
    def stability_test_loadbalancer_protocol_port(self, stability_test_loadbalancer_protocol_port):
        self.stability_test_loadbalancer_protocol_port = stability_test_loadbalancer_protocol_port

    @property
    def stability_test_loadbalancer_protocol(self):
        return self.stability_test_loadbalancer_protocol

    @stability_test_loadbalancer_protocol.setter
    def stability_test_loadbalancer_protocol(self, stability_test_loadbalancer_protocol):
        self.stability_test_loadbalancer_protocol = stability_test_loadbalancer_protocol

    @property
    def stability_test_loadbalancer_connection_limit(self):
        return self.stability_test_loadbalancer_connection_limit

    @stability_test_loadbalancer_connection_limit.setter
    def stability_test_loadbalancer_connection_limit(self, stability_test_loadbalancer_connection_limit):
        self.stability_test_loadbalancer_connection_limit = stability_test_loadbalancer_connection_limit

    @property
    def stability_test_loadbalancer_member_weight(self):
        return self.stability_test_loadbalancer_member_weight

    @stability_test_loadbalancer_member_weight.setter
    def stability_test_loadbalancer_member_weight(self, stability_test_loadbalancer_member_weight):
        self.stability_test_loadbalancer_member_weight = stability_test_loadbalancer_member_weight

    @property
    def stability_test_loadbalancer_flavor(self):
        return self.stability_test_loadbalancer_flavor

    @stability_test_loadbalancer_flavor.setter
    def stability_test_loadbalancer_flavor(self, stability_test_loadbalancer_flavor):
        self.stability_test_loadbalancer_flavor = stability_test_loadbalancer_flavor

    @property
    def stability_test_loadbalancer_member_num(self):
        return self.stability_test_loadbalancer_member_num

    @stability_test_loadbalancer_member_num.setter
    def stability_test_loadbalancer_member_num(self, stability_test_loadbalancer_member_num):
        self.stability_test_loadbalancer_member_num = stability_test_loadbalancer_member_num

    @property
    def stability_test_loadbalancer_group_num(self):
        return self.stability_test_loadbalancer_group_num

    @stability_test_loadbalancer_group_num.setter
    def stability_test_loadbalancer_group_num(self, stability_test_loadbalancer_group_num):
        self.stability_test_loadbalancer_group_num = stability_test_loadbalancer_group_num

    @property
    def stability_test_unixbench_times(self):
        return self.stability_test_unixbench_times

    @stability_test_unixbench_times.setter
    def stability_test_unixbench_times(self, stability_test_unixbench_times):
        self.stability_test_unixbench_times = stability_test_unixbench_times

    @property
    def stability_test_unixbench_cpu(self):
        return self.stability_test_unixbench_cpu

    @stability_test_unixbench_cpu.setter
    def stability_test_unixbench_cpu(self, stability_test_unixbench_cpu):
        self.stability_test_unixbench_cpu = stability_test_unixbench_cpu

    @property
    def stability_test_unixbench_flavor(self):
        return self.stability_test_unixbench_flavor

    @stability_test_unixbench_flavor.setter
    def stability_test_unixbench_flavor(self, stability_test_unixbench_flavor):
        self.stability_test_unixbench_flavor = stability_test_unixbench_flavor

    @property
    def stability_test_unixbench_num(self):
        return self.stability_test_unixbench_num

    @stability_test_unixbench_num.setter
    def stability_test_unixbench_num(self, stability_test_unixbench_num):
        self.stability_test_unixbench_num = stability_test_unixbench_num

    @property
    def stability_test_heat_flavor(self):
        return self.stability_test_heat_flavor

    @stability_test_heat_flavor.setter
    def stability_test_heat_flavor(self, stability_test_heat_flavor):
        self.stability_test_heat_flavor = stability_test_heat_flavor

    @property
    def stability_test_heat_group_num(self):
        return self.stability_test_heat_group_num

    @stability_test_heat_group_num.setter
    def stability_test_heat_group_num(self, stability_test_heat_group_num):
        self.stability_test_heat_group_num = stability_test_heat_group_num

    @property
    def stability_test_sysbench_flavor(self):
        return self.stability_test_sysbench_flavor

    @stability_test_sysbench_flavor.setter
    def stability_test_sysbench_flavor(self, stability_test_sysbench_flavor):
        self.stability_test_sysbench_flavor = stability_test_sysbench_flavor

    @property
    def stability_test_sysbench_group_num(self):
        return self.stability_test_sysbench_group_num

    @stability_test_sysbench_group_num.setter
    def stability_test_sysbench_group_num(self, stability_test_sysbench_group_num):
        self.stability_test_sysbench_group_num = stability_test_sysbench_group_num

    @property
    def stability_test_objstore_files_dir(self):
        return self.stability_test_objstore_files_dir

    @stability_test_objstore_files_dir.setter
    def stability_test_objstore_files_dir(self,stability_test_objstore_files_dir):
        self.stability_test_objstore_files_dir=stability_test_objstore_files_dir

    @property
    def stability_test_objstore_load_flavor(self):
        return self.stability_test_objstore_load_flavor

    @stability_test_objstore_load_flavor.setter
    def stability_test_objstore_load_flavor(self,stability_test_objstore_load_flavor):
        self.stability_test_objstore_load_flavor=stability_test_objstore_load_flavor

    @property
    def stability_test_iperf_seconds(self):
        return self.stability_test_iperf_seconds

    @stability_test_iperf_seconds.setter
    def stability_test_iperf_seconds(self,stability_test_iperf_seconds):
        self.stability_test_iperf_seconds=stability_test_iperf_seconds

    @property
    def stability_test_iperf_flavor(self):
        return self.stability_test_iperf_flavor

    @stability_test_iperf_flavor.setter
    def stability_test_iperf_flavor(self,stability_test_iperf_flavor):
        self.stability_test_iperf_flavor=stability_test_iperf_flavor

    @property
    def stability_test_iperf_group_num(self):
        return self.stability_test_iperf_group_num

    @stability_test_iperf_group_num.setter
    def stability_test_iperf_group_num(self,stability_test_iperf_group_num):
        self.stability_test_iperf_group_num=stability_test_iperf_group_num

    @property
    def stability_test_memtester_times(self):
        return self.stability_test_memtester_times

    @stability_test_memtester_times.setter
    def stability_test_memtester_times(self,stability_test_memtester_times):
        self.stability_test_memtester_times=stability_test_memtester_times

    @property
    def stability_test_memtester_mem(self):
        return self.stability_test_memtester_mem

    @stability_test_memtester_mem.setter
    def stability_test_memtester_mem(self,stability_test_memtester_mem):
        self.stability_test_memtester_mem=stability_test_memtester_mem

    @property
    def stability_test_memtester_flavor(self):
        return self.stability_test_memtester_flavor

    @stability_test_memtester_flavor.setter
    def stability_test_memtester_flavor(self,stability_test_memtester_flavor):
        self.stability_test_memtester_flavor=stability_test_memtester_flavor

    @property
    def stability_test_memtester_num(self):
        return self.stability_test_memtester_num

    @stability_test_memtester_num.setter
    def stability_test_memtester_num(self,stability_test_memtester_num):
        self.stability_test_memtester_num=stability_test_memtester_num

    @property
    def stability_test_fio_seconds(self):
        return self.stability_test_fio_seconds

    @stability_test_fio_seconds.setter
    def stability_test_fio_seconds(self,stability_test_fio_seconds):
        self.stability_test_fio_seconds=stability_test_fio_seconds

    @property
    def stability_test_fio_depth(self):
        return self.stability_test_fio_depth

    @stability_test_fio_depth.setter
    def stability_test_fio_depth(self,stability_test_fio_depth):
        self.stability_test_fio_depth=stability_test_fio_depth

    @property
    def stability_test_fio_volume_size(self):
        return self.stability_test_fio_volume_size

    @stability_test_fio_volume_size.setter
    def stability_test_fio_volume_size(self,stability_test_fio_volume_size):
        self.stability_test_fio_volume_size=stability_test_fio_volume_size

    @property
    def stability_test_fio_flavor(self):
        return self.stability_test_fio_flavor

    @stability_test_fio_flavor.setter
    def stability_test_fio_flavor(self,stability_test_fio_flavor):
        self.stability_test_fio_flavor=stability_test_fio_flavor

    @property
    def stability_test_fio_volume_types_and_num(self):
        return self.stability_test_fio_volume_types_and_num

    @stability_test_fio_volume_types_and_num.setter
    def stability_test_fio_volume_types_and_num(self,stability_test_fio_volume_types_and_num):
        self.stability_test_fio_volume_types_and_num=stability_test_fio_volume_types_and_num

    @property
    def stability_test_fio_types(self):
        return self.stability_test_fio_types

    @stability_test_fio_types.setter
    def stability_test_fio_types(self,stability_test_fio_types):
        self.stability_test_fio_types=stability_test_fio_types

    @property
    def is_stability_test_objstore(self):
        return self.is_stability_test_objstore

    @is_stability_test_objstore.setter
    def is_stability_test_objstore(self,is_stability_test_objstore):
        self.is_stability_test_objstore=is_stability_test_objstore

    @property
    def is_stability_test_heat(self):
        return self.is_stability_test_heat

    @is_stability_test_heat.setter
    def is_stability_test_heat(self,is_stability_test_heat):
        self.is_stability_test_heat=is_stability_test_heat

    @property
    def is_stability_test_loadbalancer(self):
        return self.is_stability_test_loadbalancer

    @is_stability_test_loadbalancer.setter
    def is_stability_test_loadbalancer(self,is_stability_test_loadbalancer):
        self.is_stability_test_loadbalancer=is_stability_test_loadbalancer

    @property
    def is_stability_test_sysbench(self):
        return self.is_stability_test_sysbench

    @is_stability_test_sysbench.setter
    def is_stability_test_sysbench(self,is_stability_test_sysbench):
        self.is_stability_test_sysbench=is_stability_test_sysbench

    @property
    def is_stability_test_memtester(self):
        return self.is_stability_test_memtester

    @is_stability_test_memtester.setter
    def is_stability_test_memtester(self,is_stability_test_memtester):
        self.is_stability_test_memtester=is_stability_test_memtester

    @property
    def is_stability_test_unixbench(self):
        return self.is_stability_test_unixbench

    @is_stability_test_unixbench.setter
    def is_stability_test_unixbench(self,is_stability_test_unixbench):
        self.is_stability_test_unixbench=is_stability_test_unixbench

    @property
    def is_stability_test_iperf(self):
        return self.is_stability_test_iperf

    @is_stability_test_iperf.setter
    def is_stability_test_iperf(self,is_stability_test_iperf):
        self.is_stability_test_iperf=is_stability_test_iperf

    @property
    def is_stability_test_fio(self):
        return self.is_stability_test_fio

    @is_stability_test_fio.setter
    def is_stability_test_fio(self,is_stability_test_fio):
        self.is_stability_test_fio=is_stability_test_fio

    @property
    def is_basebench_test_fio(self):
        return self.is_basebench_test_fio

    @is_basebench_test_fio.setter
    def is_basebench_test_fio(self,is_basebench_test_fio):
        self.is_basebench_test_fio=is_basebench_test_fio

    @property
    def is_basebench_test_unixbench(self):
        return self.is_basebench_test_unixbench

    @is_basebench_test_unixbench.setter
    def is_basebench_test_unixbench(self,is_basebench_test_unixbench):
        self.is_basebench_test_unixbench=is_basebench_test_unixbench

    @property
    def is_basebench_test_iperf(self):
        return self.is_basebench_test_iperf

    @is_basebench_test_iperf.setter
    def is_basebench_test_iperf(self,is_basebench_test_iperf):
        self.is_basebench_test_iperf=is_basebench_test_iperf

    @property
    def basebench_test_fio_types(self):
        return self.basebench_test_fio_types

    @basebench_test_fio_types.setter
    def basebench_test_fio_types(self,basebench_test_fio_types):
        self.basebench_test_fio_types=basebench_test_fio_types

    @property
    def basebench_test_fio_volume_types(self):
        return self.basebench_test_fio_volume_types

    @basebench_test_fio_volume_types.setter
    def basebench_test_fio_volume_types(self,basebench_test_fio_volume_types):
        self.basebench_test_fio_volume_types=basebench_test_fio_volume_types

    @property
    def basebench_test_fio_flavor(self):
        return self.basebench_test_fio_flavor

    @basebench_test_fio_flavor.setter
    def basebench_test_fio_flavor(self,basebench_test_fio_flavor):
        self.basebench_test_fio_flavor=basebench_test_fio_flavor

    @property
    def basebench_test_fio_volume_size(self):
        return self.basebench_test_fio_volume_size

    @basebench_test_fio_volume_size.setter
    def basebench_test_fio_volume_size(self,basebench_test_fio_volume_size):
        self.basebench_test_fio_volume_size=basebench_test_fio_volume_size

    @property
    def basebench_test_fio_depth(self):
        return self.basebench_test_fio_depth

    @basebench_test_fio_depth.setter
    def basebench_test_fio_depth(self,basebench_test_fio_depth):
        self.basebench_test_fio_depth=basebench_test_fio_depth

    @property
    def basebench_test_unixbench_flavors(self):
        return self.basebench_test_unixbench_flavors

    @basebench_test_unixbench_flavors.setter
    def basebench_test_unixbench_flavors(self,basebench_test_unixbench_flavors):
        self.basebench_test_unixbench_flavors=basebench_test_unixbench_flavors

    @property
    def basebench_test_iperf_flavor(self):
        return self.basebench_test_iperf_flavor

    @basebench_test_iperf_flavor.setter
    def basebench_test_iperf_flavor(self,basebench_test_iperf_flavor):
        self.basebench_test_iperf_flavor=basebench_test_iperf_flavor

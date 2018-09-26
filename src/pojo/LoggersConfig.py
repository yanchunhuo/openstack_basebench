class LoggersConfig:
    def __init__(self):
        self.basebench_test_log_path=None
        self.stability_test_iperf_log_path=None
        self.stability_test_memtester_log_path=None
        self.stability_test_unixbench_log_path=None
        self.stability_test_sysbench_log_path=None
        self.stability_test_heat_log_path=None
        self.stability_test_loadbalancer_log_path=None
        self.stability_test_fio_log_path=None
        self.stability_test_objstore_log_path=None

    @property
    def basebench_test_log_path(self):
        return self.basebench_test_log_path

    @basebench_test_log_path.setter
    def basebench_test_log_path(self,basebench_test_log_path):
        self.basebench_test_log_path=basebench_test_log_path

    @property
    def stability_test_iperf_log_path(self):
        return self.stability_test_iperf_log_path

    @stability_test_iperf_log_path.setter
    def stability_test_iperf_log_path(self, stability_test_iperf_log_path):
        self.stability_test_iperf_log_path = stability_test_iperf_log_path

    @property
    def stability_test_memtester_log_path(self):
        return self.stability_test_memtester_log_path

    @stability_test_memtester_log_path.setter
    def stability_test_memtester_log_path(self, stability_test_memtester_log_path):
        self.stability_test_memtester_log_path = stability_test_memtester_log_path

    @property
    def stability_test_unixbench_log_path(self):
        return self.stability_test_unixbench_log_path

    @stability_test_unixbench_log_path.setter
    def stability_test_unixbench_log_path(self, stability_test_unixbench_log_path):
        self.stability_test_unixbench_log_path = stability_test_unixbench_log_path

    @property
    def stability_test_sysbench_log_path(self):
        return self.stability_test_sysbench_log_path

    @stability_test_sysbench_log_path.setter
    def stability_test_sysbench_log_path(self, stability_test_sysbench_log_path):
        self.stability_test_sysbench_log_path = stability_test_sysbench_log_path

    @property
    def stability_test_heat_log_path(self):
        return self.stability_test_heat_log_path

    @stability_test_heat_log_path.setter
    def stability_test_heat_log_path(self, stability_test_heat_log_path):
        self.stability_test_heat_log_path = stability_test_heat_log_path

    @property
    def stability_test_loadbalancer_log_path(self):
        return self.stability_test_loadbalancer_log_path

    @stability_test_loadbalancer_log_path.setter
    def stability_test_loadbalancer_log_path(self, stability_test_loadbalancer_log_path):
        self.stability_test_loadbalancer_log_path = stability_test_loadbalancer_log_path

    @property
    def stability_test_fio_log_path(self):
        return self.stability_test_fio_log_path

    @stability_test_fio_log_path.setter
    def stability_test_fio_log_path(self, stability_test_fio_log_path):
        self.stability_test_fio_log_path = stability_test_fio_log_path

    @property
    def stability_test_objstore_log_path(self):
        return self.stability_test_objstore_log_path

    @stability_test_objstore_log_path.setter
    def stability_test_objstore_log_path(self, stability_test_objstore_log_path):
        self.stability_test_objstore_log_path = stability_test_objstore_log_path
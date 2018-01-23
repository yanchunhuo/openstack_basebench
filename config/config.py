#!-*- coding:utf8 -*-

"""
[openrc]
"""
#管理员账号信息
LC_ALL=''
OS_NO_CACHE='true'
OS_TENANT_NAME='admin'
OS_PROJECT_NAME='admin'
OS_USERNAME='admin'
OS_PASSWORD='admin'
OS_AUTH_URL='http://172.31.0.2:5000/'
OS_DEFAULT_DOMAIN='default'
OS_AUTH_STRATEGY='keystone'
OS_REGION_NAME='RegionOne'
CINDER_ENDPOINT_TYPE='internalURL'
GLANCE_ENDPOINT_TYPE='internalURL'
KEYSTONE_ENDPOINT_TYPE='internalURL'
NOVA_ENDPOINT_TYPE='internalURL'
NEUTRON_ENDPOINT_TYPE='internalURL'
OS_ENDPOINT_TYPE='internalURL'
MURANO_REPO_URL='http://storage.apps.openstack.org/'

"""
[network]
"""
DEFAULT_SECGROUP_NAME='default'
ADMIN_FLOAT_NET_NAME='admin_floating_net'
#浮动ip带宽,单位:Mbit/s
FLOAT_IP_QOS=200

"""
[volume]
"""
#平台云硬盘类型名字,格式：{'type':'type_name','type':'type_name'}
VOLUME_TYPE_NAME={'sata':'VolumeType_SATA','sas':'VolumeType_SATA','ssd':'VolumeType_SATA'}

"""
[image]
"""
#使用的镜像名称
TEST_IMAGE_NAME='基准测试镜像'
#平台云主机规格名字,每一种格式：{'flavor_x_x':'flavor_name'}
FLAVOR_TYPE_NAME={'flavor_2_8':'memory-2','flavor_8_8':'compute-8'}

"""
[nova]
"""
#可用域名称,至少两个可用域，否则无法进行iperf基准性能测试
ZONE_NAMES=['default','node2']
#用于连接云主机的用户名,确保和user_data里的用户名保持一致
COMPUTE_USER_NAME='root'
#用于连接云主机的用户密码,确保和user_data里的用户密码保持一致
COMPUTE_USER_PASSWORD='123456..'

"""
[basePerFormanceTest]
"""
#设置需要测试哪些基准测试
IS_TEST_FIO=True
IS_TEST_UNIXBENCH=True
IS_TEST_IPERF=True
#FIO测试的类型,包括:read、write、randread、randwrite、randrw
#不测试的类型删除即可
WHAT_FIO_TEST={'read','write','randread','randwrite','randrw'}
#测试fio的磁盘类型,此处类型需要在VOLUME_TYPE_NAME中存在
#不测试的类型删除即可
TEST_FIO_VOLUME_TYPE=['sata','sas','ssd']
#测试FIO使用的云主机规格,此处规格需要在FLAVOR_TYPE_NAME中存在
TEST_FIO_FLAVOR='flavor_8_8'
#测试FIO云硬盘大小,单位GB
TEST_FIO_VOLUME_SIZE=200
#测试FIO寻址空间大小,需小于云硬盘大小,单位GB
TEST_FIO_SIZE=100
#测试unixbench使用的云主机规格,此处规格需要在FLAVOR_TYPE_NAME中存在
TEST_UNIXBENCH_FLAVOR=['flavor_4_8','flavor_8_8','flavor_8_16','flavor_16_32']
#测试iperf使用的云主机规格,此处规格需要在FLAVOR_TYPE_NAME中存在，建议为8核８G
TEST_IPERF_FLAVOR='flavor_8_8'

"""
[stabilityTest]
"""
#设置需要测试哪些稳定性测试
IS_STABILITY_TEST_FIO=True
IS_STABILITY_TEST_IPERF=True
IS_STABILITY_TEST_UNIXBENCH=True
IS_STABILITY_TEST_MEMTESTER=True
IS_STABILITY_TEST_SYSBENCH=True
IS_STABILITY_TEST_JMETER=True
IS_STABILITY_TEST_LOADBALANCER=True
IS_STABILITY_TEST_HEAT=True
IS_STABILITY_TEST_OBJECTSTORAGE=True


#稳定性测试FIO测试的类型，一般write即可
STABILITY_TEST_FIO_WHAT=['write','read','randrw']
#稳定性测试fio的磁盘类型,此处类型需要在VOLUME_TYPE_NAME中存在
#不测试的类型删除即可
STABILITY_TEST_FIO_VOLUME_TYPE={'sata':'2','ssd':'3'}
#稳定性测试FIO使用的云主机规格,此处规格需要在FLAVOR_TYPE_NAME中存在
STABILITY_TEST_FIO_FLAVOR='flavor_8_8'
#稳定性测试FIO云硬盘大小,单位GB
STABILITY_TEST_FIO_VOLUME_SIZE=200
#稳定性测试FIO寻址空间大小,需小于云硬盘大小,单位GB
STABILITY_TEST_FIO_SIZE=100
#稳定性测试FIO测试时间,如7*24小时,单位秒
STABILITY_TEST_FIO_TIME=36000

#稳定性测试MEMTESTER云主机数
STABILITY_TEST_MEMTESTER_NUM=10
#稳定性测试MEMTESTER使用的云主机规格,此处规格需要在FLAVOR_TYPE_NAME中存在
STABILITY_TEST_MEMTESTER_FLAVOR='flavor_8_8'
#稳定性测试MEMTESTER需要使用云主机内存大小,建议为总内存的80％
STABILITY_TEST_MEMTESTER_MEM=6400
#稳定性测试MEMTESTER的测试次数
STABILITY_TEST_MEMTESTER_TIMES=100000

#测试iperf起的组数,每组两台云主机
STABILITY_TEST_IPERF_GROUP_NUM=3
STABILITY_TEST_IPERF_FLAVOR='flavor_8_8'
#稳定性测试iperf测试时间,如7*24小时,单位秒
STABILITY_TEST_IPERF_TIME=36000

#稳定性测试对象存储负载机使用的云主机规格
STABILITY_TEST_OSS_FLAVOR = 'flavor_8_8'

#测试sysbench起的组数,每组两台云主机
STABILITY_TEST_SYSBENCH_GROUP_NUM=1
STABILITY_TEST_SYSBENCH_FLAVOR='flavor_8_8'

#稳定性测试heat起的组数,每组3台云主机
STABILITY_TEST_HEAT_GROUP_NUM=1
STABILITY_TEST_HEAT_FLAVOR='flavor_8_8'


#稳定性测试UNIXBENCH云主机数
STABILITY_TEST_UNIXBENCH_NUM=10
#稳定性测试UNIXBENCH使用的云主机规格,此处规格需要在FLAVOR_TYPE_NAME中存在
STABILITY_TEST_UNIXBENCH_FLAVOR='flavor_8_8'
#稳定性测试UNIXBENCH需要使用云主机CPU总大小
STABILITY_TEST_UNIXBENCH_CPU=8
#稳定性测试UNIXBENCH的测试次数
STABILITY_TEST_UNIXBENCH_TIMES=100000000

#测试loadbalancer起的组数,每组五台云主机
STABILITY_TEST_LOADBALANCER_GROUP_NUM=3
STABILITY_TEST_LOADBALANCER_MEMBER_NUM=5
STABILITY_TEST_LOADBALANCER_FLAVOR='flavor_8_8'
#每个负载均衡器有多少个后端服务器就有多少个相应的权重,以下参数可默认
STABILITY_TEST_LOADBALANCER_MEMBER_WEIGHT=[1,1,1,1,1]
connection_limit='5000'
protocol='HTTP'
protocol_port='80'
lb_algorithmt='ROUND_ROBIN'
delay_time='22'
max_retries='3'
timeout='10'
protocol_type='PING'



"""
[Accounts]以下内容可不进行更改
"""
BASE_ACCOUNT_OS_TENANT_NAME='basebench'
BASE_ACCOUNT_OS_PROJECT_NAME='basebench'
BASE_ACCOUNT_OS_USERNAME='basebench'
BASE_ACCOUNT_OS_PASSWORD='123456..'

STABILITY_FIO_ACCOUNT_OS_TENANT_NAME='stability_fio'
STABILITY_FIO_ACCOUNT_OS_PROJECT_NAME='stability_fio'
STABILITY_FIO_ACCOUNT_OS_USERNAME='stability_fio'
STABILITY_FIO_ACCOUNT_OS_PASSWORD='123456..'

STABILITY_UNIXBENCH_ACCOUNT_OS_TENANT_NAME='stability_unixbench'
STABILITY_UNIXBENCH_ACCOUNT_OS_PROJECT_NAME='stability_unixbench'
STABILITY_UNIXBENCH_ACCOUNT_OS_USERNAME='stability_unixbench'
STABILITY_UNIXBENCH_ACCOUNT_OS_PASSWORD='123456..'

STABILITY_MEMTESTER_ACCOUNT_OS_TENANT_NAME='stability_memtester'
STABILITY_MEMTESTER_ACCOUNT_OS_PROJECT_NAME='stability_memtester'
STABILITY_MEMTESTER_ACCOUNT_OS_USERNAME='stability_memtester'
STABILITY_MEMTESTER_ACCOUNT_OS_PASSWORD='123456..'

STABILITY_IPERF_ACCOUNT_OS_TENANT_NAME='stability_iperf'
STABILITY_IPERF_ACCOUNT_OS_PROJECT_NAME='stability_iperf'
STABILITY_IPERF_ACCOUNT_OS_USERNAME='stability_iperf'
STABILITY_IPERF_ACCOUNT_OS_PASSWORD='123456..'

STABILITY_LOADBALANCER_ACCOUNT_OS_TENANT_NAME='stability_loadbalancer'
STABILITY_LOADBALANCER_ACCOUNT_OS_PROJECT_NAME='stability_loadbalancer'
STABILITY_LOADBALANCER_ACCOUNT_OS_USERNAME='stability_loadbalancer'
STABILITY_LOADBALANCER_ACCOUNT_OS_PASSWORD='123456..'

STABILITY_HEAT_ACCOUNT_OS_TENANT_NAME='stability_heat'
STABILITY_HEAT_ACCOUNT_OS_PROJECT_NAME='stability_heat'
STABILITY_HEAT_ACCOUNT_OS_USERNAME='stability_heat'
STABILITY_HEAT_ACCOUNT_OS_PASSWORD='123456..'

STABILITY_OBJECTSTORE_ACCOUNT_OS_TENANT_NAME='stability_oss'
STABILITY_OBJECTSTORE_ACCOUNT_OS_PROJECT_NAME='stability_oss'
STABILITY_OBJECTSTORE_ACCOUNT_OS_USERNAME='stability_oss'
STABILITY_OBJECTSTORE_ACCOUNT_OS_PASSWORD='123456..'

STABILITY_SYSBENCH_ACCOUNT_OS_TENANT_NAME='stability_sysbench'
STABILITY_SYSBENCH_ACCOUNT_OS_PROJECT_NAME='stability_sysbench'
STABILITY_SYSBENCH_ACCOUNT_OS_USERNAME='stability_sysbench'
STABILITY_SYSBENCH_ACCOUNT_OS_PASSWORD='123456..'




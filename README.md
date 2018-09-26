# [特性]()
* 支持openstack O版本
* 创建的资源名称皆以basebench开头
* 可根据资源名称的关键字清除平台资源

# [使用方法]()
* 请在openstack控制节点使用本项目

## 一、创建python虚拟环境 
### 1、安装虚拟环境
* pip install virtualenv
* virtualenv --no-site-package testEnv

### 2、在虚拟环境里安装依赖模块
* cd testEnv/
* source bin/activate
* pip install -r requirements.txt

### 3、下载测试代码
* git clone http://124.239.146.247:9091/baiwucloud/basebench.git

## 二、开始测试
### 1、修改配置
* cd basebench
* 根据实际情况修改config/base.conf
* 根据实际情况修改config/executeTest.conf
* 根据实际情况修改config/tools.conf

### 2、基准测试 
* python runTest.py -t startBasebench & 运行基准测试
* python runTest.py -t freeBasebenchResource & 释放基准测试资源

### 3、稳定性测试
* python runTest.py -t startStability & 运行稳定性测试
* python runTest.py -t stopStability & 停止稳定性测试
* python runTest.py -t restartStability & 重启稳定性测试
* python runTest.py -t freeStabilityResource & 释放稳定性测试资源

### 4、清除平台资源
* python cleanup.py &

# [目录结构]()
* config 基础配置文件
* dbs 测试创建的资源信息，以json格式存储
* heat_template 创建伸缩所需的模板
* logs　日志
* output 基准测试结果存放目录
* src 业务代码 
* userdata 云主机启动所需要的数据

# [项目介绍]()
* 项目分为基准测试、稳定性测试、清除平台资源
* 基准测试包括iperf/fio/unixbench
* 稳定性测试包括iperf/fio/unixbench/memtester/loadbalancer/heat/trove/objectstore
* 清除平台资源将清除名称包含关键字的云主机、云硬盘、对象存储、路由、网络、账户及名下浮动ip等资源
* 基准性能测试在一个账号里完成
* 稳定性测试每一种类型的测试都在各自的一个账号里完成
* 稳定性测试每一种类型的测试在启动、停止、释放资源时都分别有一个线程处理

# [注意点]()
* 本项目中的客户端不可直接用于平台接口的性能测试脚本，因为部分资源是创建成功后才继续的
* 稳定性在控制节点执行，确保浮动ip够
* 云主机挂载云硬盘时，默认使用/dev/vdc设备，/dev/vdb用于做密码注入

# [编码规范]()
* 编写脚本时，名字相关请确保唯一
* 编写脚本时，python文件开头都不指定解释器
* 类、方法的注释均写在def下一行，并且用三个双引号形式注释
* 局部代码注释使用#号

# [测试软件相关版本]()
* memtester 4.3.0
* fio 2.14
* iperf 3.1.3
* unixbench 5.1.2
* sysbench 1.0.8
* iftop 1.0pre4
* jmeter 2.13

# [作者]()
* wangxiurong
* zhangpingyun
* limingya
* yanchunhuo
 
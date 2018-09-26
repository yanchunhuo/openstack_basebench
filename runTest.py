#-*- coding:utf8 -*-
from src.basebench.testBasebench import TestBasebench
from src.testStability.testStability import TestStability
import argparse

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('-t','--type',help='执行何种测试,可以有startBasebench(基准测试)、freeBasebenchResource(释放基准测试资源)、startStability(稳定性测试)、stopStability(停止稳定性测试)、restartStability(重启稳定性测试)、freeStabilityResource(释放稳定性测试资源)',type=str)
    args=parser.parse_args()

    testType=args.type
    testBasebench = TestBasebench()
    testStability = TestStability()
    if testType=='startBasebench':
        testBasebench.start()
    elif testType=='freeBasebenchResource':
        testBasebench.free()
    elif testType=='startStability':
        testStability.start()
    elif testType=='stopStability':
        testStability.stop()
    elif testType=='restartStability':
        testStability.restart()
    elif testType=='freeStabilityResource':
        testStability.free()
    else :
        print '测试类型错误,使用-h查看使用说明'

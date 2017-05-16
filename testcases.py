#coding=utf-8
import time,io,sys,os,re
from PyIxChariot.km import *
from PyIxChariot.kt import *
from PyIxChariot.kc import *
def cur_file_dir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path.decode('gbk')
     elif os.path.isfile(path):
         return os.path.dirname(path).decode('gbk')
rootdir=cur_file_dir()
kc=kc()
kt=kt(rootdir=rootdir)
# kt1=testcfg(intf="ra0",serverip="192.168.0.3")
km=km(rootdir=rootdir)
#初始化环境
if __name__ == "__main__":
    # while True:
    tL=[8,10,15]
    for i in tL:
        funct_name="testcase%s" %(i)
        try:
            eval(funct_name)()
        except Exception,e:
            print str(e)
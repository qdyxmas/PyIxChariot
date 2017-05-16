#!/usr/bin/python
#encoding=utf-8

import os,sys,time,re
import socket,struct
from Tkinter import Tcl
tcl = Tcl()
class km():
    def __init__(self,rootdir="./"):
        self.script = os.path.join(rootdir,"Script","Throughput.scr").replace("\\","/")
        self.downscript=os.path.join(rootdir,"Script","Throughputdown.scr").replace("\\","/")
        self.chariot_result=rootdir+"result"
    def save_chariot(allstr=None):
        fd = open(self.chariot_result,"a+")
        fd.write(allstr+"\n")
        fd.close()
    def run_Ixchariot(self,**kargs):
        self.start_ip = kargs['sip'].split(" ")
        self.sip_len=len(self.start_ip)
        self.dst_ip = kargs['dip'].split(" ")
        self.dip_len=len(self.dst_ip)
        self.sum_pair = kargs['sum_pair']
        self.tx_pair= kargs['tx_pair']
        self.proto = kargs['proto'].upper()
        self.run_time =  kargs['run_time']
        
        tcl.eval("load ChariotExt")
        tcl.eval("package require ChariotExt")

        #导入后进行设置
        #根据IP地址和页面配置生成.tsc
        #循环2次取比较大的值
        max_ret=0.0
        for loop in range(1,3):
            if not "name" in kargs.keys():
                test_result=gettime()+".tst"
            else:
                test_result=kargs['name']+"_"+gettime()+".tst"
            test_now=os.path.join("./result",test_result).replace("\\","/")
            print "test_now=",test_now
            #创建test
            tcl.eval("set test [chrTest new]")
            #设置运行时间
            tcl.eval("set runOpts [chrTest getRunOpts $test]")
            tcl.eval("chrRunOpts set $runOpts TEST_END FIXED_DURATION")
            tcl.eval("chrRunOpts set $runOpts TEST_DURATION %d" %(self.run_time))
            #向test中添加pair
            
            for i in range(0,self.sum_pair):
                tcl.eval("set pair%d [chrPair new]"%i)
                tcl.eval("chrPair set [set pair%d] PROTOCOL %s" %(i,self.proto.upper()))
                tcl.eval("chrPair set [set pair%d] E1_ADDR %s" %(i,self.start_ip[i%self.sip_len]))
                tcl.eval("chrPair set [set pair%d] E2_ADDR %s" %(i,self.dst_ip[i%self.dip_len]))
                if i< self.tx_pair:
                    tcl.eval("chrPair useScript [set pair%d] \"%s\" " %(i,self.script))
                else:
                    tcl.eval("chrPair useScript [set pair%d] \"%s\" " %(i,self.downscript))
                tcl.eval("chrTest addPair $test [set pair%d]"%(i))
            tcl.eval("chrTest start $test")
            time.sleep(2)
            if self.run_time<10:
                chktime=60
            else:
                chktime=3*self.run_time
            for j in range(0,chktime):
                ret=tcl.eval("chrTest isStopped $test")
                print "ret=",ret
                print "j=%d total=%d" %(j,chktime)
                time.sleep(1)
                if ret == "1":
                    print u"chariot run done"
                    break
                else:
                    time.sleep(2)
                if j>self.run_time:
                    try:
                        tcl.eval("chrTest stop $test")
                    except Exception,e:
                        print str(e)
            #获取测试结果
            max_runtime=1
            errnum=0
            sum_throught=0.0
            for j in range(0,self.sum_pair):
                try:
                    run_pair_time=tcl.eval("set runingtime [chrCommonResults get [set pair%d] MEAS_TIME]" %(j))
                    # print "run_pair_time=",run_pair_time
                    run_pair_time=float(run_pair_time)
                    if run_pair_time >max_runtime:
                        max_runtime=run_pair_time
                    throuput_pair=tcl.eval("set throughput [chrPairResults get [set pair%d] THROUGHPUT]" %(j))
                    avg_throuput=throuput_pair.split(" ")[0]
                    sum_throught=sum_throught+float(avg_throuput)*run_pair_time
                except Exception,e:
                    errnum=errnum+1
                    print str(e)
            print "sum_throught=",sum_throught
            print "max_runtime=",max_runtime
            if self.run_time-max_runtime<=1:
                max_runtime=float(self.run_time)
            
            ret=sum_throught/max_runtime
            # print u"平均吞吐量为%.3f" %(sum_throught/max_runtime)
            tcl.eval("chrTest save $test \"%s\"" %(test_now))
            tcl.eval("chrTest delete $test force")
            if max_ret<ret:
                max_ret=ret
            # if sum_throught >100:
                # break
        #打开刚刚创建的数据流
        # os.startfile(test_now)
        max_ret="%.3f" %(max_ret)
        return max_ret
        
if __name__ == "__main__":
    km_obj=km()
    kargs={"sip":"127.0.0.1 127.0.0.1","dip":"127.0.0.1 127.0.0.1","sum_pair":20,"tx_pair":20,"proto":"TCP","run_time":10}
    km_obj.run_Ixchariot(**kargs)
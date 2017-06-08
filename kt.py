#!/usr/bin/python
#coding=utf-8
import time,io,sys,os,re
from socket import *
import serial
class kt():
    def __init__(self,intf="ra0",serverip="",rootdir="./"):
        # 删除多余的配置文件
        if serverip:
            self.serverip=serverip
            self.cmdExec="tcpcli.exe %s " %(self.serverip)
        else:
            self.serverip=""
            self.cmdExec=""
        if intf == "ra0":
            print "sendcmd=",self.cmd_str("""netsh wlan show profile""")
            cmd = os.popen(self.cmd_str("""netsh wlan show profile"""))
            ss=cmd.read().split("\n")
            for i in ss:
                ssid=re.search(" : .*",i)
                if ssid:
                    delcmd="""netsh wlan delete profile name=%s""" %(i.split(":")[-1])
                    os.system(self.cmd_str(delcmd))
            cfgname=(rootdir+"/config/ra0-tenda_ganraoceshi.xml").replace("\\","/")
            print cfgname
            if self.cmdExec:
                cmd="""netsh wlan add profile filename=c:\\tcpser\\ra0-tenda_ganraoceshi.xml interface=ra0"""
            else:
               cmd="netsh wlan add profile filename=%s interface=ra0" %(cfgname)
            if not os.system(self.cmd_str(cmd)):
                print "__init__ suc"
            #
        self.intf=intf;
        # self.index=self.get_register_mac_info()
    #以下2个为ping函数
    def echoping(self,dip="192.168.0.252",timeout=1,sip=None):
        if not sip:
            cmd="ping %s -w %s -n 1" %(dip,timeout*1000)
        else:
            cmd="ping %s -w %s -S %s -n 1" %(dip,timeout*1000,sip)
        print "cmd=",cmd
        ret = os.popen(self.cmd_str(cmd))
        retstr="".join(ret.readlines())
        print retstr
        if retstr.find("TTL=") != -1:
            return True
        else:
            time.sleep(timeout)
            return False

    def pingtest(self,**kargs):
        sucnum = 0
        errnum = 0
        if not "dip" in kargs.keys():
            dip="192.168.10.1"
        else:
            dip=kargs["dip"]
        if not "sip" in kargs.keys():
            sip=None
        else:
            sip=kargs["sip"]
        if not "timeout" in kargs.keys():
            timeout=1
        else:
            timeout=kargs["timeout"]
        if not "maxerr" in kargs.keys():
            maxerr=60
        else:
            maxerr=kargs["maxerr"]
        if not "maxsuc" in kargs.keys():
            maxsuc=5
        else:
            maxsuc=kargs["maxsuc"]
        if not "expe" in kargs.keys():
            expe=True
        else:
            expe=kargs["expe"]
        flag=False
        #等待3秒
        print u"等待10秒"
        time.sleep(10)
        for i in range(0,maxerr+1):
            if self.echoping(dip=dip,timeout=timeout,sip=sip):
                sucnum+=1
                time.sleep(1)
            else:
                errnum+=1
                time.sleep(1)
            if sucnum == maxsuc:
                flag=True
                break
        if flag == expe:
            return True
        else:
            return False
    #连接无线函数 调用ra0接口连接无线DUT
    def windows_link_wireless(self,**kargs):
        #以下是配置windows连接无线ssid的命令
        #set cmd "netsh wlan disconnect interface=ra0
        for i in range(0,3):
            time.sleep(1)
            try:
                cmd=[]
                cmd.append("netsh wlan disconnect interface=ra0")
                cmd.append("netsh interface set interface ra0 disable")
                cmd.append("netsh interface set interface ra0 enabled")
                cmd.append("netsh wlan connect name=tenda_ganraoceshi")
                #set cmd "netsh wlan add profile filename=c:\\tcpser\\ra0-cfg.xml interface=ra0"
                #1、设置配置文件
                #2、配置配置文件
                #3、连接配置文件
                #4、
                if not self.windows_cfg_wireless(**kargs):
                    continue
                for subcmd in cmd:
                    time.sleep(2)
                    print self.cmd_str(subcmd)
                    if os.system(self.cmd_str(subcmd)):
                       continue
                #1、使用netsh wlan show interfaces查看是否连接
                time.sleep(3)
                for min in range(0,3):
                    status=os.popen(self.cmd_str("netsh wlan show interfaces"))
                    ra0status=status.read()
                    if re.search(kargs["ssid"],ra0status):
                        status.close()
                        return True
                    time.sleep(3)
                    status.close()
            except Exception,e:
                print str(e)
        return False
    def windows_cfg_wireless(self,**kargs):
        cmd="netsh wlan set profileparameter "
        #参数配置文件名
        try:
            if 'name' in kargs.keys() and kargs['name'] != "":
                cmd=cmd+"name=tenda_ganraoceshi "
            if 'intf' in kargs.keys():
                if not kargs['intf']:
                    kargs['intf'] = self.intf
                cmd=cmd+"interface=%s " %(kargs['intf'])
            if 'ssid' in kargs.keys() and kargs['ssid'] != "":
                cmd=cmd+"SSIDname=%s " %(kargs['ssid'])
            cmd = cmd + "ConnectionType=ESS autoSwitch=yes ConnectionMode=auto nonBroadcast=yes "
            if not "authmode" in kargs.keys() or kargs["authmode"][0] == "none":
                cmd = cmd + "authentication=open encryption=none"
            elif kargs["authmode"][0] in  "shared open":
                cmd = cmd + "authentication=%s encryption=WEP keyType=networkKey keyIndex=%s keyMaterial=%s " %(kargs["authmode"][0],kargs["authmode"][1],kargs["authmode"][2])
            elif kargs["authmode"][0] in  "wpapsk wpa2psk":
                cmd = cmd + "authentication=%s encryption=%s keyType=passphrase keyMaterial=%s " %(kargs["authmode"][0],kargs["authmode"][1],kargs["authmode"][2])
            print self.cmd_str(cmd)
            if not os.system(self.cmd_str(cmd)):
                time.sleep(2)
                return True
            return False
        except Exception,e:
            print str(e)
            return False
    #
    def send_cmd(self,dip='',funcname='',**kargs):
        host=(dip,6000)
        sendTocmd=funcname+" "
        for key,value in kargs.items():
            sendTocmd=sendTocmd+"%s=%s " %(key,value)
        for i in range(0,3):
            try:
                sk=socket(AF_INET,SOCK_STREAM)
                sk.connect(host)
                if sendTocmd:
                    sk.send(sendTocmd)
                recvdata=""
                print "send suc"
                # time.sleep(1)
                flag=0
                while True:
                    data=sk.recv(BUFFSIZE)
                    if data:
                        recvdata=recvdata+data
                        flag=1
                    else:
                        if flag == 1:
                            break
                if  recvdata.strip() == "Suc":
                    sk.close()
                    return True
            except Exception,e:
                print str(e)
        return False
    #执行cmd函数 如果服务器地址为空则本地执行 否则把命令发给服务器执行 flag =0 表示以os.system执行 否则以os.popen执行
    def cmd_str(self,cmd):
        if self.cmdExec:
            cmd="""%s \"%s\" """ %(self.cmdExec,cmd)
        return cmd
            
# r_code=tc.pingtest(dip="192.168.10.2",maxerr=10,maxsuc=5)
# r_code=pingtest(dip="192.168.10.2",maxerr=10,maxsuc=5)
# print r_code
class ks():
    def __init__(self,**kargs):
        brate=38400
        port="COM1"
        if kargs.has_key('brate'):
            brate=kargs['brate']
        if kargs.has_key('port'):
            port=kargs['port']
        self.serial = serial.Serial(port=port, baudrate=brate, bytesize=8, parity=serial.PARITY_NONE, stopbits=1, timeout=None, xonxoff=1, rtscts=0, writeTimeout=None, dsrdtr=None)
    def config_rssi(self,num):
        cmd=""
        self.serial.write(cmd)
    def sendcmd(self,cmd):
        cmd=cmd+"\n"
        # cmd=self.str2bin(cmd)
        self.serial.write(cmd)
        time.sleep(0.5)
    def read_cominfo(self):
        buffer=''
        while True:
            if self.serial.inWaiting():
                data=self.serial.read(1)
                buffer=buffer+data
            else:
                break
        return buffer
if __name__ == "__main__":
    kargs={"intf":"ra0"}
    s=ks()
    s.sendcmd("ifconfig")
    data=s.read_cominfo()
    print "data=",data
 

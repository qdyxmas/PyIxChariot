#!/usr/bin/python
#coding=utf-8
import requests
import time,io,sys,os,re
#坐标元素

#主要用于检测tag之间的信息
Session=requests.Session()
class kc:
    def __init__(self):
        # kargs={"user":"admin","pwd":"admin"}
        self.user="admin"
        self.pwd="admin"
        self.dip="192.168.0.1"
        self.session=Session
        self.sys_login()
    def sys_login(self):
        ret=self.session.get("http://%s" %(self.dip))
        if ret.url.find("main") != -1:
            print u"login suc"
            return True
    def config_wan(self,**kargs):
        if self.sys_login():
            url="http://192.168.0.1/goform/WanParameterSetting?0.10657474784897802"
            ret=self.session.post(url=url,data=kargs)
            if ret.status_code==200:
                return True
    def config_wireless(self,**kargs):
        if  self.sys_login():
            url="http://192.168.0.1/goform/WifiBasicSet"
            ret=self.session.post(url=url,data=kargs)
            if ret.status_code==200:
                return True
    def config_channel(self,**kargs):
        if  self.sys_login():
            url="http://192.168.0.1/goform/WifiRadioSet"
            ret=self.session.post(url=url,data=kargs)
            if ret.status_code==200:
                return True
    def config_apclient(self,**kargs):
        #http://192.168.0.1/goform/WifiExtraSet
        if  self.sys_login():
            url="http://192.168.0.1/goform/WifiExtraSet"
            ret=self.session.post(url=url,data=kargs)
            if ret.status_code==200:
                #请求重启DUT
                return config_reboot()
    def config_wisp(self,**kargs):
        pass
    def config_vpnclient(self,**kargs):
        if  self.sys_login():
            url="http://192.168.0.1/goform/SetPptpClientCfg"
            ret=self.session.post(url=url,data=kargs)
            if ret.status_code==200:
                return True
            else:
                return False
    def config_reboot(self):
        url="http://192.168.0.1/goform/WifiExtraSet"
if __name__ == "__main__":
    ac=AC18()
    #http://192.168.0.1/goform/WanParameterSetting?0.9382516425730241
    pppoe_dict={"wanType":"2","adslUser":"123","adslPwd":"123","vpnServer":"","vpnUser":"","vpnPwd":"","vpnWanType":"1","dnsAuto":"1","staticIp":"","mask":"","gateway":"", "dns1":"","dns2":"","module":"wan1", "downSpeedLimit":""}
    dhcp_dict={"wanType":"0","adslUser":"123","adslPwd":"123","vpnServer":"","vpnUser":"","vpnPwd":"","vpnWanType":"1","dnsAuto":"1","staticIp":"","mask":"","gateway":"", "dns1":"","dns2":"","module":"wan1", "downSpeedLimit":""}
    static_dict={"wanType":"1","adslUser":"123","adslPwd":"123","vpnServer":"","vpnUser":"","vpnPwd":"","vpnWanType":"1","dnsAuto":"1","staticIp":"192.168.100.100","mask":"255.255.255.0","gateway":"192.168.100.200", "dns1":"192.168.100.200","dns2":"","module":"wan1", "downSpeedLimit":""}
    #http://192.168.0.1/goform/SetPptpClientCfg
    pptp_dict={"clientEn":"1","clientType":"pptp","clientMppe":"0","clientMppeOp":"128","domain":"192.168.100.200","userName":"123","password":"123"}
    l2tp_dict={"clientEn":"1","clientType":"l2tp","clientMppe":"0","clientMppeOp":"128","domain":"192.168.100.200","userName":"123","password":"123"}
    vpn_dict={"clientEn":"0"}
    #无线加密配置security:none/wpapsk/wpa2psk/wpawpa2psk
    wifi_dict={"wrlEn":"1","wrlEn_5g":"1","security":"wpapsk","security_5g":"wpapsk","ssid":"Tenda_2B78D0","ssid_5g":"Tenda_2B78D0_5G","hideSsid":"0","hideSsid_5g":"0","wrlPwd":"12345678","wrlPwd_5g":"12345678"}
    #无线信道设置
    #http://192.168.0.1/goform/WifiRadioSet
    wifi_chan_dict={"adv_mode":"bgn","adv_channel":"1","adv_band":"40","adv_mode_5g":"ac","adv_channel_5g":"36","adv_band_5g":"80"}
    wisp_dict={"wl_mode":"wisp","ssid":"abcde","security":"wpapsk","wpapsk_type":"wpa","wpapsk_crypto":"aes","wpapsk_key":"12345678","wifi_chkHz":"0","mac":"","handset":"1"}
    ac.config_wan(**dhcp_dict)
    # ac.config_channel(**wifi_chan_dict)
    # ac.config_vpnclient(**vpn_dict)
<FRAMESET>
PyIxChariot模块主要用于通过调用IxChariot脚本测试DUT的吞吐量信息
1、测试时请保证该目录下有Script目录存放Throughput.scr/Throughputdown.scr
2、config目录下有无线配置文件
3、kt模块主要用于配置windows信息
4、kc模块主要通过requests配置DUT信息
5、km模块主要通过调用IxChariot
最后结果会存放到当前目录result目录下
注意:先要保证能够load ChariotExt能够正常加载(把IxChariot目录添加到环境变量PATH中)
test
│
├─testcases.py	#测试脚本
│
├─config	#无线接口配置文件
│      cfg.xml
│      ra0-tenda_ganraoceshi.xml
│
├─result	#结果保存文件目录
├─Script	#Ixchariot 脚本
│      Throughput.scr
│      Throughputdown.scr
</FRAMESET>

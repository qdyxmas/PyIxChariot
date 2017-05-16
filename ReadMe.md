PyIxChariot模块主要用于通过调用IxChariot脚本测试DUT的吞吐量信息<br />
1、测试时请保证该目录下有Script目录存放Throughput.scr/Throughputdown.scr <br />
2、config目录下有无线配置文件<br />
3、kt模块主要用于配置windows信息<br />
4、kc模块主要通过requests配置DUT信息<br />
5、km模块主要通过调用IxChariot<br />
最后结果会存放到当前目录result目录下<br />
注意:先要保证能够load ChariotExt能够正常加载(把IxChariot目录添加到环境变量PATH中)<br />
test<br />
│<br />
├─testcases.py	#测试脚本<br />
│<br />
├─config	#无线接口配置文件<br />
│      cfg.xml<br />
│      ra0-tenda_ganraoceshi.xml<br />
│<br />
├─result	#结果保存文件目录<br />
├─Script	#Ixchariot 脚本<br />
│      Throughput.scr<br />
│      Throughputdown.scr<br />

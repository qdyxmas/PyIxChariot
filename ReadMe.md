# PyIxChariot

> 模块主要用于通过调用Ixia Chariot脚本测试DUT的吞吐量信息

## 介绍

````text
1. 测试时请保证该目录下有Script目录存放Throughput.scr/Throughputdown.scr
2. config目录下有无线配置文件
3. kt模块主要负责配置windows信息
4. kc模块主要负责requests库通过cgi接口配置路由器DUT配置
5. km模块主要负责调用IxChariot

执行完成后，结果存放到当前目录result目录下
````
> 注意:先要保证能够load ChariotExt能够正常加载, 需把IxChariot目录添加到环境变量PATH中。

### 项目结构

````text
test
|
|--config	      # 无线接口配置文件
|  |---cfg.xml
│  |---ra0-ganraoceshi.xml
|--Script	      # Ixchariot吞吐量脚本
│  |---Throughput.scr
│  |---Throughputdown.scr
|--result	      # 结果保存文件目录
|--kc.py          # 配置DUT设备
|--km.py          # 调用Ixia Chariot
|--kt.py          # 配置Windows
|--testcases.py	  # 测试脚本
|
````

## 环境

### 运行环境

Windows系统PC安装IxChariot6.7；6.7版本的IxChariot软件只支持Python2.7 32bit版本，调用此版本IxChariot软件的扩展库。

### 语言环境

> python2.7 32bit

依赖：
````text
requests==2.27.1
````
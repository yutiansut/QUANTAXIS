# QUANTAXIS 安装说明

## 安装须知

QUANTAXIS 使用到了一些3.6以上才支持的新语法,因此只支持3.6以上的python版本

* 在安装python时,请务必选择[add to path]选项
* 如果需要实盘交易,一般推荐安装32位的python, 因为对接需要的tradex.dll需要32位python
* 推荐使用anaconda来安装python,会自动安装ipython,jupyter,numpy等常用包
* Linux下无所谓32/64版本,实盘只能用windows,但是QUANTAXIS支持linux

QUANTAXIS的运行依赖以下环境:

1. 64位的电脑(64位系统)
2. 64位的MongoDB(32位的mongo只支持最大2G的数据存储,如果需要存分钟线数据,是不够的)
3. Python3.6+环境
4. Nodejs 7+ 环境 推荐Nodejs 8 速度更快

## 安装各个依赖项的步骤:

### MongoDB 
> Windows

- 下载地址 MongoDB 64位 3.4.7:[下载链接](https://www.mongodb.com/dr/fastdl.mongodb.org/win32/mongodb-win32-x86_64-2008plus-ssl-3.4.7-signed.msi)

- 可以使用迅雷下载加速

- 下载完毕以后双击MSI文件安装,一般会安装到C:\Program Files\MongoDB\Server\3.4\bin

* MongoDB需要一个data目录一个logo目录,一般我们会在D:中新建一个data目录
```powershell
# 打开Powershell(Win键+R 在运行中输入Powershell)
cd D:
md data
# 然后在data目录下 新建一个data目录用于存放mongo的数据,log目录用于存放log
cd data
md data
md log
# 到Mongo的程序文件夹下,使用命令
cd C:\Program Files\MongoDB\Server\3.4\bin
# 用mongod 命令安装
.\mongod.exe --dbpath  D:\data\data  --logpath D:\data\log\mongo.log --httpinterface --rest --serviceName 'MongoDB' --install
# 启动mongodb服务
net start MongoDB
```
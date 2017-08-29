# QUANTAXIS 安装说明
<!-- TOC -->

- [QUANTAXIS 安装说明](#quantaxis-安装说明)
    - [安装须知](#安装须知)
    - [安装各个依赖项的步骤:](#安装各个依赖项的步骤)
        - [git](#git)
        - [MongoDB](#mongodb)
        - [Nodejs](#nodejs)

<!-- /TOC -->
## 安装须知

QUANTAXIS 使用到了一些3.6以上才支持的新语法,因此只支持3.6以上的python版本

* 在安装python时,请务必选择[add to path]选项
* 如果需要实盘交易,一般推荐安装32位的python, 因为对接需要的tradex.dll需要32位python
* 推荐使用anaconda来安装python,会自动安装ipython,jupyter,numpy等常用包
* Linux下无所谓32/64版本,实盘只能用windows,但是QUANTAXIS支持linux

QUANTAXIS的运行依赖以下环境:

1. 64位的电脑(64位系统)
2. git 用于不断更新代码
2. 64位的MongoDB(32位的mongo只支持最大2G的数据存储,如果需要存分钟线数据,是不够的)
3. Python3.6+环境
4. Nodejs 7+ 环境 推荐Nodejs 8 速度更快

## 安装各个依赖项的步骤:
### git
>windows

百度搜索:git 下载--exe安装

>linux

自带 无需安装

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
> linux
- Ubuntu

```shell
#  添加源
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
# Ubuntu 12.04
echo "deb [ arch=amd64 ] http://repo.mongodb.org/apt/ubuntu precise/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
# Ubuntu 14.04
echo "deb [ arch=amd64 ] http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
# Ubuntu 16.04
echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
# 更新源
sudo apt-get update
# 安装MongoDB
sudo apt-get install -y mongodb-org
# 开启MongoDB服务
sudo service mongod start

```
### Nodejs
> windows

官网链接: https://nodejs.org/zh-cn/download/current/

直接下载exe 按要求安装即可 最新版本 8.2.1

> Linux

- Ubuntu

```shell
sudo apt-get install npm
sudo npm install n -g
sudo n latest
sudo npm install npm -g #更新npm
sudo npm install forever -g #安装一个全局的forever 用于之后启动
```

linux/mac下的nodejs有一个版本管理包 叫n 需要全局安装 -g

所以无论装了什么版本的nodejs  只需要npm install n -g  就行  
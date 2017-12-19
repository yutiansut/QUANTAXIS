# QUANTAXIS 的安装/部署/更新


<!-- TOC -->

- [QUANTAXIS 的安装/部署/更新](#quantaxis-的安装部署更新)
    - [部署问题:](#部署问题)
        - [ubuntu换源](#ubuntu换源)
        - [git](#git)
        - [MongoDB](#mongodb)
        - [Nodejs](#nodejs)
        - [python](#python)
        - [安装QUANTAXIS](#安装quantaxis)
    - [安装QUANATXIS_WebKit](#安装quanatxis_webkit)
    - [启动QUANTAXIS CLI 并进行数据的初始化存储](#启动quantaxis-cli-并进行数据的初始化存储)
    - [启动QUANTAXIS_Webkit来查看回测的结果](#启动quantaxis_webkit来查看回测的结果)
    - [更新QUANTAXIS](#更新quantaxis)

<!-- /TOC -->
## 部署问题:

- Windows/Linux(ubuntu) 已测试通过
- python3.6(开发环境) python2 回测框架不兼容(attention! 之后会逐步用更多高级语法)   [*] 如果需要交易,请下载32位的python3.6
- nodejs 需要安装>7的版本,来支持es6语法
- mongodb是必须要装的
- 强烈推荐mongodb的可视化库  robomongo 百度即可下载

一个简易demo(需要先安装并启动mongodb,python版本需要大于3)
### ubuntu换源
```
# 更换阿里云的源
echo "deb-src http://archive.ubuntu.com/ubuntu xenial main restricted #Added by software-properties
deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted
deb-src http://mirrors.aliyun.com/ubuntu/ xenial main restricted multiverse universe #Added by software-properties
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted multiverse universe #Added by software-properties
deb http://mirrors.aliyun.com/ubuntu/ xenial universe
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates universe
deb http://mirrors.aliyun.com/ubuntu/ xenial multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse #Added by software-properties
deb http://archive.canonical.com/ubuntu xenial partner
deb-src http://archive.canonical.com/ubuntu xenial partner
deb http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted multiverse universe #Added by software-properties
deb http://mirrors.aliyun.com/ubuntu/ xenial-security universe
deb http://mirrors.aliyun.com/ubuntu/ xenial-security multiverse " | sudo tee /etc/apt/sources.list.d/sources.list  

# 更新

sudo apt-get update
```

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

```
阿里云镜像版本
#  添加源
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
# Ubuntu 16.04
echo "deb http://mirrors.aliyun.com/mongodb/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list

# 更新
sudo apt-get update
# 安装MongoDB
sudo apt-get install -y mongodb-org
# 开启MongoDB服务
sudo service mongod start
```
```
注意:
如果遇到这个错误:
WARNING: The following packages cannot be authenticated!
  mongodb-org-shell mongodb-org-server mongodb-org-mongos mongodb-org-tools mongodb-org
E: There were unauthenticated packages and -y was used without --allow-unauthenticated

则需要
sudo apt-get install -y mongodb-org --allow-unauthenticated
```


### Nodejs
> windows

官网链接: https://nodejs.org/zh-cn/download/current/

直接下载exe 按要求安装即可 最新版本 8.2.1

> Linux

- Ubuntu

```shell
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo apt-get install npm
sudo npm install npm -g #更新npm
sudo npm install forever -g #安装一个全局的forever 用于之后启动
(如果forever 安装卡住/耗时过长 使用淘宝镜像CNPM)

(sudo npm install cnpm -g)
(sudo cnpm install forever -g)

```

linux/mac下的nodejs有一个版本管理包 叫n 需要全局安装 -g

所以无论装了什么版本的nodejs  只需要npm install n -g  就行  
### python

> Linux
```shell

#install python3.6 in linux
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install python3.6
wget https://bootstrap.pypa.io/get-pip.py
sudo -H python3.6 get-pip.py
```
> Windows

建议直接安装Anaconda包,记住在安装时 选择添加path不然后面会很麻烦

> python的一些需要编译的包的安装

安装TA-Lib(现在talib不是必须选项)
> Ubuntu
```
sudo apt-get update
sudo apt-get install python3.6-dev
# 装talib前要先装numpy
sudo python3.6 -m pip install numpy -i https://pypi.doubanio.com/simple
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzvf ta-lib-0.4.0-src.tar.gz
cd ta-lib
./configure --prefix=/usr
make
sudo make install
cd ..
sudo python3.6 -m pip install TA-Lib
# 安装剩余的依赖项
sudo python3.6 -m pip install -r requirements.txt -i https://pypi.doubanio.com/simple
sudo python3.6 -m pip install tushare==0.8.7 -i https://pypi.doubanio.com/simple
# 有一定几率在安装0.8.7的tushare时会出错
sudo python3.6 -m pip install git+https://github.com/yutiansut/tushare

```
> Windows
```

访问http://www.lfd.uci.edu/~gohlke/pythonlibs/  下载对应的whl安装包

(如 http://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib 下载TA_Lib‑0.4.10‑cp36‑cp36m‑win_amd64.whl)

pip install xxxxx(文件名).whl
```
### 安装QUANTAXIS
```
git clone https://github.com/yutiansut/quantaxis --depth 1
cd quantaxis .
pip install -r requirements.txt -i https://pypi.doubanio.com/simple
pip install tushare==0.8.7
(sudo) pip install -e . # 一定要用这种方法,python setup.py install方法无法解压 安装在本目录下的开发模式
# 注: 安装成本地开发模式以后,只需要git pull 就可以更新代码 无需重新 pip install -e .
```

```
[注意: tushare最新版本因为单方面直接复制了pytdx  所以导致和最新版本的pytdx不兼容 如有安装0.8.7版本以上的tushare 请降级使用]

典型表现是: 即使已经安装了pytdx 依然会报错找不到pytdx

*** 降级时需注意: 直接pip uninstall tushare以后 还要去删掉tushare安装目录下(一般是lib\site-packages\)的pytdx 再重新安装最新版本的pytdx ***

```
## 安装QUANATXIS_WebKit
```shell
cd QUANTAXIS_Webkit
(sudo) npm install forever -g

# 先去后台项目的文件夹安装
cd backend
(sudo) npm install
# 再去前端的文件夹安装
cd ..
cd web
(sudo) npm install
```
## 启动QUANTAXIS CLI 并进行数据的初始化存储

在命令行输入 quantaxis 进去quantaxis CLI
```
quantaxis> save all
quantaxis> save stock_block
quantaxis> save stock_info
```

随意新建一个目录:(不要跟QUANTAXIS文件夹在一个目录)

在命令行输入 quantaxis 进去quantaxis CLI


输入examples 在当前目录下生成一个示例策略

运行这个示例策略:

python  backtest.py

一般而言 日线4个组合的回测(一年)在14-17秒左右 5min级别4个组合的回测(一年)在3-4分钟左右


## 启动QUANTAXIS_Webkit来查看回测的结果


启动网络插件(nodejs 版本号需要大于6,最好是7)
```shell
cd QUANTAXIS_Webkit
# 先启动后台服务器  在3000端口
cd backend
(sudo) forever start bin/www
cd ..
# 再启动前端服务器  在8080端口
cd web
(sudo) npm run dev 或者 forever start build/dev-server.js
```

会自动启动localhost:8080网页端口,用账户名admin,密码admin登录
(注明: admin注册是在python的QUANTAXIS save all时候执行的)

另外 如果save all已经执行,依然登录不进去 点击插件状态 查看3000端口是否打开


登录后点击左上角 <模拟回测> 在模拟回测的选择界面的用户名搜索框输入回测的时候的用户名(默认是admin),回车

选择和你回测策略中名称一致的结果即可进入可视化界面
![开启web](http://osnhakmay.bkt.clouddn.com/quantaxis%E5%BC%80%E5%90%AF.gif)
![web操作](http://osnhakmay.bkt.clouddn.com/quantaxisweb.gif)
(web操作的图太大 github上无法显示, 可以点进链接查看)

## 更新QUANTAXIS

由于目前项目还在开发中,所以需要使用Git来更新项目:

点击右上角的Star和watch来持续跟踪项目进展~

常规更新:
```
cd QUANTAXIS
git pull
```

如果本地有进行更改,遇到更新失败:

(注意: 最好不要在本地修改该项目文件,如果需要做一些自定义功能,可以进fork[在项目的右上角])

```
git reset --hard origin/master
git pull
```

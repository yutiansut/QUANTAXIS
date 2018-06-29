# QUANTAXIS 的安装 Ubuntu篇
<!-- TOC -->

- [QUANTAXIS 的安装 Ubuntu篇](#quantaxis-的安装-ubuntu篇)
    - [1. 一键部署](#1-一键部署)
    - [2. 手动部署](#2-手动部署)
    - [3. 换源](#3-换源)
    - [4. 安装python](#4-安装python)
    - [5. 安装git](#5-安装git)
    - [6. 下载安装quantaxis](#6-下载安装quantaxis)
    - [7. 安装mongo](#7-安装mongo)

<!-- /TOC -->
##  1. 一键部署

```
wget https://raw.githubusercontent.com/QUANTAXIS/QUANTAXIS/master/config/ubuntu16.sh
sudo bash ./ubuntu16.sh
```

在脚本运行中,遇到输入的时候 一律选```yes```或者 ```y```


##  2. 手动部署

##  3. 换源
```
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
deb http://mirrors.aliyun.com/ubuntu/ xenial-security multiverse " | tee /etc/apt/sources.list.d/sources.list  


apt-get update
```
##  4. 安装python
```
apt install software-properties-common

add-apt-repository ppa:jonathonf/python-3.6
apt-get update

apt-get install python3.6-dev
wget https://bootstrap.pypa.io/get-pip.py

python3.6 get-pip.py
```

##  5. 安装git

```
apt-get install git
```

##  6. 下载安装quantaxis

```
cd ~
git clone https://github.com/yutiansut/quantaxis
cd ~/quantaxis
python3.6 -m pip install -r requirements.txt -i https://pypi.doubanio.com/simple
python3.6 -m pip install tushare
python3.6 -m pip install pytdx
python3.6 -m pip install -e .

```


##  7. 安装mongo
```
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
# Ubuntu 16.04
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list

# 更新
apt-get update
# 安装MongoDB
apt-get install -y mongodb-org --allow-unauthenticated

```

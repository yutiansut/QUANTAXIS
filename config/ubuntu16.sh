echo 'INSTALL_QUANTAXIS'

echo 'USING ALIYUN deb'

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

apt -y update


# apt-get install python3.6-dev
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-5.1.0-Linux-x86_64.sh
bash Anaconda3-5.1.0-Linux-x86_64.sh

source ~/.bashrc

#wget https://bootstrap.pypa.io/get-pip.py

#python get-pip.py


apt install  -y libxml2-dev libxslt-dev git gcc g++ software-properties-common

python -m pip install pip==9.0.1 # 降级
python -m pip install pyecharts_jupyter_installer
python -m pip install pillow -i https://pypi.doubanio.com/simple
python -m pip install tushare
python -m pip install pytdx --user
python -m pip install quantaxis



apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
# Ubuntu 16.04
#echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list
#echo "deb [ arch=amd64,arm64,ppc64el,s390x ] http://repo.mongodb.com/apt/ubuntu xenial/mongodb-enterprise/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-enterprise.list
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list


# Ubuntu 18.04
# echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list

# debian 8
# echo "deb http://repo.mongodb.org/apt/debian jessie/mongodb-org/4.0 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list

# debian 9
# echo "deb http://repo.mongodb.org/apt/debian stretch/mongodb-org/4.0 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list

# 更新
apt update -y 
# 安装MongoDB
apt install -y mongodb-org --allow-unauthenticated
cd /
mkdir data
cd data
mkdir data
mkdir log

# 开启MongoDB服务
service mongod start

apt install -y curl
# curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
# apt-get install -y nodejs
# apt-get install npm
# npm install npm -g #更新npm
# npm install forever -g #安装一个全局的forever 用于之后启动
# npm install cnpm -g




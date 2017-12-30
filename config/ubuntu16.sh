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

apt-get update

apt install software-properties-common

add-apt-repository ppa:jonathonf/python-3.6
apt-get update

apt-get install python3.6
apt-get install python3.6-dev
wget https://bootstrap.pypa.io/get-pip.py

python3.6 get-pip.py


apt-get install libxml2-dev libxslt-dev
apt-get install git
cd ~
git clone https://github.com/yutiansut/quantaxis
# add some permission for quantaxis
chmod -R 777 ./quantaxis
cd ~/quantaxis
python3.6 -m pip install pillow -i https://pypi.doubanio.com/simple
python3.6 -m pip install -r requirements.txt -i https://pypi.doubanio.com/simple
python3.6 -m pip install git+https://github.com/yutiansut/tushare
pip install -e .



apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
# Ubuntu 16.04
echo "deb http://mirrors.aliyun.com/mongodb/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list

# 更新
apt-get update
# 安装MongoDB
apt-get install -y mongodb-org --allow-unauthenticated
# 开启MongoDB服务
service mongod start


curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
apt-get install -y nodejs
apt-get install npm
npm install npm -g #更新npm
npm install forever -g #安装一个全局的forever 用于之后启动
npm install cnpm -g

cd ~/quantaxis/QUANTAXIS_Webkit/backend
npm install


cd ~/quantaxis/QUANTAXIS_Webkit/web
npm install



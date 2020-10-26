#!/bin/bash
cat > /etc/apt/sources.list <<EOF
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
EOF

export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get upgrade -y
apt-get autoremove -y
apt-get install wget curl nodejs npm nginx gcc git make tzdata fonts-wqy-microhei -y


wget https://downloads.sourceforge.net/project/ta-lib/ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz
tar xvf ta-lib-0.4.0-src.tar.gz
cd ta-lib
./configure --prefix=/usr
make
make install
cd ..
rm -rf ta-lib
rm ta-lib-0.4.0-src.tar.gz

mkdir /root/.conda
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod u+x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh -b -p /usr/local/conda
rm ./Miniconda3-latest-Linux-x86_64.sh
echo 'export PATH="/usr/local/conda/bin:$PATH"' >> ~/.bashrc
PATH="/usr/local/conda/bin:$PATH"

cat > ~/.condarc <<EOF
channels:
  - defaults
show_channel_urls: true
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
EOF

conda install -n base python==3.6.9 -y
conda update -n base conda -y
conda install -n base tensorflow-gpu==1.15.0 flask plotly cython pyinstaller simplejson lxml click six cryptography pylint pytest pypandoc gitpython requests aiohttp matplotlib pymysql pymongo gevent-websocket apscheduler protobuf retrying selenium scrapy attrs jinja2 future python-socketio SQLAlchemy appdirs ply keras-gpu py-xgboost-gpu jupyterlab pillow seaborn pandas==0.24.2 marshmallow==2.18.0 tzlocal=1.5.1 numpy scikit-learn -y


pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install TA-LIB pytdx pyecharts==0.5.11 aioch redis dag-factory jupyter_contrib_nbextensions cufflinks
pip install quantaxis-servicedetect quantaxis-pubsub qastrategy qifiaccount tqsdk tushare  quantaxis 


mkdir ~/.jupyter/
cat > ~/.jupyter/jupyter_notebook_config.py <<EOF
import os
from IPython.lib import passwd

c.NotebookApp.ip = '127.0.0.1'
c.NotebookApp.port = int(os.getenv('PORT', 8887))
c.NotebookApp.notebook_dir = '/home'
c.NotebookApp.open_browser = False
c.MultiKernelManager.default_kernel_name = 'python3'
c.NotebookApp.token = ''
c.NotebookApp.password = passwd(os.environ.get("QAPUBSUB_PWD", 'quantaxis'))
c.NotebookApp.allow_credentials = True
c.NotebookApp.allow_origin = '*'
c.NotebookApp.allow_remote_access = True
c.NotebookApp.tornado_settings = { 'headers': { 'Content-Security-Policy': "" }}
EOF

jupyter nbextension enable --py widgetsnbextension
jupyter serverextension enable --py jupyterlab
jupyter contrib nbextension install --system --skip-running-check
pyppeteer-install

mkdir ~/.config/matplotlib/ -p
cat > ~/.config/matplotlib/matplotlibrc <<EOF
font.family         : WenQuanYi Micro Hei, sans-serif 
font.sans-serif     : WenQuanYi Micro Hei, DejaVu Sans, Bitstream Vera Sans, Computer Modern Sans Serif, Lucida Grande, Verdana, Geneva, Lucid, Arial, Helvetica, Avant Garde, sans-serif
axes.unicode_minus  : False
EOF
ln -s /usr/share/fonts/truetype/wqy/wqy-microhei.ttc /usr/local/conda/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf/

cat > ~/.npmrc <<EOF
registry=https://registry.npm.taobao.org/
sass_binary_site=https://npm.taobao.org/mirrors/node-sass/
phantomjs_cdnurl=http://npm.taobao.org/mirrors/phantomjs
ELECTRON_MIRROR=https://npm.taobao.org/mirrors/electron/
CHROMEDRIVER_CDNURL=http://npm.taobao.org/mirrors/chromedriver
SELENIUM_CDNURL=http://npm.taobao.org/mirrorss/selenium
EOF

npm install -U -g npm
npm install -g phantomjs-prebuilt


chmod u+x /usr/local/conda/lib/python3.6/site-packages/QUANTAXIS/QAUtil/QASetting.py

cat > /etc/nginx/nginx.conf  <<EOF
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
        worker_connections 768;
}

http {  
        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;
        keepalive_timeout 65;
        types_hash_max_size 2048;
        client_max_body_size 10m;

        include /etc/nginx/mime.types;
        default_type application/octet-stream;

        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_prefer_server_ciphers on;

        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;

        gzip on;

        include /etc/nginx/conf.d/*.conf;
        include /etc/nginx/sites-enabled/*;
}
EOF

cat > /etc/nginx/passwd  <<EOF
quantaxis:\$apr1\$zKMmVZmz\$7nSJ4sDTYww0jSHPNlSPk1
EOF

cat > /etc/nginx/sites-enabled/default  <<EOF
server {
        listen 80 default_server;
        root /var/www/html;


        auth_basic "who are you";
        auth_basic_user_file /etc/nginx/passwd;

        index index.html index.htm;

        server_name _;
}
server {
        listen 8888;

        auth_basic "who are you";
        auth_basic_user_file /etc/nginx/passwd;

        location / {
            proxy_set_header Host \$host;
            proxy_set_header X-Real-Scheme \$scheme;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_pass  http://127.0.0.1:8887;

            proxy_http_version 1.1;
            proxy_set_header Upgrade \$http_upgrade;
            proxy_set_header Connection "upgrade";

            proxy_read_timeout 120s;
            proxy_next_upstream error;
        }
}
EOF

conda clean -a
apt-get clean -y
rm /tmp/* -rf
rm /root/.cache/ -rf
rm /root/.npm -rf


cat > /entrypoint.sh <<EOF
rm /var/www/html/* -rf
rm /var/www/html/.git* -rf
git clone https://gitee.com/yutiansut/QADESK_BASIC /var/www/html
nginx

PATH="/usr/local/conda/bin:\$PATH"
pip install -U quantaxis quantaxis-servicedetect quantaxis-pubsub qastrategy qifiaccount tqsdk tushare 
jupyter lab --allow-root
EOF
chmod u+x /entrypoint.sh



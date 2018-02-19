# QUANTAXIS 的安装 MAC篇

<!-- TOC -->

- [QUANTAXIS 的安装 MAC篇](#quantaxis-%E7%9A%84%E5%AE%89%E8%A3%85-mac%E7%AF%87)
    - [python](#python)
    - [QUANTAXIS](#quantaxis)
    - [MONGODB](#mongodb)
    - [NODEJS](#nodejs)
    - [QUANTAXIS_WEBKIT](#quantaxiswebkit)

<!-- /TOC -->
## python
```
brew install python3
```

## QUANTAXIS

```
git clone https://github.com/yutiansut/quantaxis --depth 1
cd quantaxis .
sudo python3.6 -m pip install -r requirements.txt -i https://pypi.doubanio.com/simple
sudo python3.6 -m pip install tushare
sudo python3.6 -m pip install pytdx

python3.6 -m pip install -e .
```


## MONGODB

安装mongodb:
```
brew update
brew install mongodb
```


创建数据库文件:
```
sudo mkdir -p /data/db
```

然后需要输入你的密码

启动mongodb
```
sudo mongod
```
继续输入你的密码


## NODEJS

```
brew install node

sudo npm install cnpm -g
sudo npm install forever -g
```

## QUANTAXIS_WEBKIT

```
cd QUANTAXIS_WEBKIT\web 
cnpm install

cd QUANTAXIS_WEBKIT\backend
cnpm install
```
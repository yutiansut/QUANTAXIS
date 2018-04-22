# QUANTAXIS 的安装 WIN篇
<!-- vscode-markdown-toc -->
* 1. [部署问题:](#:)
* 2. [下载PYTHON(可以跳过)](#PYTHON)
* 3. [安装(可以跳过)](#)
* 4. [下载git](#git)
* 5. [使用git下载QUANTAXIS](#gitQUANTAXIS)
* 6. [安装QUANTAXIS的依赖项](#QUANTAXIS)
* 7. [下载安装数据库](#-1)
* 8. [安装QUANTAXIS的web插件](#QUANTAXISweb)
* 9. [安装完成后 参见部署](#-1)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->
##  1. <a name=':'></a>部署问题:

- Windows/Linux(ubuntu) 已测试通过
- python3.6(开发环境) python2 回测框架不兼容(attention! 之后会逐步用更多高级语法)   [*] 如果需要交易,请下载32位的python3.6
- nodejs 需要安装>7的版本,来支持es6语法
- mongodb是必须要装的
- 强烈推荐mongodb的可视化库  robomongo 百度即可下载

一个简易demo(需要先安装并启动mongodb,python版本需要大于3)





##  2. <a name='PYTHON'></a>下载PYTHON(可以跳过)

QUANATXIS 支持的安装环境是python3以上 优先推荐3.6环境

在windows下,推荐使用ANACONDA集成环境来安装python[推荐Anaconda3-5.0.1-Windows-x86_64.exe]

(由于anaconda较大而官网的速度较慢,推荐去清华的anaconda镜像站下载)

[清华镜像ANACONDA链接](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/)

##  3. <a name=''></a>安装(可以跳过)

在安装ANACONDA的过程中,注意勾选```add to path```选项,将python的执行路径加入系统路径中

在安装完成后,可以使用```python -V```来验证是否成功

```bash
λ  python -V
Python 3.6.3 :: Anaconda, Inc.
```

##  4. <a name='git'></a>下载git

QUANTAXIS的代码托管在github,你需要经常用过```git pull```来更新代码,所以请勿直接在网站上下载zip压缩包

[git 下载地址](http://rj.baidu.com/soft/detail/40642.html)

同样,在安装的时候 选择```add to path```

##  5. <a name='gitQUANTAXIS'></a>使用git下载QUANTAXIS

打开命令行(推荐使用powershell) 选择你想要的目录 下载quantaxis


``` 
WIN键+R 在运行中输入 powershell 回车

cd C:\
git clone https://github.com/yutiansut/quantaxis --depth 1 
```

##  6. <a name='QUANTAXIS'></a>安装QUANTAXIS的依赖项

```
cd C:\quantaxis

python -m pip install -r requirements.txt -i https://pypi.doubanio.com/simple
python -m pip install tushare
python -m pip install pytdx
python -m pip install -e . 
```

完成以后 在命令行输入 ```quantaxis```即可进入QUANTAXIS的cli界面

```
λ  quantaxis
QUANTAXIS>> start QUANTAXIS
QUANTAXIS>> Selecting the Best Server IP of TDX
QUANTAXIS>> === The BEST SERVER ===
 stock_ip 115.238.90.165 future_ip 61.152.107.141
QUANTAXIS>> Welcome to QUANTAXIS, the Version is remake-version
QUANTAXIS>
```


##  7. <a name='-1'></a>下载安装数据库

QUANTAXIS使用MONGODB数据库作为数据存储,需要下载数据库

下载地址
[下载地址 MongoDB 64位 3.4.7](https://www.mongodb.com/dr/fastdl.mongodb.org/win32/mongodb-win32-x86_64-2008plus-ssl-3.4.7-signed.msi)

安装以后,需要在本地新建一个文件夹作为数据存储的文件夹,示例中,我们建在D盘

```
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


# 如果你下载了3.6版本以上的mongodb 则使用

.\mongod.exe --dbpath  D:\data\data  --logpath D:\data\log\mongo.log --serviceName 'MongoDB' --install
```

开启数据库服务

```
# 启动mongodb服务
net start MongoDB
```

##  8. <a name='QUANTAXISweb'></a>安装QUANTAXIS的web插件

QUANTAXIS使用了nodejs写了web部分的插件,所以需要下载nodejs

nodejs下载地址 [](https://nodejs.org/zh-cn/download/current/)

注意: 需要下载的是nodejs8的版本,切勿下载9版本的nodejs

安装时也需要```add to path ```

安装完成后,在命令行输入```node -v```来查看是否安装成功

```
λ  node -v
v8.9.3
```


```
npm install cnpm -g
cnpm install forever -g

cd C:\quantaxis\QUANTAXIS_WEBKIT\backend
cnpm install

cd C:\quantaxis\QUANTAXIS_WEBKIT\web
cnpm install

```


##  9. <a name='-1'></a>安装完成后 参见部署

[部署](install.md#%E5%90%AF%E5%8A%A8quantaxis-cli-%E5%B9%B6%E8%BF%9B%E8%A1%8C%E6%95%B0%E6%8D%AE%E7%9A%84%E5%88%9D%E5%A7%8B%E5%8C%96%E5%AD%98%E5%82%A8)

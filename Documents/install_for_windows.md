# QUANTAXIS 的安装 WIN篇
<!-- TOC -->

- [QUANTAXIS 的安装 WIN篇](#quantaxis-的安装-win篇)
    - [1. 部署问题:](#1-部署问题)
    - [2. 下载PYTHON(可以跳过)](#2-下载python可以跳过)
    - [3. 安装(可以跳过)](#3-安装可以跳过)
    - [4. 下载git[新手/以及不想自己改代码的注意 此段跳过]](#4-下载git新手以及不想自己改代码的注意-此段跳过)
    - [5. 使用git下载QUANTAXIS [新手/以及不想自己改代码的注意 此段跳过]](#5-使用git下载quantaxis-新手以及不想自己改代码的注意-此段跳过)
    - [6. 安装QUANTAXIS的依赖项 [新手/以及不想自己改代码的注意 此段跳过]](#6-安装quantaxis的依赖项-新手以及不想自己改代码的注意-此段跳过)
    - [7. 直接安装quantaxis [仅供新手/直接安装 使用]](#7-直接安装quantaxis-仅供新手直接安装-使用)
    - [8. 下载安装数据库](#8-下载安装数据库)
    - [9. 安装完成后 参见部署](#9-安装完成后-参见部署)

<!-- /TOC -->
##  1. 部署问题:

- Windows/Linux(ubuntu) 已测试通过
- python3.6(开发环境) python2 回测框架不兼容(attention! 之后会逐步用更多高级语法)   [*] 如果需要交易,请下载32位的python3.6
- nodejs 需要安装>7的版本,来支持es6语法
- mongodb是必须要装的
- 强烈推荐mongodb的可视化库  robomongo 百度即可下载

一个简易demo(需要先安装并启动mongodb,python版本需要大于3)





##  2. 下载PYTHON(可以跳过)

QUANATXIS 支持的安装环境是python3以上 优先推荐3.6环境

在windows下,推荐使用ANACONDA集成环境来安装python[推荐Anaconda3-5.0.1-Windows-x86_64.exe]

(由于anaconda较大而官网的速度较慢,推荐去清华的anaconda镜像站下载)

[清华镜像ANACONDA链接](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/)


anaconda安装的时候 注意:

敲黑板! 一定都要选上, 不然需要自己手动配置path, 如果不是很了解path的童靴一定要都选上

![](http://pic.yutiansut.com/anaconda_install_win.png)

##  3. 安装(可以跳过)

在安装ANACONDA的过程中,注意勾选```add to path```选项,将python的执行路径加入系统路径中

在安装完成后,可以使用```python -V```来验证是否成功

```bash
λ  python -V
Python 3.6.3 :: Anaconda, Inc.
```

##  4. 下载git[新手/以及不想自己改代码的注意 此段跳过]

QUANTAXIS的代码托管在github,你需要经常用过```git pull```来更新代码,所以请勿直接在网站上下载zip压缩包

[git 下载地址](https://pc.qq.com/search.html#!keyword=git)

同样,在安装的时候 选择```add to path```

![](http://pic.yutiansut.com/git1.png)
![](http://pic.yutiansut.com/git2.png)
![](http://pic.yutiansut.com/git3.png)
![](http://pic.yutiansut.com/git4.png)
![](http://pic.yutiansut.com/git5.png)

##  5. 使用git下载QUANTAXIS [新手/以及不想自己改代码的注意 此段跳过]

打开命令行(推荐使用powershell) 选择你想要的目录 下载quantaxis


``` 
WIN键+R 在运行中输入 powershell 回车

cd C:\
git clone https://github.com/yutiansut/quantaxis --depth 1 
```

##  6. 安装QUANTAXIS的依赖项 [新手/以及不想自己改代码的注意 此段跳过]

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
QUANTAXIS>
```


## 7. 直接安装quantaxis [仅供新手/直接安装 使用]


```
pip install quantaxis
```


安装时可能会遇到几个问题:


1. twisted, lxml 等需要编译:  出现VC14 required等字样:


    ```
    解决方法:

    单独去https://www.lfd.uci.edu/~gohlke/pythonlibs/ 找到你所缺少的包, 下载到本地 pip install 安装

    ```

2. pip no 'main' 问题:


    ```
    解决方法:

    pip10 的不兼容升级, 使用pip install pip==9.0.1 降级后安装
    ```

3. 缺少包 例如 jupyter-echarts-installer

    ```
    解决方法:

    单独安装 pip install xxxx
    ```






##  8. 下载安装数据库

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


##  9. 安装完成后 参见部署

[部署](install.md#%E5%90%AF%E5%8A%A8quantaxis-cli-%E5%B9%B6%E8%BF%9B%E8%A1%8C%E6%95%B0%E6%8D%AE%E7%9A%84%E5%88%9D%E5%A7%8B%E5%8C%96%E5%AD%98%E5%82%A8)

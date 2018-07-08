# QUANTAXIS的小白级别教程

<!-- TOC -->

- [QUANTAXIS的小白级别教程](#quantaxis的小白级别教程)
    - [了解windows命令行:](#了解windows命令行)
    - [安装python](#安装python)
    - [安装quantaxis](#安装quantaxis)
    - [安装数据库](#安装数据库)
    - [使用jupyter调试你的代码](#使用jupyter调试你的代码)
    - [自动更新数据](#自动更新数据)

<!-- /TOC -->


此篇安装纯粹写给刚学习编程/对python不熟悉/金融系的童靴们, 如果已经有一定的基础,知道怎么倒腾系统,路径,命令行,git等操作,可以直接去[install](install.md)

作者本来也是金融系出身,代码这些属于自己摸索,清楚一路上的艰难,所以我们一切从最简单的说起:


1. quantaxis 是一个开源的python库, 你可以调用和引入(import), 可以自己修改里面的源代码并提交给[官方组织](htttps://github.com/quantaxis)来贡献自己的力量和想法
2. quantaxis依赖Python3环境,所以你需要先安装一个python环境
3. quantaxis在本地存储了日线/分钟线/财务等等数据, 因此你需要准备一个数据库
4. quantaxis解决的是一个基础的框架性问题, 可以帮你自动更新/清洗数据, 给你回测/分析提供支持, 但是quantaxis不是一个可以直接运行了就赚钱的东西... 因此你还是需要自己实现你的想法
5. quantaxis的使用和调试主要通过python的 ```jupyter notebook``` 你可以直接使用jupyter来调试你的代码
6. quantaxis 100% 纯开源,并不收费, 你可以放心使用.

在以上的一些基本概念了解以后, 我们进入正题:

## 了解windows命令行:

按住 win+R键, 调出```运行```窗口

输入powershell

或者cmd

即可进入命令行, 命令行是windows中运行程序/配置服务中必备的工具

![](http://pic.yutiansut.com/powershell.png)

## 安装python

我们推荐使用anaconda来安装python, anaconda是一个集成的python环境

(由于anaconda较大而官网的速度较慢,推荐去清华的anaconda镜像站下载)

[清华镜像ANACONDA链接](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/)


anaconda安装的时候 注意:

敲黑板! 一定都要选上, 不然需要自己手动配置path, 如果不是很了解path的童靴一定要都选上

![](http://pic.yutiansut.com/anaconda_install_win.png)

在安装ANACONDA的过程中,注意勾选```add to path```选项,将python的执行路径加入系统路径中

在安装完成后,可以使用```python -V```来验证是否成功

```bash
λ  python -V
Python 3.6.3 :: Anaconda, Inc.
```

## 安装quantaxis

打开命令行输入

```
pip install quantaxis -i https://pypi.doubanio.com/simple
```

在这个过程中, 你会遇到各种报错:

- 如果出现```ModuleNotFoundError``` 一般是这个模块还没有安装起来,
- 如果出现```VC14 required ``` 等字样,说明此包需要编译

遇到这种情况, 直接访问 [python winodws wheel](https://www.lfd.uci.edu/~gohlke/pythonlibs/)

在页面上按住 ```ctrl+f```键, 调出搜索框 ,搜索你需要的包 :

![](http://pic.yutiansut.com/QQ%E6%88%AA%E5%9B%BE20180708143617.png)

然后点击进入

![](http://pic.yutiansut.com/winwheel.png)

下载whl文件到本地, 使用命令行进入本地目录:

使用 pip install 安装这个文件

```
pip install 你下载的文件.whl
```

![](http://pic.yutiansut.com/pipwhl.png)


然后再继续 


```
pip install quantaxis -i https://pypi.doubanio.com/simple
```

直至成功


## 安装数据库


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




## 使用jupyter调试你的代码

1. 在命令行启动jupyter
![](http://pic.yutiansut.com/QQ%E6%88%AA%E5%9B%BE20180626231059.png)


2. 在产生的网页上新建一个notebook
![](http://pic.yutiansut.com/QQ%E5%9B%BE%E7%89%8720180626231143.png)

3. 在notebook中运行代码
![](http://pic.yutiansut.com/QQ%E5%9B%BE%E7%89%8720180626231307.png)


4. 保存notebook为可运行的python文件
![](http://pic.yutiansut.com/QQ%E5%9B%BE%E7%89%8720180626231353.png)


## 自动更新数据


我们使用计划任务来开启自动更新任务:


1. 打开控制面板-系统和安全-管理工具
![](http://pic.yutiansut.com/management.png)

2. 打开计划任务程序
![](http://pic.yutiansut.com/management2.png)

3. 在计划任务程序中,新建任务
![](http://pic.yutiansut.com/task1.png)

4. 创建QUANTAXIS_Update任务
![](http://pic.yutiansut.com/task2.png)

5. 选择运行时间/频率
![](http://pic.yutiansut.com/task3.png)

6. 选择执行的命令
![](http://pic.yutiansut.com/task4.png)

7. 配置完毕
![](http://pic.yutiansut.com/task5.png)
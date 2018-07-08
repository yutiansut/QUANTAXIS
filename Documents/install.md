# QUANTAXIS 的安装/部署/更新


<!-- TOC -->

- [QUANTAXIS 的安装/部署/更新](#quantaxis-的安装部署更新)
    - [部署问题:](#部署问题)
    - [安装](#安装)
    - [启动QUANTAXIS CLI 并进行数据的初始化存储](#启动quantaxis-cli-并进行数据的初始化存储)
    - [启动jupyter 来运行QUANTAXIS](#启动jupyter-来运行quantaxis)
        - [1.在命令行启动jupyter](#1在命令行启动jupyter)
        - [2.在产生的网页上新建一个notebook](#2在产生的网页上新建一个notebook)
        - [3.在notebook中运行代码](#3在notebook中运行代码)
        - [4.保存notebook为可运行的python文件](#4保存notebook为可运行的python文件)
    - [更新QUANTAXIS](#更新quantaxis)

<!-- /TOC -->
## 部署问题:

- Windows/Linux(ubuntu)/Mac 已测试通过
- python3.6(开发环境) python2 回测框架不兼容(attention! 之后会逐步用更多高级语法)   [*] 如果需要交易,请下载32位的python3.6
- mongodb是必须要装的
- 强烈推荐mongodb的可视化库  robomongo (百度即可下载,QQ群文件也有)

一个简易demo(需要先安装并启动mongodb,python版本需要大于3)


## 安装


- WINDOWS安装 参见 [windows](install_for_windows.md)

- Ubuntu安装 参见 [Ubuntu](install_for_ubuntu.md)

- MAC 安装 参见 [MAC](install_for_mac.md)

- 便捷版本 参见 [Portable-QA](https://github.com/QUANTAXIS/portable_QA)






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

## 启动jupyter 来运行QUANTAXIS

### 1.在命令行启动jupyter
![](http://pic.yutiansut.com/QQ%E6%88%AA%E5%9B%BE20180626231059.png)


### 2.在产生的网页上新建一个notebook
![](http://pic.yutiansut.com/QQ%E5%9B%BE%E7%89%8720180626231143.png)

### 3.在notebook中运行代码
![](http://pic.yutiansut.com/QQ%E5%9B%BE%E7%89%8720180626231307.png)


### 4.保存notebook为可运行的python文件
![](http://pic.yutiansut.com/QQ%E5%9B%BE%E7%89%8720180626231353.png)

参见 [userjupyter](usejupyter.md)

<!-- ## 启动QUANTAXIS_Webkit来查看回测的结果


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
![开启web](http://pic.yutiansut.com/quantaxis%E5%BC%80%E5%90%AF.gif)
![web操作](http://pic.yutiansut.com/quantaxisweb.gif)
(web操作的图太大 github上无法显示, 可以点进链接查看) -->

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


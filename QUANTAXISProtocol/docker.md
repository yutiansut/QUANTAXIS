# 快速使用Docker建立QUANTAXIS执行环境

<!-- TOC -->

- [快速使用Docker建立QUANTAXIS执行环境](#快速使用docker建立quantaxis执行环境)
    - [QUANTAXIS的镜像](#quantaxis的镜像)
    - [获取安装了QUANTAIS的镜像](#获取安装了quantais的镜像)
        - [执行以下命令获取镜像(4选1)](#执行以下命令获取镜像4选1)
        - [下载镜像后执行(4选一)](#下载镜像后执行4选一)
        - [在docker容器中执行以下命令](#在docker容器中执行以下命令)
        - [在浏览器中打开以下链接](#在浏览器中打开以下链接)
    - [从头安装QUANTAXIS](#从头安装quantaxis)

<!-- /TOC -->


## QUANTAXIS的镜像

QUANTAXIS官方维护了3个镜像:

1. DOCKER网站下的 ```yutiansut/quantaxis``` 以及国内的加速版本 ```registry.docker-cn.com/yutiansut/quantaxis```

2. 阿里云DOCKER= 杭州镜像仓库的 ```registry.cn-hangzhou.aliyuncs.com/quantaxis/quantaxis ```

3. 阿里云DOCKER= 上海镜像仓库的 ```registry.cn-shanghai.aliyuncs.com/quantaxis/quantaxis``` 


其中 杭州的镜像是包括了```node_modules```,以及市场日线数据的镜像  比较大 适合只想一次性部署的同学们

阿里云上海仓库,DOCKER官网的镜像是同一份docker,包含了所有必需的程序 但是没有存储数据

|              | yutiansut/quantaxis | 上海阿里云DOCKER仓库 | 杭州阿里云DOCKER仓库    |
| ------------ | ------------------- | ------------- | ---------------- |
| 地址           | 国外(可以加速)            | 上海            | 杭州               |
| 系统           | Ubuntu16.04         | Ubuntu16.04   | Ubuntu16.04      |
| python       | python3.6           | python 3.6    | python3.6        |
| mongo        | mongo 3.4 社区版       | mongo 3.4 社区版 | mongo3.4 社区版     |
|              | nodejs 8.2.1        | nodejs 8.2.1  | nodejs 8.2.1     |
| QUANTAXIS 目录 | ~/QUANTAXIS         | ~/QUANTAXIS   | ~/root/quantaxis |
| forever      | 有                   | 有             | 有                |
| web部分的依赖项    | 未安装                 | 未安装           | 已安装              |
|              | 未存储                 | 未存储           | 已存储(每日更新)        |
|              |                     |               |                  |








## 获取安装了QUANTAIS的镜像

首先，到[docker网站](https://www.docker.com/)下载相应的版本，并创建账号（注意：登录docker账号才能下载镜像）

(如果国外网站下载速度过慢,windows版本的docker安装文件群共享有)


### 执行以下命令获取镜像(4选1)


```shell
docker pull yutiansut/quantaxis

# 国内镜像加速
docker pull registry.docker-cn.com/yutiansut/quantaxis

# 国内阿里云镜像

### 杭州阿里云镜像
docker pull registry.cn-hangzhou.aliyuncs.com/quantaxis/quantaxis  
# 5G大礼包 包括完整的ubuntu/nodejs/python3.6/mongodb/quantaxis环境 已保存部分数据 开箱即用
# 会持续更新数据

### 上海阿里云镜像
docker pull registry.cn-shanghai.aliyuncs.com/quantaxis/quantaxis  
# 包括完整的ubuntu/nodejs/python3.6/mongodb/quantaxis环境 无数据版本 开箱后需要存储
# Ubuntu 16.04 64位 纯净版
# nodejs 8.2.1

# python3.6 python3.6-dev
# quantaxis 最新版本

# mongodb community server 3.4 版本
```


![执行时的命令行](http://osnhakmay.bkt.clouddn.com/QQ%E6%88%AA%E5%9B%BE20171213102629.png)


### 下载镜像后执行(4选一)

```
# 选择你下载的镜像
docker run -it -p 8080:8080 -p 3000:3000 yutiansut/quantaxis bash

docker run -it -p 8080:8080 -p 3000:3000 registry.docker-cn.com/yutiansut/quantaxis bash

docker run -it -p 8080:8080 -p 3000:3000 registry.cn-hangzhou.aliyuncs.com/quantaxis/quantaxis

docker run -it -p 8080:8080 -p 3000:3000 registry.cn-shanghai.aliyuncs.com/quantaxis/quantaxis
```


### 在docker容器中执行以下命令
```
tmux #建议使用tmux来管理多个窗口，与 Tmux 类似的软件还有 screen、dvtm、splitvt、byobu 等

# 启动 mongodb    
cd root
nohup sh ./startmongodb.sh &


# 使用tmux开启新窗口 (Ctrl-b c)

# 启动
cd root
./startwebkit.sh


# WEBKIT 也可以用forever来打开

```

### 在浏览器中打开以下链接
```angular2html
http://localhost:8080
```

## 从头安装QUANTAXIS

可以从一个干净的ubuntu镜像上开始安装，获取ubuntu镜像
```angular2html
docker pull library/ubuntu
docker run -it library/ubuntu bash
```
然后按照[QUANTAXIS 安装说明](install.md)进行安装

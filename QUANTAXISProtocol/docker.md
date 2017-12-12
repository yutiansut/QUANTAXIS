# 快速使用Docker建立QUANTAXIS执行环境

<!-- TOC -->
- [快速使用Docker建立QUANTAXIS执行环境](#快速使用Docker建立QUANTAXIS执行环境)
    - [获取安装了QUANTAXIS的镜像](#获取安装了QUANTAXIS的镜像)
    - [从头安装QUANTAXIS](#从头安装QUANTAXIS)

<!-- TOC -->

## 获取安装了QUANTAIS的镜像

首先，到[docker网站](https://www.docker.com/)下载相应的版本，并创建账号（注意：登录docker账号才能下载镜像）

执行以下命令获取镜像
```shell
docker pull duanrb/quantaxis

# 国内镜像加速
docker pull registry.docker-cn.com/duanrb/quantaxis

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


下载镜像后执行
```
# 选择你下载的镜像
docker run -it -p 8080:8080 -p 3000:3000 yutiansut/quantaxis bash

docker run -it -p 8080:8080 -p 3000:3000 registry.cn-hangzhou.aliyuncs.com/quantaxis/quantaxis

docker run -it -p 8080:8080 -p 3000:3000 registry.cn-shanghai.aliyuncs.com/quantaxis/quantaxis
```

然后在docker容器中执行以下命令
```
tmux #建议使用tmux来管理多个窗口，与 Tmux 类似的软件还有 screen、dvtm、splitvt、byobu 等

# 启动 mongodb    
cd
./startmongodb.sh

# 使用tmux开启新窗口 (Ctrl-b c)

# 启动
cd
./startwebkit.sh

```

在浏览器中打开以下链接
```angular2html
http://localhost:8080
```
 
## 从头安装QUANTAXIS

可以从一个干净的ubuntu镜像上开始安装，获取ubuntu镜像
```angular2html
docker pull ubuntu
```
然后按照[QUANTAXIS 安装说明](install.md)进行安装

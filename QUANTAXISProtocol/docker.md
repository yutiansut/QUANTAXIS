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
```

下载镜像后执行
```
docker run -it -p 8080:8080 -p 3000:3000 duanrb/quantaxis bash
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
然后按照[QUANTAXIS 安装说明](Setup.md)进行安装
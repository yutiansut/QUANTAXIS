# 使用Docker建立QUANTAXIS执行环境

<!-- vscode-markdown-toc -->
* 1. [QUANTAXIS的镜像](#QUANTAXIS)
* 2. [1.获取QUANTAIS镜像](#QUANTAIS)
	* 2.1. [1.1 执行以下命令获取镜像(2选1)](#)
	* 2.2. [1.2 运行镜像(2选1)](#-1)
	* 2.3. [1.3 在docker中执行命令(启动服务)](#docker)
	* 2.4. [在浏览器中打开以下链接](#-1)
	* 2.5. [其他注意选项](#-1)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

##  1. <a name='QUANTAXIS'></a>QUANTAXIS的镜像

QUANTAXIS官方维护了2个镜像:


境外版本:

1. DOCKER网站下的 ```yutiansut/quantaxis``` 以及国内的加速版本 ```registry.docker-cn.com/yutiansut/quantaxis```

境内版本/(享受阿里云内网加速):

2. 阿里云DOCKER= 上海镜像仓库的 ```registry.cn-shanghai.aliyuncs.com/yutiansut/quantaxis``` 


其中 杭州的镜像是包括了```node_modules```,以及市场日线数据的镜像  比较大 适合只想一次性部署的同学们

阿里云上海仓库,DOCKER官网的镜像是同一份docker,包含了所有必需的程序 但是没有存储数据

|                 |     海外仓库           | 上海阿里云DOCKER仓库   | 
| --------------- | ------------------- | --------------- | 
| 描述              | 网速不好的轻量纯净版本         | 网速不好的轻量纯净版本     | 
| 地址              | 国外(可以加速)            | 上海              | 
| 系统              | Ubuntu16.04         | Ubuntu16.04     | 
| python入口名       | python3.6           | python          |
| mongo           | mongo 3.4 社区版       | 暂无   | 
| nodejs          | nodejs 8.2.1        | nodejs 8.9.3   | 
| sshserver       | 内置                  | 暂无              |
| QUANTAXIS 目录    | /QUANTAXIS          | /home/quantaxis | 
| forever         | 有                   | 有               | 
| web部分的依赖项       | 未安装                 | 已安装            | 
| 日线数据            | 未存储                 | 未存储             | 
| 版本号             | V+数字版本              | V+数字版本          | 
| JupyterNoteBook | 暂不支持                | 支持              | 



##  2. <a name='QUANTAIS'></a>1.获取QUANTAIS镜像

首先，到[docker网站](https://www.docker.com/)下载相应的版本，并创建账号（注意：登录docker账号才能下载镜像）

(如果国外网站下载速度过慢,windows版本的docker安装文件群共享有)


###  2.1. <a name=''></a>1.1 执行以下命令获取镜像(2选1)


```shell

# 海外镜像(境外用户)
docker pull yutiansut/quantaxis


# 上海阿里云镜像(国内用户)
docker pull registry.cn-shanghai.aliyuncs.com/yutiansut/quantaxis  

```


![执行时的命令行](http://pic.yutiansut.com/QQ%E6%88%AA%E5%9B%BE20171213102629.png)


###  2.2. <a name='-1'></a>1.2 运行镜像(2选1)

```
# 选择你下载的镜像
docker run -it -p 8080:8080 -p 3000:3000 yutiansut/quantaxis bash

# 带jupyter版本
docker run -it -e GRANT_SUDO=yes -p 8888:8888 -p 8080:8080 -p 3000:3000 registry.cn-shanghai.aliyuncs.com/yutiansut/quantaxis
```


###  2.3. <a name='docker'></a>1.3 在docker中执行命令(启动服务)
```

# 启动 mongodb    
cd /home/quantaxis/config && nohup sh ./run_backend.sh &


# 启动 WEBKIT
cd /home/quantaxis/QUANTAXIS_Webkit/backend && forever start ./bin/www

cd /home/quantaxis/QUANTAXIS_Webkit/web && forever start ./build/dev-server.js

# 启动jupyter
cd /home/quantaxis/config && nohup sh ./startjupyter.sh &

```

![启动命令](http://pic.yutiansut.com/QQ%E6%88%AA%E5%9B%BE20171213104144.png)



###  2.4. <a name='-1'></a>在浏览器中打开以下链接
```angular2html
http://localhost:8080
http://localhost:8888
```


###  2.5. <a name='-1'></a>其他注意选项

1. docker 是可以通过ssh 连接的 ``` /etc/init.d/ssh start ```
2. 多窗口 

首先需要运行一个docker

```
A:\quantaxis [master ≡]
λ  docker run -it -p 8080:8080 -p 3000:3000 registry.cn-shanghai.aliyuncs.com/yutiansut/quantaxis
root@f22b5357dc6e:/#

```
然后在别的命令行执行 ``` docker ps``` 查询正在运行的docker的container_id
```
A:\Users\yutia
λ  docker ps


CONTAINER ID        IMAGE                                                   COMMAND             CREATED             STATUS              PORTS                                            NAMES
f22b5357dc6e        registry.cn-shanghai.aliyuncs.com/yutiansut/quantaxis   "bash"              21 seconds ago      Up 20 seconds       0.0.0.0:3000->3000/tcp, 0.0.0.0:8080->8080/tcp   boring_panini

```
然后执行 ```docker exec -it  [CONTAINERID] /bin/bash``` 进入

```
A:\Users\yutia
λ  docker exec -it  f22b5357dc6e /bin/bash
root@f22b5357dc6e:/#

```


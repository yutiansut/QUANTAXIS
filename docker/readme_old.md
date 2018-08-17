# 使用Docker建立QUANTAXIS执行环境

<!-- TOC -->

- [使用Docker建立QUANTAXIS执行环境](#使用docker建立quantaxis执行环境)
    - [QUANTAXIS的镜像](#quantaxis的镜像)
    - [1.获取QUANTAIS镜像](#1获取quantais镜像)
        - [1.1 执行以下命令获取镜像(2选1)](#11-执行以下命令获取镜像2选1)
        - [1.2 运行镜像](#12-运行镜像)
        - [在浏览器中打开以下链接](#在浏览器中打开以下链接)
        - [其他注意选项](#其他注意选项)

<!-- /TOC -->


## QUANTAXIS的镜像

quantaxis/quantaxis

## 1.获取QUANTAIS镜像

首先，到[docker网站](https://www.docker.com/)下载相应的版本，并创建账号（注意：登录docker账号才能下载镜像）

(如果国外网站下载速度过慢,windows版本的docker安装文件群共享有)


### 1.1 执行以下命令获取镜像(2选1)


```shell

docker pull quantaxis/quantaxis


```


![执行时的命令行](http://pic.yutiansut.com/QQ%E6%88%AA%E5%9B%BE20171213102629.png)


### 1.2 运行镜像

```
docker run -it -e GRANT_SUDO=yes --user root -p 8080:8080 quantaxis/quantaxis bash

jupyter notebook --allow-root
(jupyter notebook 密码是 quantaxis)
```




### 在浏览器中打开以下链接
```angular2html

http://localhost:8888
```


### 其他注意选项

1. docker 是可以通过ssh 连接的 ``` /etc/init.d/ssh start ```
2. 多窗口 

首先需要运行一个docker

```
A:\quantaxis [master ≡]
λ  docker run -it -p 8080:8080 quantaxis/quantaxis bash
root@f22b5357dc6e:/#

```
然后在别的命令行执行 ``` docker ps``` 查询正在运行的docker的container_id
```
A:\Users\yutia
λ  docker ps


CONTAINER ID        IMAGE                                                   COMMAND             CREATED             STATUS              PORTS                                            NAMES
f22b5357dc6e        quantaxis   "bash"              21 seconds ago      Up 20 seconds      0.0.0.0:8888->8888/tcp   boring_panini

```
然后执行 ```docker exec -it  [CONTAINERID] /bin/bash``` 进入

```
A:\Users\yutia
λ  docker exec -it  f22b5357dc6e /bin/bash
root@f22b5357dc6e:/#

```



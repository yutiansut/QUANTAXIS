
# QUANTAXIS DOCKER


提纲挈领的讲 此段内容分为4部分

1. 安装docker

2. 配置qa-service的环境

3. 以上两步干完了你改干啥

4. 如果你还闲得慌想要深入学习下docker的话



## 1. 安装docker 

### ubuntu 一键脚本(仅限linux!!!!! 看清楚!!!!)

```
wget https://raw.githubusercontent.com/QUANTAXIS/QUANTAXIS/master/config/install_docker.sh
sudo bash install_docker.sh
```
### win/mac 安装

win/mac 下的docker  需要手动安装一个docker desktop

非常简单 去docker网站下载win/mac的docker_desktop 或者  文件较大, 我在群文件也共享了

ps: quantaxis强烈推荐不要使用win10以下的系统...(好吧忽略我)

> 注意在安装exe的时候 最后一步 关于在使用windows container的地方 一定不要勾选 !!!!!!


```
到此处 你应该已经装起来了一个docker 

然后我们往下看
```


## 2. 使用QA_SERVICE(配置qa-service的环境)


qaservice是一个帮你预装/预拉起好一切东西的一个docker environment  你需要理解的是 这个environment


你如果只是想使用(指的是 包括且不限于: 就想写个回测/ 就想实盘 / 就想看个可视化 / 这类) 的话, 只需要拉起这个qaservice环境即可, 你不需要不需要不需要学docker!! 注意 不需要会用docker!!!!



如果你需要二次开发=> 对我说的就是特别喜欢魔改别人代码的你  或者 你需要和你现有的功能组合的话 ==>  也不建议用docker, 建议在本地调试本地部署完毕以后, 再学习怎么制作docker镜像==> 实现你的二次开发/分发需求


你需要注意的是 qaenvironment是需要做一些预处理的


1/  我们需要创建两个docker volume (1个是qamg 用来装数据库的数据文件 1个是qacode 用来存你写的代码)

2/  在你对于docker volume的理解里 docker volume 就是在docker级别的可移动硬盘

3/  docker volume仅需要创建一次



4/  这个qaservice的environment  需要一个叫做docker-compose.yaml的文件

4.1/ 你不需要理解docker-compose.yaml文件里的内容, 你只需要知道 这个yaml 是关于这个环境配置的设置文件

4.2/ 你唯一需要做的就是 建一个文件夹(爱建在哪里建哪里) 下载这个docker-compose.yaml ==> 复制粘贴进去



以上都是对win/mac的小白用户说的, 如果你已经是一个linux用户, 我默认你是一个精通百度搜索的男人...


### linux下的qa-service使用

第一次使用

```
wget https://raw.githubusercontent.com/QUANTAXIS/QUANTAXIS/master/docker/qaservice_docker.sh
sudo bash qaservice_docker.sh
```

后续使用 ==> cd 到有docker-compose.yaml的文件夹

```
docker-compose up -d
```

### mac/windows下的qa-service使用

第一次使用

1. 打开你的命令行, 输入

```

docker volume create --name=qamg
docker volume create --name=qacode
```
2. 下载docker-compose.yaml (https://raw.githubusercontent.com/QUANTAXIS/QUANTAXIS/master/docker/qa-service/docker-compose.yaml)

如果你不知道咋下载 可以去qq群 群文件下载

3. 找到你心爱的文件夹, 把这个宝贵的yaml放进去, 并记住你的文件夹目录(比如D:/qa/)

4. 打开你的命令行继续输入

```
cd D:/qa  (此处就是你心爱的文件夹的目录)

docker-compose up
```

后续使用

```
cd D:/qa  (此处就是你心爱的文件夹的目录)

docker-compose pull (这里的意思是更新docker文件)

docker-compose up
```

![](https://data.yutiansut.com/dockerinstall.png)


## 3.怎么用docker?



你需要知道的是  quantaxis致力于帮你把配置环境这些脏活干完以后, 他实现了



==> 帮你直接开启你需要的服务

==> 你可以直接访问html界面来写回测/ 看回测/ 上实盘等

==> 如果你本地有python环境 你可以在本地写, 并使用qaservice帮你开启的环境(比如数据库环境/ 比如mq环境)





端口:

- 27017 mongodb
- 8888 jupyter
- 8010 quantaxis_webserver
- 81 quantaxis_community 社区版界面
- 61208 系统监控
- 15672 qa-eventmq


然后就可以开始你的量化之路了骚年!


你需要注意的事情是 

1. docker和本地环境是可以并存的 没有人说过(就算说了也肯定不是我说的) 有了本地python就不能有docker了

2. docker 的目的是方便你快速拉起 如果你真的很有兴趣把我辛辛苦苦写的18个quantaxis及相关模块都本地部署一遍我是非常欢迎的



## 4.后面内容为docker进阶部分(指的是 如果你看不懂且不愿意看 就不用看)


### 查看每天数据更新日志：

docker logs cron容器名  

日志只输出到容器前台，如果日志对你很重要，建议用专业的日志收集工具，从cron容器收集日志

### 查看服务状态
```
docker ps

docker stats

docker-compose top

docker-compose ps
```

### 停止/删除 QUANTAXIS 服务 （包括 QUANTAXIS，自动更新服务，数据库容器）：

!!! 注意 这两条真的超级管用!!!! 不信你可以试下

停止：  
```
docker stop $(docker ps -a -q)
```
删除：  
```
docker rm $(docker ps -a -q)
```

### 更新：

```
docker-compose pull
```  


### 数据库备份(备份到宿主机当前目录，文件名：dbbackup.tar)：

1. 停止服务  
```
docker-compose stop
```

2. 备份到当前目录
```
docker run  --rm -v qamg:/data/db \
-v $(pwd):/backup alpine \
tar zcvf /backup/dbbackup.tar /data/db
```

### 数据库还原（宿主机当前目录下必要有以前备份过的文件，文件名：dbbackup.tar）：
1. 停止服务  
```
docker-compose stop
```

2. 还原当前目录下的dbbackup.tar到mongod数据库  
```
docker run  --rm -v qamg:/data/db \
-v $(pwd):/backup alpine \
sh -c "cd /data/db \
&& rm -rf diagnostic.data \
&& rm -rf journal \
&& rm -rf configdb \
&& cd / \
&& tar xvf /backup/dbbackup.tar"
```

3. 重新启动服务
```
docker-compose up -d
```

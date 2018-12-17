docker images for QUANTAXIS: https://github.com/QUANTAXIS/QUANTAXIS

## 镜像说明：
qa-base: QA 基础镜像  
qa-cron: cron 镜像, 每天19:00自动更新数据(update_all.py)，如需更改计划任务，请自行制作py文件并更新Dockerfile  
qa-jupyter: jupyter lab 镜像，端口8888，没有登录密码，如需制定密码，请自行更改jupyter_notebook_config.py 文件  
qa-web: websocket 服务镜像，端口8010  
mgdb: mongodb 数据库镜像，端口27017  


## 第一次部署：
```
1. 为mongodb创建 docker volume
  docker volume create qamg

2. 启动 QUANTAXIS 服务 （包括 QUANTAXIS，自动更新服务，数据库, 重新打开docker程序后，所有服务会自动运行）
  docker-compose up -d
```

## 查看每天数据更新日志：
```
docker logs cron容器名

日志只输出到容器前台，如果日志对你很重要，建议用专业的日志收集工具，从cron容器收集日志
```

## 查看服务状态
```
docker ps

docker stats
```

## 停止/删除 QUANTAXIS 服务 （包括 QUANTAXIS，自动更新服务，数据库容器）：
```
停止：docker-compose stop

删除：docker-compose rm （只删除数据库容器，不会删除数据）
```

## 更新：
```
选项1: 先删除容器，再从dockerhub从新下载
docker-compose rm
docker rmi 容器名
docker-compose up -d


选项2: 进入容器内用 git pull 更新
1. docker exec -it 容器名 bash
2. run git pull in the /QUANTAXIS folder
```

## 数据库备份(备份到宿主机当前目录，文件名：dbbackup.tar)：
```
1. docker-compose stop

2.
docker run  --rm -v qamg:/data/db \
-v $(pwd):/backup alpine \
tar zcvf /backup/dbbackup.tar /data/db

3. docker-compose up -d
```

## 数据库还原（宿主机当前目录下必要有以前备份过的文件，文件名：dbbackup.tar）：
```
1. docker-compose stop

2.
docker run  --rm -v qamg:/data/db \
-v $(pwd):/backup alpine \
sh -c "cd /data/db \
&& rm -rf diagnostic.data \
&& rm -rf journal \
&& rm -rf configdb \
&& cd / \
&& tar xvf /backup/dbbackup.tar"

3. docker-compose up -d
```

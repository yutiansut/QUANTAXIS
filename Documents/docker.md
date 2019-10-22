# QUANTAXIS容器服务：
qa-jupyter: http://localhost:8888/lab  
qa-web：http://localhost:8010/  
mongo：mongodb  
qa-cron：数据更新容器，每周一到五，19：00自动更新数据  


## 安装docker：
各平台安装，云上部署，请参考[官网](https://docs.docker.com/install/#supported-platforms)  

Windows 7用户请安装 [Docker Toolbox](https://docs.docker.com/toolbox/overview/#ready-to-get-started)


## 第一次部署：
1. 下载 [docker-compose.yaml](https://raw.githubusercontent.com/QUANTAXIS/QUANTAXIS/master/docker/docker-compose.yaml)
2. 创建 docker volume  
  ```
  docker volume create qamg
  docker volume create qacode
  ```
3. 启动 QUANTAXIS 服务 （包括 QUANTAXIS-jupyter，自动更新服务，数据库，web，每次启动docker，所有服务都会自动启动）  
  ```
  docker-compose up -d
  ```

## 查看服务状态
```
docker ps

docker stats

docker-compose top

docker-compose ps
```

## 更新：
1. 删除容器和镜像  
```
docker-compose down --rmi all
```  
2. 重新下载并启动容器  
```
docker-compose up -d
```

## 数据库备份(备份到宿主机当前目录，文件名：dbbackup.tar)：

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

3. 重新启动服务
```
docker-compose up -d
```

## 数据库还原（宿主机当前目录下必要有以前备份过的文件，文件名：dbbackup.tar）：
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

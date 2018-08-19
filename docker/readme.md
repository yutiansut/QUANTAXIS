docker image for QUANTAXIS: https://github.com/QUANTAXIS/QUANTAXIS

## deployment:
1. start up 
```
docker-compose up
```
2. initialization  #TODO

```
  docker exec -it CONTAINERNAME base
  mkdir FOLDER
  cd FOLDER
  quantaxis
  save all
```

## stop/remove container:
```
1. docker-compose stop
2. docker-compose rm
```

## update:
```
1. rename the 'image' name for qa service in docker-compose
2. docker-compose up -d
```

## database backup:
```
1. docker-compose stop
2. ./data/db  为mongo数据文件
   ./notebooks 为 程序文件
```

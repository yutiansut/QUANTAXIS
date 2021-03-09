UI版镜像文件；

增加kite索引库检索目录，并创建本机python库与kite索引库检索目录的软连接，使kite不需要学习即可直接索引本地库函数；

本机编程输入词频学习记录需要持久化，新增加一个kite卷；

第一次启动前创建数据卷

docker volume create kite

docker volume create qamg

docker volume create qacode

修改期货股票两个update文件第一行解释器路径，替换为 #!/opt/conda/bin/python；

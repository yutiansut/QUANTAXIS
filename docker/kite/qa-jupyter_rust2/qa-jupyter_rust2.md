上层镜像用Kite Engine版镜像qa-base_rust2:1.0 ；若该镜像已上传DaoCloud，可改用 DaoCloud 地址；

安装jupyterlab-kite，jupyterlab-kite依赖tornado==6.1.0，同时会把jupyterlab升级为3.0.9或更新版。

安装jupyterlab官方汉化包jupyterlab_language_pack_zh_CN-0.0.1.dev0-py2.py3-none-any.whl

jupyterlab-kite依赖tornado==6.1.0会和web service依赖tornado==5.1.1冲突，有两个解决方案

方案一、kite版qacommunity-rust-go镜像启动UI容器，原版qacommunity-rust-go镜像启动WEB service容器，这有个问题，两个镜像的镜像层可能没办法互相复用节约磁盘空间了，一个镜像容量8GB左右；

方案二、在qa-jupyter_rust2镜像基础上分别build UI和WEB service镜像，UI镜像默认tornado==6.1.0，注释掉原dockerfile文件中tornado==5.1.1的安装语句，WEB service镜像则会安装tornado==5.1.1保证WEB service正常启动。这种情况两个镜像80%的镜像层应该可以复用，能节约6GB左右空间；

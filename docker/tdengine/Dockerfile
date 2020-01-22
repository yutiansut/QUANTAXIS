FROM centos:7.6.1810

RUN yum -y install wget unzip cmake make gcc gcc-c++ && mkdir /app
WORKDIR /app

RUN wget https://github.com/taosdata/TDengine/archive/master.zip && unzip master.zip && cd TDengine-master && mkdir build && cd build && cmake .. && cmake --build . && curl https://bootstrap.pypa.io/get-pip.py | python && pip install /app/TDengine-master/src/connector/python/python2/ && cp /app/TDengine-master/build/build/lib/libtaos.so /usr/lib64/ && ldconfig
WORKDIR /app/TDengine-master/build
EXPOSE 6035 6020
CMD ["./build/bin/taosd","-c","test/cfg"]

FROM ubuntu:16.04

ENV GOPATH=/root/go
ENV TZ=Asia/Shanghai
ENV DEBIAN_FRONTEND noninteractive
ENV PATH=${GOPATH}/bin:/usr/lib/go-1.11/bin:/usr/local/cmake/bin:${PATH}
ENV LD_LIBRARY_PATH=:${LD_LIBRARY_PATH}:/usr/local/cuda/lib64:${ARESDB_PATH}/lib
ENV GO111MODULE=on
RUN apt-get update --fix-missing \
&& apt-get install -y --reinstall software-properties-common \
&& add-apt-repository ppa:gophers/archive\
&& apt-get update \
&& apt-get install -y golang-1.11-go git npm wget
# install cmake 3.12
ARG CMAKE_VERSION=3.12.0
WORKDIR /tmp
RUN wget https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}-Linux-x86_64.tar.gz \
&& tar xzf cmake-${CMAKE_VERSION}-Linux-x86_64.tar.gz \
&& mv cmake-${CMAKE_VERSION}-Linux-x86_64 /usr/local/cmake \
&& cmake -version

WORKDIR /

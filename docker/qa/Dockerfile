FROM jupyter/base-notebook
MAINTAINER yutiansut 'yutiansut@qq.com'
MAINTAINER hexj 'hexj001@qq.com'
USER root
COPY source.list /etc/apt/sources.list
# 修改docker的时区
RUN sudo apt update -y \
    && apt install -y tzdata \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN sudo apt install -y python3-tk
# RUN pip install pip -U -i https://pypi.doubanio.com/simple
RUN pip install -i https://pypi.doubanio.com/simple --upgrade pip
USER jovyan
RUN pip install -r https://raw.githubusercontent.com/yutiansut/QUANTAXIS/master/requirements.txt -i https://pypi.doubanio.com/simple
RUN pip install tushare pytdx quantaxis

EXPOSE 8888

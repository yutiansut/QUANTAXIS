FROM python:3.8.6-buster

ENV TZ=Asia/Shanghai
ENV DEBIAN_FRONTEND noninteractive

COPY requirements.txt /requirements.txt
# for mirrors in China
COPY pip.conf /root/.pip/pip.conf
COPY source.list /etc/apt/sources.list
RUN  apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 3B4FE6ACC0B21F32 40976EAF437D05B5 && apt update
  
RUN  apt-get update \
  && apt-get install -y apt-utils locales --allow\
  && apt install gcc -y --allow\
  && locale-gen zh_CN.UTF-8 \
	&& localedef -i zh_CN -c -f UTF-8 -A /usr/share/locale/locale.alias zh_CN.UTF-8 \
	&& echo "LANG=zh_CN.UTF-8" > /etc/locale.conf \
	&& echo "zh_CN.UTF-8 UTF-8" >> /etc/locale.gen \
	&& echo "LC_ALL=zh_CN.UTF-8" >> /etc/environment

RUN \
  git clone https://gitee.com/yutiansut/QUANTAXIS \
  && cd QUANTAXIS \
  && pip install -r /QUANTAXIS/requirements.txt -i https://pypi.doubanio.com/simple \
  && pip install -r /requirements.txt -i https://pypi.doubanio.com/simple \
  && pip install quantaxis -U \
  && pip install quantaxis-servicedetect\
	&& apt-get clean -y --allow\
	&& apt-get autoclean -y --allow\
	&& apt-get autoremove -y --allow\
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

  ENV LANG zh_CN.UTF-8
  ENV LANGUAGE zh_CN.UTF-8
  ENV LC_ALL zh_CN.UTF-8

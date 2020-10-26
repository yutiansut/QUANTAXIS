FROM python:3.6.5-jessie

ENV TZ=Asia/Shanghai
ENV DEBIAN_FRONTEND noninteractive

COPY requirements.txt /requirements.txt
# for mirrors in China
COPY pip.conf /root/.pip/pip.conf
COPY source.list /etc/apt/sources.list

RUN  apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 3B4FE6ACC0B21F32 40976EAF437D05B5\
  && apt-get update \
  && apt-get install -y apt-utils locales --force-yes\
  && apt install gcc -y --force-yes\
  && locale-gen zh_CN.UTF-8 \
	&& localedef -i zh_CN -c -f UTF-8 -A /usr/share/locale/locale.alias zh_CN.UTF-8 \
	&& echo "LANG=zh_CN.UTF-8" > /etc/locale.conf \
	&& echo "zh_CN.UTF-8 UTF-8" >> /etc/locale.gen \
	&& echo "LC_ALL=zh_CN.UTF-8" >> /etc/environment

RUN \
  git clone https://gitee.com/yutiansut/QUANTAXIS \
  && cd QUANTAXIS \
  && pip install -r /QUANTAXIS/requirements.txt \
  && pip install -r /requirements.txt \
  && pip install quantaxis -U \
  && pip install quantaxis-servicedetect\
	&& apt-get clean -y --force-yes\
	&& apt-get autoclean -y --force-yes\
	&& apt-get autoremove -y --force-yes\
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

  ENV LANG zh_CN.UTF-8
  ENV LANGUAGE zh_CN.UTF-8
  ENV LC_ALL zh_CN.UTF-8

FROM python:3.7.4-stretch

ENV TZ=Asia/Shanghai
ENV DEBIAN_FRONTEND noninteractive

RUN \
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E40EBBA24FF2FC69 \
&& apt-get update \
&& apt-get install -y apt-utils locales --allow\
&& apt install gcc -y --allow\
&& locale-gen zh_CN.GB18030 \
&& pip install quantaxis-servicedetect \
&& localedef -i zh_CN -c -f UTF-8 -A /usr/share/locale/locale.alias zh_CN.GB18030 \
&& echo "LANG=zh_CN.GB18030" > /etc/locale.conf \
&& echo "zh_CN.GB18030 UTF-8" >> /etc/locale.gen \
&& echo "LC_ALL=zh_CN.GB18030" >> /etc/environment

ENV LANG zh_CN.GB18030
ENV LANGUAGE zh_CN.GB18030
ENV LC_ALL zh_CN.GB18030


RUN cd ~ \
&& git clone https://gitee.com/yutiansut/ctpbee \
&& chmod +x ~/ctpbee/examples/run.py \
&& cd ctpbee && pip install -e .


EXPOSE 5000

CMD ["python", "/root/ctpbee/examples/run.py"]


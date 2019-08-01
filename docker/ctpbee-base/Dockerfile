FROM python:3.7.4-stretch

ENV TZ=Asia/Shanghai
ENV DEBIAN_FRONTEND noninteractive

RUN \
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E40EBBA24FF2FC69 \
&& apt-get update \
&& apt-get install -y apt-utils locales --force-yes\
&& apt install gcc -y --force-yes\
&& locale-gen zh_CN.UTF-8 \
&& localedef -i zh_CN -c -f UTF-8 -A /usr/share/locale/locale.alias zh_CN.UTF-8 \
&& echo "LANG=zh_CN.UTF-8" > /etc/locale.conf \
&& echo "zh_CN.UTF-8 UTF-8" >> /etc/locale.gen \
&& echo "LC_ALL=zh_CN.UTF-8" >> /etc/environment

ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8


RUN cd ~ \
&& git clone https://github.com/yutiansut/ctpbee \
&& chmod +x ~/ctpbee/examples/run.py \
&& cd ctpbee && pip install -e .


EXPOSE 5000

CMD ["python", "~/ctpbee/examples/run.py"]


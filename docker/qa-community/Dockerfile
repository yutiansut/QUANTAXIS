FROM daocloud.io/quantaxis/qa-jupyter

ENV TZ=Asia/Shanghai
ENV DEBIAN_FRONTEND noninteractive

RUN cd ~ && git clone https://gitee.com/yutiansut/QADESK_BASIC && cd QADESK_BASIC \
&& pip install quantaxis-servicedetect \
&& pip install quantaxis-pubsub
COPY run-community.sh /root/
RUN chmod +x /usr/local/lib/python3.6/site-packages/QUANTAXIS/QAUtil/QASetting.py

RUN chmod +x /root/run-community.sh
CMD ["bash", "/root/run-community.sh"]

EXPOSE 80
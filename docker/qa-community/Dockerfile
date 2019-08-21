FROM daocloud.io/quantaxis/qa-jupyter

ENV TZ=Asia/Shanghai
ENV DEBIAN_FRONTEND noninteractive

RUN cd ~ && git clone https://gitee.com/yutiansut/QADESK_BASIC && cd QADESK_BASIC
COPY run-community.sh /root/
RUN chmod +x /QUANTAXIS/QUANTAXIS/QAUtil/QASetting.py

RUN chmod +x /root/run-community.sh
CMD ["bash", "/root/run-community.sh"]

EXPOSE 80
FROM daocloud.io/quantaxis/qa-jupyter

ENV TZ=Asia/Shanghai
ENV DEBIAN_FRONTEND noninteractive

RUN cd ~ && git clone https://gitee.com/yutiansut/QADESK_BASIC && cd QADESK_BASIC \
&& pip install quantaxis-servicedetect \
&& pip install quantaxis-pubsub \
&& pip install aioch \
&& pip install redis \
&& pip install dag-factory\
&& pip install quantaxis -U \
&& pip uninstall pytdx -y \
&& pip install pytdx

COPY run-community.sh /root/
RUN chmod +x /usr/local/lib/python3.6/site-packages/QUANTAXIS/QAUtil/QASetting.py \
&& echo "set nocp" >> ~/.vimrc && echo "set paste" >> ~/.vimrc &&  /bin/bash -c "source ~/.vimrc"


RUN chmod +x /root/run-community.sh
CMD ["bash", "/root/run-community.sh"]

EXPOSE 80

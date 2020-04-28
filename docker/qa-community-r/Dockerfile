FROM daocloud.io/quantaxis/qajupyter-r:latest
USER root
ENV TZ=Asia/Shanghai
ENV DEBIAN_FRONTEND noninteractive

RUN cd /root && git clone https://gitee.com/yutiansut/QADESK_BASIC && cd QADESK_BASIC

RUN apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 3B4FE6ACC0B21F32 40976EAF437D05B5\
  && apt update 

RUN apt install install -y gnupg2 \
&& pip install quantaxis-servicedetect \
&& pip install qifiaccount -U \
&& pip install QAStrategy -U \
&& pip install quantaxis-pubsub \
&& pip install qgrid \
&& pip install "dask[complete]"


# RUN pip install qgrid\
# && jupyter nbextension enable --py --sys-prefix qgrid\
# && jupyter nbextension enable --py --sys-prefix widgetsnbextension\
# && jupyter labextension install @jupyter-widgets/jupyterlab-manager\
# && jupyter labextension install qgrid


COPY run-community.sh /root/run-community.sh
RUN chmod +x /opt/conda/lib/python3.7/site-packages/QUANTAXIS/QAUtil/QASetting.py

RUN chmod +x /root/run-community.sh
CMD ["bash", "/root/run-community.sh"]

WORKDIR /home

EXPOSE 80
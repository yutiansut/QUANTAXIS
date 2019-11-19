FROM daocloud.io/quantaxis/qajupyter-go-r:latest
USER root
ENV TZ=Asia/Shanghai
ENV DEBIAN_FRONTEND noninteractive

RUN cd /root && git clone https://gitee.com/yutiansut/QADESK_BASIC && cd QADESK_BASIC \
&& pip install quantaxis-servicedetect \
&& pip install quantaxis-pubsub
COPY run-community.sh /root/run-community.sh
RUN chmod +x /opt/conda/lib/python3.7/site-packages/QUANTAXIS/QAUtil/QASetting.py\
    && mkdir -p /home/jovyan/.local/share/jupyter/kernels/gophernotes \
    && cd /home/jovyan/.local/share/jupyter/kernels/gophernotes \
    && pip install quantaxis -U\
    && pip uninstall pytdx -y \
    && pip install pytdx \
    && pip install qifiaccount -U \
    && pip install QAStrategy -U \
    && wget https://raw.githubusercontent.com/gopherdata/gophernotes/master/kernel/kernel.json \
    && wget https://raw.githubusercontent.com/gopherdata/gophernotes/master/kernel/logo-32x32.png \
    && wget https://raw.githubusercontent.com/gopherdata/gophernotes/master/kernel/logo-64x64.png 
    ## clean

RUN pip install qgrid\
&& jupyter nbextension enable --py --sys-prefix qgrid\
&& jupyter nbextension enable --py --sys-prefix widgetsnbextension\
&& jupyter labextension install @jupyter-widgets/jupyterlab-manager\
&& jupyter labextension install qgrid

RUN chmod +x /root/run-community.sh
CMD ["bash", "/root/run-community.sh"]

EXPOSE 80
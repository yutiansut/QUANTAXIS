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
&& pip install pytdx\
&& pip install qifiaccount -U \
&& pip install QAStrategy -U



RUN apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 3B4FE6ACC0B21F32  40976EAF437D05B5\
  && apt update
  
RUN apt install npm -y \
  && npm install n -g \
  && n stable
  
# RUN apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 3B4FE6ACC0B21F32  40976EAF437D05B5\
# && apt update \
# && apt install -y curl\
# && curl -sL https://deb.nodesource.com/setup_10.x | bash - \
# && apt install -y nodejs \
# && apt install npm \
# && npm install npm -g 

# RUN pip install qgrid\
# && jupyter nbextension enable --py --sys-prefix qgrid\
# && jupyter nbextension enable --py --sys-prefix widgetsnbextension\
# && jupyter labextension install @jupyter-widgets/jupyterlab-manager\
# && jupyter labextension install qgrid
RUN pip install qgrid && pip install "dask[complete]"

COPY run-community.sh /root/run-community.sh
RUN chmod +x /usr/local/lib/python3.6/site-packages/QUANTAXIS/QAUtil/QASetting.py \
&& echo "set nocp" >> ~/.vimrc && echo "set paste" >> ~/.vimrc &&  /bin/bash -c "source ~/.vimrc"


RUN chmod +x /root/run-community.sh
CMD ["bash", "/root/run-community.sh"]

EXPOSE 80

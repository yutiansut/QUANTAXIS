FROM daocloud.io/quantaxis/qabase:latest

COPY requirements.txt /requirements.txt
COPY entrypoint.sh /entrypoint.sh
COPY jupyter_notebook_config.py /root/.jupyter/

WORKDIR home

RUN wget https://downloads.sourceforge.net/project/ta-lib/ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz \
	&& tar xvf ta-lib-0.4.0-src.tar.gz \
	&& cd ta-lib \
	&& ./configure --prefix=/usr \
	&& make \
	&& make install \
  && cd .. \
	&& rm -rf ta-lib \
	&& rm ta-lib-0.4.0-src.tar.gz \
  && pip install -r /requirements.txt \
  && pip install quantaxis-servicedetect \
  && pip install prompt-toolkit \
  && pip install quantaxis -U \
  && pip uninstall pytdx -y \
  && pip install pytdx \
  && pip install pandarallel \
  && pip install apscheduler \
  && jupyter nbextension enable --py widgetsnbextension \
  && jupyter serverextension enable --py jupyterlab

RUN apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 3B4FE6ACC0B21F32 40976EAF437D05B5\
  && apt update

RUN apt install -y curl\
&& apt install npm -y \
&& npm install npm -g \
&& npm install n -g \
&& n stable


RUN pip install qgrid\
&& jupyter nbextension enable --py --sys-prefix qgrid\
&& jupyter nbextension enable --py --sys-prefix widgetsnbextension\
&& jupyter labextension install @jupyter-widgets/jupyterlab-manager\
&& jupyter labextension install qgrid


RUN pip install quantaxis-servicedetect \
&& pip install quantaxis-pubsub \
&& pip install aioch \
&& pip install redis \
&& pip install dag-factory \
&& chmod +x /entrypoint.sh
EXPOSE 8888 

COPY runpy.sh /root/
RUN chmod +x /usr/local/lib/python3.6/site-packages/QUANTAXIS/QAUtil/QASetting.py

RUN chmod +x /root/runpy.sh
CMD ["bash", "/root/runpy.sh"]

FROM jupyter/r-notebook

RUN Rscript -e "install.packages(c(\"devtools\", \"testthat\", \"roxygen2\"), repos = c(\"http://irkernel.github.io/\", \"http://cran.rstudio.com\"))"

RUN Rscript -e "library(\"devtools\")" -e "install_github(\"IRkernel/repr\")" -e "install_github(\"IRkernel/IRdisplay\")"

RUN pip install jupyter_kernel_test ndjson-testrunner

RUN unlink /opt/conda/lib/libstdc++.so.6
ENV TZ=Asia/Shanghai
ENV DEBIAN_FRONTEND noninteractive
USER root
COPY requirements.txt /requirements.txt
# for mirrors in China
# COPY pip.conf /root/.pip/pip.conf
COPY source.list /etc/apt/sources.list

RUN \ 
    apt-get update \
    # && apt-get install -y apt-utils locales\
    && apt-get install gcc -y --force-yes\
    && locale-gen zh_CN.UTF-8 \
    && localedef -i zh_CN -c -f UTF-8 -A /usr/share/locale/locale.alias zh_CN.UTF-8 \
    && echo "LANG=zh_CN.UTF-8" > /etc/locale.conf \
    && echo "zh_CN.UTF-8 UTF-8" >> /etc/locale.gen \
    && echo "LC_ALL=zh_CN.UTF-8" >> /etc/environment

RUN \
    cd ~ \
    && git clone https://github.com/QUANTAXIS/QUANTAXIS \
    && cd QUANTAXIS \
    && pip install -r requirements.txt \
    && pip install quantaxis-servicedetect \
    && pip install quantaxis -U \
    && apt-get clean -y --force-yes\
    && apt-get autoclean -y --force-yes\
    && apt-get autoremove -y --force-yes\
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8


RUN \
    cd ~ && mkdir .quantaxis && cd ~/.quantaxis && mkdir setting

COPY requirements.txt /requirements.txt
COPY entrypoint.sh /entrypoint.sh
COPY jupyter_notebook_config.py /root/.jupyter/

WORKDIR home

RUN cd ~ && wget https://downloads.sourceforge.net/project/ta-lib/ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz \
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
    && pip install rpy2 \
    && pip install quantaxis -U \
    && jupyter nbextension enable --py widgetsnbextension \
    && jupyter serverextension enable --py jupyterlab
RUN chmod +x /entrypoint.sh
COPY runpy.sh /root/
RUN chmod +x /opt/conda/lib/python3.7/site-packages/QUANTAXIS/QAUtil/QASetting.py && chmod +x /root/runpy.sh



EXPOSE 8888 
RUN Rscript -e "install.packages(c(\"lars\", \"glmnet\", \"rugarch\"), repos = c(\"http://irkernel.github.io/\", \"http://cran.rstudio.com\"))"
CMD ["bash", "/root/runpy.sh"]

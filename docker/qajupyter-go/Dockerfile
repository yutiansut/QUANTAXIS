FROM jdaocloud.io/quantaxis/qajupyter-r

RUN git clone https://github.com/gopherdata/gophernotes /go/src/github.com/gopherdata/gophernotes/
RUN set -x \
    # install python and dependencies
    && apk update \
    && apk --no-cache \
        --repository http://dl-4.alpinelinux.org/alpine/v3.7/community \
        --repository http://dl-4.alpinelinux.org/alpine/v3.7/main \
        --arch=x86_64 add \
        ca-certificates \
        su-exec \
        gcc \
        git \
        pkgconfig \
        zeromq-dev \
        musl-dev \
    ## install Go
    && apk --update-cache --allow-untrusted \
        --repository http://dl-4.alpinelinux.org/alpine/edge/community \
        --arch=x86_64 add \
        go \
    ## jupyter notebook
    && ln -s /usr/include/locale.h /usr/include/xlocale.h \
    ### fix pyzmq to v16.0.2 as that is what is distributed with py3-zmq
    ### pin down the tornado and ipykernel to compatible versions
    ## install gophernotes
    && GOPATH=/go go install github.com/gopherdata/gophernotes \
    && cp /go/bin/gophernotes /usr/local/bin/ \
    && mkdir -p ~/.local/share/jupyter/kernels/gophernotes \
    && cp -r /go/src/github.com/gopherdata/gophernotes/kernel/* ~/.local/share/jupyter/kernels/gophernotes \
    ## clean
    && rm -rf \
        /root/.[acpw]* \
        ipaexg00301* \
    && rm -rf /var/cache/apk/*

# Set GOPATH.
ENV GOPATH /go

EXPOSE 8888 
RUN Rscript -e "install.packages(c(\"lars\", \"glmnet\", \"rugarch\"), repos = c(\"http://irkernel.github.io/\", \"http://cran.rstudio.com\"))"
CMD ["bash", "/root/runpy.sh"]

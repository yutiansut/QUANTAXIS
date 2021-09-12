FROM qa-jupyter_rust2:1.0
#FROM daocloud.io/quantaxis/qa-jupyter:latest
USER root
ENV TZ=Asia/Shanghai
ENV DEBIAN_FRONTEND noninteractive

COPY daily_update /etc/cron.d/daily_update
COPY run-community.sh /root/
COPY runcelery.sh /root/
COPY wait_for_it.sh /root/

RUN cd /root && git clone https://gitee.com/yutiansut/qamazing_community && cd qamazing_community \
&& pip install quantaxis-servicedetect quantaxis-pubsub quantaxis quantaxis_webserver quantaxis_run qifimanager qavifiserver eventlet  -U -i https://pypi.doubanio.com/simple\
&& pip uninstall pytdx -y \
&& pip install pytdx -i https://pypi.doubanio.com/simple\
&& pip install qifiaccount QAStrategy -U -i https://pypi.doubanio.com/simple\
&& pip install qgrid -i https://pypi.doubanio.com/simple && pip install "dask[complete]" -i https://pypi.doubanio.com/simple


ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH \
    RUST_VERSION=1.55.0
    #https://cmake.org/files/v3.19/cmake-3.19.0-Linux-x86_64.tar.gz
ARG CMAKE_VERSION=3.19.0
WORKDIR /tmp
RUN wget https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}-Linux-x86_64.tar.gz \
&& tar xzf cmake-${CMAKE_VERSION}-Linux-x86_64.tar.gz \
&& mv cmake-${CMAKE_VERSION}-Linux-x86_64 /usr/local/cmake 
RUN apt-get install -y --allow-downgrades  zlib1g pkg-config  && apt-get install pkg-config libssl-dev -y

RUN set -eux; \
    dpkgArch="$(dpkg --print-architecture)"; \
    case "${dpkgArch##*-}" in \
        amd64) rustArch='x86_64-unknown-linux-gnu'; rustupSha256='49c96f3f74be82f4752b8bffcf81961dea5e6e94ce1ccba94435f12e871c3bdb' ;; \
        armhf) rustArch='armv7-unknown-linux-gnueabihf'; rustupSha256='5a2be2919319e8778698fa9998002d1ec720efe7cb4f6ee4affb006b5e73f1be' ;; \
        arm64) rustArch='aarch64-unknown-linux-gnu'; rustupSha256='d93ef6f91dab8299f46eef26a56c2d97c66271cea60bf004f2f088a86a697078' ;; \
        i386) rustArch='i686-unknown-linux-gnu'; rustupSha256='e3d0ae3cfce5c6941f74fed61ca83e53d4cd2deb431b906cbd0687f246efede4' ;; \
        *) echo >&2 "unsupported architecture: ${dpkgArch}"; exit 1 ;; \
    esac; \
    url="https://static.rust-lang.org/rustup/archive/1.22.1/${rustArch}/rustup-init"; \
    wget "$url"; \
    echo "${rustupSha256} *rustup-init" | sha256sum -c -; \
    chmod +x rustup-init; \
    ./rustup-init -y --no-modify-path --profile minimal --default-toolchain $RUST_VERSION --default-host ${rustArch}; \
    rm rustup-init; \
    chmod -R a+w $RUSTUP_HOME $CARGO_HOME; \
    rustup --version; \
    cargo --version; \
    rustc --version;


ENV GOPATH=/root/go
ENV PATH=${GOPATH}/bin:/usr/lib/go-1.15/bin:/usr/local/cmake/bin:${PATH}
ENV PKG_CONFIG_PATH = /usr/local/lib/pkgconfig
ENV LD_LIBRARY_PATH=:${LD_LIBRARY_PATH}:/usr/local/bin:/usr/local/lib
ENV GO111MODULE=on

COPY ./config  /root/.cargo/
COPY ./update_future.py  /root/QUANTAXIS/config/
RUN set -eux; \
    wget https://mirrors.ustc.edu.cn/golang/go1.15.6.linux-amd64.tar.gz;  \ 
    apt update --fix-missing; \
    apt install -y build-essential libzmq3-dev pkg-config cmake;\
    apt-get install -y cron --allow-unauthenticated;\
	chmod 0644 /etc/cron.d/daily_update ;\
	chmod +x /root/QUANTAXIS/config/update_future.py; \
	crontab /etc/cron.d/daily_update; \
    echo "set nocp" >> ~/.vimrc && echo "set paste" >> ~/.vimrc &&  /bin/bash -c "source ~/.vimrc";\
    chmod +x /root/run-community.sh;\
    chmod +x /root/runcelery.sh && chmod +x /root/wait_for_it.sh;\
    tar xvf go1.15.6.linux-amd64.tar.gz ;\
    chown -R root:root ./go ;\
    mv go /usr/lib/go-1.15;\
    go env -w GOPROXY=https://goproxy.cn;\    
    go get -u github.com/gopherdata/gophernotes;\
    cp /root/go/bin/gophernotes /usr/local/bin/ ;\
    mkdir -p /root/.local/share/jupyter/kernels/gophernotes ;\
    cd /root/.local/share/jupyter/kernels/gophernotes;\
    wget https://raw.fastgit.org/gopherdata/gophernotes/master/kernel/kernel.json ;\
    wget https://raw.fastgit.org/gopherdata/gophernotes/master/kernel/logo-32x32.png ;\
    wget https://raw.fastgit.org/gopherdata/gophernotes/master/kernel/logo-64x64.png ;\
    cargo install evcxr_jupyter --force; \
    evcxr_jupyter --install;
    ## clean
## run build for tensorflow 2
ENV GOPROXY=https://goproxy.io
RUN conda install --yes tensorflow 
 
RUN pip install tornado==5.1.1 -i https://pypi.doubanio.com/simple &&conda install --yes keras \
    && pip install QAStrategy quantaxis quantaxis_run qifiaccount -U -i https://pypi.doubanio.com/simple

RUN apt-get update && apt-get -y install libcurl4-openssl-dev  libssl-dev  build-essential net-tools htop\
    && cd /root/ && wget https://github.com/QUANTAXIS/QUANTAXIS/releases/download/1.10.2/portfoliohandler\
    && chmod +777 /root/portfoliohandler
RUN mkdir -p ~/.kite/libraries \
&& ln -s /opt/conda/lib/python3.8/site-packages ~/.kite/libraries
WORKDIR /root
EXPOSE 80 8010 8787 8020 8029 8018 8019 8028
CMD ["/bin/bash", "/root/run-community.sh"]
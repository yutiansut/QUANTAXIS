FROM daocloud.io/quantaxis/qa-jupyter:latest
USER root
ENV TZ=Asia/Shanghai
ENV DEBIAN_FRONTEND noninteractive

RUN cd /root && git clone https://github.com/yutiansut/qamazing_community && cd qamazing_community \
&& pip install quantaxis-servicedetect \
&& pip install quantaxis-pubsub


COPY run-community.sh /root/run-community.sh
RUN pip install quantaxis -U -i https://pypi.doubanio.com/simple\
    && pip uninstall pytdx -y \
    && pip install pytdx -i https://pypi.doubanio.com/simple\
    && pip install qifiaccount QAStrategy -U -i https://pypi.doubanio.com/simple
    ## clean

RUN pip install qgrid -i https://pypi.doubanio.com/simple && pip install "dask[complete]" -i https://pypi.doubanio.com/simple

ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH \
    RUST_VERSION=1.48.0
    
ARG CMAKE_VERSION=3.12.0
WORKDIR /tmp
RUN wget https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}-Linux-x86_64.tar.gz \
&& tar xzf cmake-${CMAKE_VERSION}-Linux-x86_64.tar.gz \
&& mv cmake-${CMAKE_VERSION}-Linux-x86_64 /usr/local/cmake 
RUN apt install zlib1g -y --allow-downgrades 
RUN apt-get install -y --allow-downgrades pkg-config  && apt-get install pkg-config libssl-dev -y




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


RUN set -eux; \
    apt-get update; \
    apt-get install -y build-essential libzmq3-dev pkg-config;

RUN set -eux; \
    cargo install evcxr_jupyter --force; \
    evcxr_jupyter --install;

RUN echo "set nocp" >> ~/.vimrc && echo "set paste" >> ~/.vimrc &&  /bin/bash -c "source ~/.vimrc"

RUN chmod +x /root/run-community.sh
CMD ["bash", "/root/run-community.sh"]

WORKDIR /home

EXPOSE 80
EXPOSE 8787

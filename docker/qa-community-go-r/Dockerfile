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

RUN pip install qgrid && pip install "dask[complete]"

ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH \
    RUST_VERSION=1.39.0

ARG CMAKE_VERSION=3.12.0
WORKDIR /tmp
RUN wget https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}-Linux-x86_64.tar.gz \
&& tar xzf cmake-${CMAKE_VERSION}-Linux-x86_64.tar.gz \
&& mv cmake-${CMAKE_VERSION}-Linux-x86_64 /usr/local/cmake \
&& cmake -version

RUN apt-get install -y --allow-downgrades pkg-config zlib1g=1:1.2.8.dfsg-2ubuntu4.1 && apt-get install pkg-config libssl-dev -y

RUN set -eux; \
    dpkgArch="$(dpkg --print-architecture)"; \
    case "${dpkgArch##*-}" in \
        amd64) rustArch='x86_64-unknown-linux-gnu'; rustupSha256='a46fe67199b7bcbbde2dcbc23ae08db6f29883e260e23899a88b9073effc9076' ;; \
        armhf) rustArch='armv7-unknown-linux-gnueabihf'; rustupSha256='6af5abbbae02e13a9acae29593ec58116ab0e3eb893fa0381991e8b0934caea1' ;; \
        arm64) rustArch='aarch64-unknown-linux-gnu'; rustupSha256='51862e576f064d859546cca5f3d32297092a850861e567327422e65b60877a1b' ;; \
        i386) rustArch='i686-unknown-linux-gnu'; rustupSha256='91456c3e6b2a3067914b3327f07bc182e2a27c44bff473263ba81174884182be' ;; \
        *) echo >&2 "unsupported architecture: ${dpkgArch}"; exit 1 ;; \
    esac; \
    url="https://static.rust-lang.org/rustup/archive/1.18.3/${rustArch}/rustup-init"; \
    wget "$url"; \
    echo "${rustupSha256} *rustup-init" | sha256sum -c -; \
    chmod +x rustup-init; \
    ./rustup-init -y --no-modify-path --default-toolchain $RUST_VERSION; \
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


RUN chmod +x /root/run-community.sh
CMD ["bash", "/root/run-community.sh"]

EXPOSE 80

FROM daocloud.io/quantaxis/qajupyter-r
ENV GOPATH=/root/go
ENV PATH=${GOPATH}/bin:/usr/lib/go-1.13/bin:/usr/local/cmake/bin:${PATH}
ENV PKG_CONFIG_PATH = /usr/local/lib/pkgconfig
ENV LD_LIBRARY_PATH=:${LD_LIBRARY_PATH}:/usr/local/bin:/usr/local/lib
ENV GO111MODULE=on
USER root
RUN wget https://studygolang.com/dl/golang/go1.13.1.linux-amd64.tar.gz && tar xvf go1.13.1.linux-amd64.tar.gz \
    && chown -R root:root ./go &&  mv go /usr/lib/go-1.13

ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH \
    RUST_VERSION=1.39.0

ARG CMAKE_VERSION=3.12.0
WORKDIR /tmp
RUN wget https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}-Linux-x86_64.tar.gz \
&& tar xzf cmake-${CMAKE_VERSION}-Linux-x86_64.tar.gz \
&& mv cmake-${CMAKE_VERSION}-Linux-x86_64 /usr/local/cmake \
&& apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 3B4FE6ACC0B21F32  40976EAF437D05B5\
&& cmake -version


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
    cargo install evcxr_jupyter; \
    evcxr_jupyter --install;
# install add-apt-repository
# RUN apt update --fix-missing \
# && apt install -y --reinstall software-properties-common \
# && add-apt-repository ppa:gophers/archive\
# && apt update
# RUN apt install -y golang-1.13-go git npm wget

# # install cmake 3.12
# # ARG CMAKE_VERSION=3.12.0
# # WORKDIR /tmp
# # RUN wget https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}-Linux-x86_64.tar.gz \
# # && tar xzf cmake-${CMAKE_VERSION}-Linux-x86_64.tar.gz \
# # && mv cmake-${CMAKE_VERSION}-Linux-x86_64 /usr/local/cmake \
# # && cmake -version
# WORKDIR /

RUN mkdir /root/go && cd /root/go \
    && apt install -y build-essential \
    && apt update && apt upgrade \
    && apt install -y pkg-config\
    && apt-get install -y libzmq3-dev\
    && pip install quantaxis -U \
    && pip uninstall pytdx -y \
    && pip install pytdx
    # && go get -insecure gonum.org/v1/plot/... \
    # && go get -insecure gonum.org/v1/gonum/... \
    # && go get github.com/kniren/gota/... \
    # && go get github.com/sajari/regression \
    # && go get github.com/sjwhitworth/golearn/... \
    # && go get -insecure go-hep.org/x/hep/csvutil/... \
    # && go get -insecure go-hep.org/x/hep/fit \
    # && go get -insecure go-hep.org/x/hep/hbook \
    # && go get github.com/montanaflynn/stats \
    # && go get github.com/boltdb/bolt \
    # && go get github.com/patrickmn/go-cache \
    # && go get github.com/chewxy/math32 \
    # && go get github.com/chewxy/hm \
    # && go get gorgonia.org/vecf64 \
    # && go get gorgonia.org/vecf32 \
    # && go get github.com/awalterschulze/gographviz \
    # && go get github.com/leesper/go_rng \
    # && go get github.com/pkg/errors \
    # && go get github.com/stretchr/testify/assert \

RUN go get -u github.com/gopherdata/gophernotes
RUN cp /root/go/bin/gophernotes /usr/local/bin/ \
    && mkdir -p /home/jovyan/.local/share/jupyter/kernels/gophernotes \
    && cd /home/jovyan/.local/share/jupyter/kernels/gophernotes \
    && wget https://raw.githubusercontent.com/gopherdata/gophernotes/master/kernel/kernel.json \
    && wget https://raw.githubusercontent.com/gopherdata/gophernotes/master/kernel/logo-32x32.png \
    && wget https://raw.githubusercontent.com/gopherdata/gophernotes/master/kernel/logo-64x64.png 
    ## clean
EXPOSE 8888 

CMD ["bash", "/root/runpy.sh"]

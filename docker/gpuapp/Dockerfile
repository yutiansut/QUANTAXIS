
ARG CUDA_VERSION=9.2
ARG CUDA_SHORT_VERSION=${CUDA_VERSION}
ARG LINUX_VERSION=ubuntu16.04
FROM nvidia/cuda:${CUDA_VERSION}-devel-${LINUX_VERSION}


ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/lib
# Needed for cudf.concat(), avoids "OSError: library nvvm not found"
ENV NUMBAPRO_NVVM=/usr/local/cuda/nvvm/lib64/libnvvm.so
ENV NUMBAPRO_LIBDEVICE=/usr/local/cuda/nvvm/libdevice/
ENV DEBIAN_FRONTEND=noninteractive

ARG CC=5
ARG CXX=5
RUN apt update -y --fix-missing && \
    apt upgrade -y && \
    apt install -y \
      git \
      gcc-${CC} \
      g++-${CXX} \
      libboost-all-dev \
      tzdata

# Install conda
ADD https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh /miniconda.sh
RUN sh /miniconda.sh -b -p /conda && /conda/bin/conda update -n base conda
ENV PATH=${PATH}:/conda/bin
# Enables "source activate conda"
SHELL ["/bin/bash", "-c"]

# Build cuDF conda env
ARG CUDA_SHORT_VERSION
ARG PYTHON_VERSION
ENV PYTHON_VERSION=$PYTHON_VERSION
ARG NUMBA_VERSION
ENV NUMBA_VERSION=$NUMBA_VERSION
ARG NUMPY_VERSION
ENV NUMPY_VERSION=$NUMPY_VERSION
ARG PANDAS_VERSION
ENV PANDAS_VERSION=$PANDAS_VERSION
ARG PYARROW_VERSION
ENV PYARROW_VERSION=$PYARROW_VERSION
ARG CYTHON_VERSION
ENV CYTHON_VERSION=$CYTHON_VERSION
ARG CMAKE_VERSION
ENV CMAKE_VERSION=$CMAKE_VERSION
ARG CUDF_REPO=https://github.com/rapidsai/cudf
ENV CUDF_REPO=$CUDF_REPO
ARG CUDF_BRANCH=master
ENV CUDF_BRANCH=$CUDF_BRANCH

# Add everything from the local build context
ADD . /cudf/

# Checks if local build context has the source, if not clone it then run a bash script to modify
# the environment file based on versions set in build args
RUN ls -la /cudf
RUN if [ -f /cudf/docker/package_versions.sh ]; \
    then /cudf/docker/package_versions.sh /cudf/conda/environments/cudf_dev_cuda${CUDA_SHORT_VERSION}.yml && \
         conda env create --name cudf --file /cudf/conda/environments/cudf_dev_cuda${CUDA_SHORT_VERSION}.yml ; \
    else rm -rf /cudf && \
         git clone --recurse-submodules -b ${CUDF_BRANCH} ${CUDF_REPO} /cudf && \
         /cudf/docker/package_versions.sh /cudf/conda/environments/cudf_dev_cuda${CUDA_SHORT_VERSION}.yml && \
         conda env create --name cudf --file /cudf/conda/environments/cudf_dev_cuda${CUDA_SHORT_VERSION}.yml ; \
    fi

# libcudf build/install
ENV CC=/usr/bin/gcc-${CC}
ENV CXX=/usr/bin/g++-${CXX}
RUN source activate cudf && \
    mkdir -p /cudf/cpp/build && \
    cd /cudf/cpp/build && \
    cmake .. -DCMAKE_INSTALL_PREFIX=${CONDA_PREFIX} && \
    make -j install

# cuDF build/install
RUN source activate cudf && \
    cd /cudf/python/cudf && \
    python setup.py build_ext --inplace && \
    python setup.py install

ENV GOPATH=/root/go
ENV UBER_GITHUB_DIR=$GOPATH/src/github.com/uber
ENV ARESDB_PATH=$UBER_GITHUB_DIR/aresdb
ENV PATH=${GOPATH}/bin:/usr/lib/go-1.11/bin:/usr/local/cmake/bin:${PATH}
ENV LD_LIBRARY_PATH=:${LD_LIBRARY_PATH}:/usr/local/cuda/lib64:${ARESDB_PATH}/lib
ENV GO111MODULE=on
# install add-apt-repository
RUN apt-get update --fix-missing \
&& apt-get install -y --reinstall software-properties-common \
&& add-apt-repository ppa:gophers/archive\
&& apt-get update \
&& apt-get install -y golang-1.11-go git npm wget

# install cmake 3.12
ARG CMAKE_VERSION=3.12.0
WORKDIR /tmp
RUN wget https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}-Linux-x86_64.tar.gz \
&& tar xzf cmake-${CMAKE_VERSION}-Linux-x86_64.tar.gz \
&& mv cmake-${CMAKE_VERSION}-Linux-x86_64 /usr/local/cmake \
&& cmake -version

WORKDIR /

# clone aresdb repo and set up GOPATH
RUN mkdir -p $UBER_GITHUB_DIR
WORKDIR $UBER_GITHUB_DIR
RUN git clone --recursive https://github.com/uber/aresdb.git \
&& ln -sf $UBER_GITHUB_DIR/aresdb $HOME/aresdb
WORKDIR aresdb
RUN cmake . \
&& make npm-install \
&& mkdir log \
&& make aresd -j
CMD ["make", "run_server",  ">> ./log/aresdb.log 2>&1","&"]
FROM daocloud.io/quantaxis/qajupyter-r
ENV GOPATH=/root/go
ENV PATH=${GOPATH}/bin:/usr/lib/go-1.13/bin:/usr/local/cmake/bin:${PATH}
ENV GO111MODULE=on
USER root
RUN wget https://studygolang.com/dl/golang/go1.13.1.linux-amd64.tar.gz && tar xvf go1.13.1.linux-amd64.tar.gz \
    && chown -R root:root ./go &&  mv go /usr/lib/go-1.13
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
RUN go install github.com/gopherdata/gophernotes \
    && cp /root/go/bin/gophernotes /usr/local/bin/ \
    && mkdir -p ~/.local/share/jupyter/kernels/gophernotes \
    && cp -r /root/go/src/github.com/gopherdata/gophernotes/kernel/* ~/.local/share/jupyter/kernels/gophernotes
    ## clean
EXPOSE 8888 
RUN Rscript -e "install.packages(c(\"lars\", \"glmnet\", \"rugarch\"), repos = c(\"http://irkernel.github.io/\", \"http://cran.rstudio.com\"))"
CMD ["bash", "/root/runpy.sh"]

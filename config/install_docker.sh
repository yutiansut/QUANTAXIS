echo 'install_docker'

curl -sSL https://get.daocloud.io/docker | sh

curl -L https://get.daocloud.io/docker/compose/releases/download/1.24.1/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose


echo 'finished install_docker'

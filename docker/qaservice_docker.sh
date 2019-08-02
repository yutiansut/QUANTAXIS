echo "QUANTAXIS_DOCKER_SERVICE"

mkdir quantaxis_docker && cd quantaxis_docker
wget https://raw.githubusercontent.com/QUANTAXIS/QUANTAXIS/master/docker/qa-service/docker-compose.yaml
docker volume create qamg
docker volume create qacode
# curl -sSL https://get.daocloud.io/daotools/set_mirror.sh | sh -s http://f1361db2.m.daocloud.io
docker-compose up -d

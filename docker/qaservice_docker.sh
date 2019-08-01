echo "QUANTAXIS_DOCKER_SERVICE"

mkdir quantaxis_docker && cd quantaxis_docker
wget https://github.com/QUANTAXIS/QUANTAXIS/blob/master/docker/qa-service/docker-compose.yaml
docker volume create qamg
docker volume create qacode
docker-compose up -d

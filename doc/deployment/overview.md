# QUANTAXIS 2.1.0 部署指南

**版本**: 2.1.0-alpha2
**更新日期**: 2025-10-25
**作者**: @yutiansut @quantaxis

---

## 📋 目录

1. [概述](#概述)
2. [Docker部署](#docker部署)
3. [Kubernetes部署](#kubernetes部署)
4. [Helm Charts部署](#helm-charts部署)
5. [多环境配置](#多环境配置)
6. [监控和日志](#监控和日志)
7. [备份和恢复](#备份和恢复)
8. [故障排查](#故障排查)
9. [最佳实践](#最佳实践)

---

## 概述

### 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                     QUANTAXIS 2.1.0                         │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Jupyter  │  │   Web    │  │ Monitor  │  │ Collector│   │
│  │  :8888   │  │  :8080   │  │  :61208  │  │  :8011   │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │              │             │          │
│       └─────────────┴──────────────┴─────────────┘          │
│                          │                                   │
│       ┌──────────────────┴──────────────────┐               │
│       │     QUANTAXIS Core Service          │               │
│       │       (资源管理器 + API)             │               │
│       └──────────────────┬──────────────────┘               │
│                          │                                   │
│  ┌────────────┬─────────┴────────┬──────────┬─────────┐    │
│  │            │                   │          │         │    │
│  ▼            ▼                   ▼          ▼         ▼    │
│ MongoDB   RabbitMQ             Redis    ClickHouse  Logs   │
│  :27017     :5672               :6379      :8123            │
└─────────────────────────────────────────────────────────────┘
```

### 组件说明

| 组件 | 版本 | 端口 | 说明 |
|------|------|------|------|
| **MongoDB** | 7.0 | 27017 | 主数据存储 |
| **RabbitMQ** | 3.13 | 5672, 15672 | 消息队列 |
| **Redis** | 7.0 | 6379 | 缓存服务 |
| **ClickHouse** | latest | 8123, 9000 | 分析数据库(可选) |
| **QUANTAXIS Core** | 2.1.0 | 8010 | 核心服务 |
| **Jupyter** | - | 8888 | 交互式开发 |
| **Web UI** | - | 8080 | Web界面 |
| **Monitor** | - | 61208 | 系统监控 |

---

## Docker部署

### 前置要求

- Docker >= 20.10
- Docker Compose >= 2.0
- 可用内存 >= 8GB
- 可用磁盘 >= 50GB

### 快速开始

#### 1. 基础部署 (核心服务)

```bash
# 克隆仓库
git clone https://github.com/QUANTAXIS/QUANTAXIS.git
cd QUANTAXIS/docker/qa-service-v2.1

# 复制环境变量配置
cp .env.example .env
# 编辑.env修改密码(生产环境必须!)

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

#### 2. 完整部署 (包含所有可选服务)

```bash
# 启动所有服务(包括ClickHouse和行情采集)
docker-compose --profile full up -d
```

#### 3. 指定profile部署

```bash
# 仅启动分析服务(包括ClickHouse)
docker-compose --profile analytics up -d

# 仅启动行情采集
docker-compose --profile market up -d
```

### 服务访问

| 服务 | 访问地址 | 默认账号 |
|------|---------|---------|
| Jupyter | http://localhost:8888 | - |
| Web UI | http://localhost:8080 | - |
| RabbitMQ管理 | http://localhost:15672 | admin/admin |
| 系统监控 | http://localhost:61208 | - |
| QUANTAXIS API | http://localhost:8010 | - |

### 常用命令

```bash
# 查看服务状态
docker-compose ps

# 查看资源使用
docker-compose stats

# 查看日志
docker-compose logs -f [service_name]

# 重启服务
docker-compose restart [service_name]

# 停止服务
docker-compose stop

# 完全清理(包括数据卷,危险!)
docker-compose down -v
```

### 数据持久化

数据存储在Docker volumes中:

```bash
# 查看所有volumes
docker volume ls | grep quantaxis

# 数据卷列表
# - quantaxis_mongodb_data    (MongoDB数据)
# - quantaxis_rabbitmq_data   (RabbitMQ数据)
# - quantaxis_redis_data      (Redis数据)
# - quantaxis_clickhouse_data (ClickHouse数据)
# - quantaxis_code            (用户代码)
# - quantaxis_logs            (日志)
```

### 数据备份

```bash
# 备份MongoDB
docker run --rm \
  -v quantaxis_mongodb_data:/data \
  -v $(pwd)/backup:/backup \
  alpine \
  tar czf /backup/mongodb_$(date +%Y%m%d).tar.gz /data

# 备份所有数据
./scripts/backup-all.sh
```

### 更新升级

```bash
# 拉取最新镜像
docker-compose pull

# 重新创建容器
docker-compose up -d --force-recreate
```

---

## Kubernetes部署

### 前置要求

- Kubernetes >= 1.24
- kubectl配置正确
- 至少3个工作节点
- 可用内存 >= 16GB (每节点)
- StorageClass可用

### 快速开始

#### 1. 创建命名空间和基础资源

```bash
cd QUANTAXIS/docker/k8s-deployment

# 1. 创建命名空间
kubectl apply -f 00-namespace.yaml

# 2. 创建ConfigMap和Secret
kubectl apply -f 01-configmap.yaml

# 修改密码 (生产环境必须!)
kubectl create secret generic mongodb-secret \
  --from-literal=MONGO_ROOT_USER=root \
  --from-literal=MONGO_ROOT_PASSWORD='your-strong-password' \
  --from-literal=MONGO_USER=quantaxis \
  --from-literal=MONGO_PASSWORD='quantaxis-password' \
  --namespace=quantaxis --dry-run=client -o yaml | kubectl apply -f -

# 3. 创建存储
kubectl apply -f 03-storage.yaml

# 4. 部署数据库服务
kubectl apply -f 10-mongodb.yaml
kubectl apply -f 11-rabbitmq.yaml
kubectl apply -f 12-redis.yaml

# 5. 等待数据库就绪
kubectl wait --for=condition=ready pod -l app=mongodb -n quantaxis --timeout=300s
kubectl wait --for=condition=ready pod -l app=rabbitmq -n quantaxis --timeout=300s

# 6. 部署QUANTAXIS核心服务
kubectl apply -f 50-quantaxis.yaml

# 7. 验证部署
kubectl get pods -n quantaxis
kubectl get svc -n quantaxis
```

#### 2. 查看部署状态

```bash
# 查看所有资源
kubectl get all -n quantaxis

# 查看Pod详情
kubectl describe pod -n quantaxis

# 查看日志
kubectl logs -f deployment/quantaxis -n quantaxis

# 进入容器
kubectl exec -it deployment/quantaxis -n quantaxis -- bash
```

#### 3. 访问服务

```bash
# 方式1: 端口转发
kubectl port-forward -n quantaxis service/quantaxis-service 8888:8888 8010:8010

# 方式2: 获取LoadBalancer外部IP
kubectl get svc quantaxis-service -n quantaxis

# 方式3: Ingress (需要先配置Ingress Controller)
kubectl apply -f 60-ingress.yaml
```

### 扩缩容

```bash
# 手动扩容
kubectl scale deployment quantaxis --replicas=5 -n quantaxis

# 查看HPA状态
kubectl get hpa -n quantaxis

# HPA自动扩缩容配置在50-quantaxis.yaml中
# 基于CPU和内存使用率自动调整副本数 (2-10)
```

### 滚动更新

```bash
# 更新镜像
kubectl set image deployment/quantaxis \
  quantaxis=quantaxis/quantaxis:2.1.0-alpha3 \
  -n quantaxis

# 查看更新状态
kubectl rollout status deployment/quantaxis -n quantaxis

# 回滚
kubectl rollout undo deployment/quantaxis -n quantaxis
```

### 资源监控

```bash
# 查看资源使用
kubectl top nodes
kubectl top pods -n quantaxis

# 查看事件
kubectl get events -n quantaxis --sort-by='.lastTimestamp'
```

---

## Helm Charts部署

### 安装Helm

```bash
# 下载Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# 验证安装
helm version
```

### 使用Helm部署

```bash
cd QUANTAXIS/docker/helm-charts

# 1. 添加仓库(如果有)
# helm repo add quantaxis https://quantaxis.github.io/charts
# helm repo update

# 2. 查看默认配置
helm show values ./quantaxis

# 3. 自定义配置
cat > custom-values.yaml << EOF
# MongoDB配置
mongodb:
  auth:
    rootPassword: "your-root-password"
    password: "your-quantaxis-password"
  persistence:
    size: 100Gi

# QUANTAXIS配置
quantaxis:
  replicas: 3
  resources:
    limits:
      cpu: 4
      memory: 8Gi
    requests:
      cpu: 1
      memory: 2Gi
EOF

# 4. 安装
helm install quantaxis ./quantaxis \
  --namespace quantaxis \
  --create-namespace \
  --values custom-values.yaml

# 5. 查看状态
helm status quantaxis -n quantaxis
helm list -n quantaxis

# 6. 升级
helm upgrade quantaxis ./quantaxis \
  --namespace quantaxis \
  --values custom-values.yaml

# 7. 卸载
helm uninstall quantaxis -n quantaxis
```

### Helm配置说明

主要配置项 (values.yaml):

```yaml
# 全局配置
global:
  storageClass: "quantaxis-ssd"
  imagePullPolicy: IfNotPresent

# MongoDB
mongodb:
  enabled: true
  auth:
    rootPassword: ""
    password: ""
  persistence:
    size: 50Gi

# RabbitMQ
rabbitmq:
  enabled: true
  auth:
    username: admin
    password: ""
  persistence:
    size: 10Gi

# Redis
redis:
  enabled: true
  auth:
    password: ""
  persistence:
    size: 10Gi

# ClickHouse (可选)
clickhouse:
  enabled: false
  persistence:
    size: 100Gi

# QUANTAXIS
quantaxis:
  replicas: 2
  image:
    repository: quantaxis/quantaxis
    tag: "2.1.0-alpha2"
  resources:
    limits:
      cpu: 4
      memory: 8Gi
    requests:
      cpu: 1
      memory: 2Gi

# Ingress
ingress:
  enabled: false
  className: "nginx"
  hosts:
    - host: quantaxis.example.com
      paths:
        - path: /
          pathType: Prefix
```

---

## 多环境配置

### 环境划分

| 环境 | 用途 | 副本数 | 资源配置 |
|------|------|--------|---------|
| **Development** | 开发测试 | 1 | 最小 |
| **Staging** | 预生产 | 2 | 中等 |
| **Production** | 生产 | 3+ | 完整 |

### Docker Compose多环境

#### 开发环境

```yaml
# docker-compose.dev.yaml
version: '3.8'
services:
  quantaxis:
    image: quantaxis/quantaxis:2.1.0-alpha2-dev
    environment:
      - DEPLOY_ENV=development
      - DEBUG=true
    resources:
      limits:
        cpus: '2'
        memory: 2G
```

```bash
# 启动开发环境
docker-compose \
  -f docker-compose.yaml \
  -f docker-compose.dev.yaml \
  up -d
```

#### 生产环境

```yaml
# docker-compose.prod.yaml
version: '3.8'
services:
  quantaxis:
    image: quantaxis/quantaxis:2.1.0-alpha2
    environment:
      - DEPLOY_ENV=production
      - DEBUG=false
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '4'
          memory: 8G
```

```bash
# 启动生产环境
docker-compose \
  -f docker-compose.yaml \
  -f docker-compose.prod.yaml \
  up -d
```

### Kubernetes多环境

使用Kustomize管理多环境:

```
k8s-deployment/
├── base/                 # 基础配置
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   └── service.yaml
├── overlays/
│   ├── dev/             # 开发环境
│   │   ├── kustomization.yaml
│   │   └── patches/
│   ├── staging/         # 预生产环境
│   │   ├── kustomization.yaml
│   │   └── patches/
│   └── prod/            # 生产环境
│       ├── kustomization.yaml
│       └── patches/
```

```bash
# 部署到不同环境
kubectl apply -k overlays/dev
kubectl apply -k overlays/staging
kubectl apply -k overlays/prod
```

---

## 监控和日志

### Prometheus监控

```bash
# 安装Prometheus Operator
helm repo add prometheus-community \
  https://prometheus-community.github.io/helm-charts
helm install prometheus \
  prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace

# QUANTAXIS已配置Prometheus注解
# 自动被Prometheus发现和抓取指标
```

### Grafana仪表板

```bash
# 访问Grafana
kubectl port-forward -n monitoring \
  svc/prometheus-grafana 3000:80

# 登录: admin / prom-operator
# 导入QUANTAXIS仪表板 (ID: TODO)
```

### ELK日志

```bash
# 安装Elastic Stack
helm repo add elastic https://helm.elastic.co
helm install elasticsearch elastic/elasticsearch -n logging --create-namespace
helm install kibana elastic/kibana -n logging
helm install filebeat elastic/filebeat -n logging

# QUANTAXIS日志会被Filebeat收集
```

### Loki日志

```bash
# 安装Loki Stack
helm repo add grafana https://grafana.github.io/helm-charts
helm install loki grafana/loki-stack -n logging --create-namespace

# 在Grafana中添加Loki数据源
```

---

## 备份和恢复

### MongoDB备份

#### Docker环境

```bash
# 备份
docker exec quantaxis-mongodb mongodump \
  --out=/backup/$(date +%Y%m%d)

# 复制备份文件到主机
docker cp quantaxis-mongodb:/backup ./mongodb-backup

# 恢复
docker exec quantaxis-mongodb mongorestore \
  /backup/20251025
```

#### Kubernetes环境

```bash
# 创建备份Job
kubectl apply -f backup-job.yaml

# 手动触发备份
kubectl create job --from=cronjob/mongodb-backup \
  mongodb-backup-manual -n quantaxis
```

### 持久化卷备份

```bash
# 使用Velero备份整个命名空间
velero backup create quantaxis-backup \
  --include-namespaces quantaxis

# 恢复
velero restore create --from-backup quantaxis-backup
```

---

## 故障排查

### 常见问题

#### 1. MongoDB连接失败

```bash
# 检查MongoDB状态
kubectl get pods -l app=mongodb -n quantaxis
kubectl logs -l app=mongodb -n quantaxis

# 测试连接
kubectl run -it --rm mongo-test \
  --image=mongo:7.0 \
  --restart=Never \
  --namespace=quantaxis \
  -- mongosh mongodb://mongodb-service:27017
```

#### 2. 内存不足

```bash
# 查看资源使用
kubectl top pods -n quantaxis

# 增加资源限制
kubectl edit deployment quantaxis -n quantaxis
# 修改resources.limits.memory
```

#### 3. Pod无法启动

```bash
# 查看Pod事件
kubectl describe pod <pod-name> -n quantaxis

# 查看日志
kubectl logs <pod-name> -n quantaxis --previous
```

### 调试工具

```bash
# 进入调试容器
kubectl debug -it <pod-name> -n quantaxis --image=busybox

# 网络调试
kubectl run -it --rm debug \
  --image=nicolaka/netshoot \
  --restart=Never \
  --namespace=quantaxis
```

---

## 最佳实践

### 安全

1. ✅ **修改所有默认密码**
2. ✅ **使用Secret管理敏感信息**
3. ✅ **启用RBAC权限控制**
4. ✅ **配置Network Policy**
5. ✅ **定期更新镜像和依赖**

### 性能

1. ✅ **合理配置资源请求和限制**
2. ✅ **使用SSD存储**
3. ✅ **启用持久化卷**
4. ✅ **配置亲和性和反亲和性**
5. ✅ **使用HPA自动扩缩容**

### 可靠性

1. ✅ **配置健康检查和就绪探针**
2. ✅ **设置Pod Disruption Budget**
3. ✅ **多副本部署**
4. ✅ **定期备份数据**
5. ✅ **配置监控和告警**

### 运维

1. ✅ **使用基础设施即代码 (IaC)**
2. ✅ **Git管理配置文件**
3. ✅ **自动化CI/CD流程**
4. ✅ **文档化运维流程**
5. ✅ **定期演练灾难恢复**

---

## 附录

### A. 端口清单

| 服务 | 端口 | 协议 | 说明 |
|------|------|------|------|
| MongoDB | 27017 | TCP | 数据库连接 |
| RabbitMQ | 5672 | TCP | AMQP协议 |
| RabbitMQ管理 | 15672 | HTTP | 管理界面 |
| RabbitMQ Prometheus | 15692 | HTTP | 指标 |
| Redis | 6379 | TCP | 缓存连接 |
| ClickHouse HTTP | 8123 | HTTP | HTTP接口 |
| ClickHouse Native | 9000 | TCP | Native接口 |
| QUANTAXIS API | 8010 | HTTP | API服务 |
| Jupyter | 8888 | HTTP | 开发环境 |
| Web UI | 8080 | HTTP | Web界面 |
| Monitor | 61208 | HTTP | 监控界面 |
| Market Collector | 8011 | HTTP | 行情采集 |

### B. 资源推荐配置

| 部署规模 | CPU | 内存 | 存储 | 节点数 |
|---------|-----|------|------|--------|
| **小型** | 8核 | 16GB | 100GB | 1 |
| **中型** | 16核 | 32GB | 500GB | 3 |
| **大型** | 32核 | 64GB | 1TB | 5+ |

### C. 相关链接

- [QUANTAXIS GitHub](https://github.com/QUANTAXIS/QUANTAXIS)
- [Docker Hub](https://hub.docker.com/u/quantaxis)
- [官方文档](https://doc.yutiansut.com/)
- [社区论坛](http://www.yutiansut.com/)

---

**作者**: @yutiansut @quantaxis
**最后更新**: 2025-10-25
**版本**: 2.1.0-alpha2

如有问题,请提交Issue或加入QQ群: 563280067

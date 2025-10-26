# 生产环境部署

**版本**: 2.1.0-alpha2
**作者**: @yutiansut @quantaxis
**更新日期**: 2025-10-25

本文档提供QUANTAXIS生产环境部署的完整指南，包括硬件配置、系统优化、安全加固和监控方案。

---

## 🎯 生产环境架构

### 完整系统架构

```
                    ┌─────────────┐
                    │   Nginx     │
                    │  (负载均衡)  │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
    │ XServer │      │ XServer │      │ XServer │
    │  Node1  │      │  Node2  │      │  Node3  │
    └────┬────┘      └────┬────┘      └────┬────┘
         │                │                 │
         └────────────────┼─────────────────┘
                          │
         ┌────────────────┴────────────────┐
         │                                 │
    ┌────▼────┐                      ┌────▼────┐
    │ MongoDB │                      │RabbitMQ │
    │ Cluster │                      │ Cluster │
    │(3 nodes)│                      │(3 nodes)│
    └─────────┘                      └─────────┘
         │
    ┌────▼────┐
    │ClickHouse│
    │  Cluster │
    └──────────┘

[策略服务器 - 独立部署]
    ┌─────────────────────────────┐
    │  XQuant Pods (多实例)       │
    │  ├─ Strategy 1              │
    │  ├─ Strategy 2              │
    │  └─ Strategy N              │
    └─────────────────────────────┘
```

---

## 🖥️ 硬件配置

### 推荐配置

#### 数据库服务器

```yaml
MongoDB Primary:
  CPU: 32核心
  内存: 128GB
  存储: 
    - 系统盘: 500GB SSD
    - 数据盘: 4TB NVMe SSD (RAID 10)
  网络: 10Gbps

ClickHouse Node:
  CPU: 64核心
  内存: 256GB
  存储:
    - 系统盘: 500GB SSD
    - 数据盘: 10TB NVMe SSD (RAID 10)
  网络: 10Gbps
```

#### Web/API服务器

```yaml
XServer Node:
  CPU: 16核心
  内存: 64GB
  存储: 1TB SSD
  网络: 10Gbps
```

#### 策略服务器

```yaml
XQuant Node:
  CPU: 32核心
  内存: 128GB
  存储: 2TB NVMe SSD
  网络: 10Gbps（低延迟）
```

---

## ⚙️ 系统优化

### 1. Linux内核优化

```bash
# /etc/sysctl.conf
cat >> /etc/sysctl.conf << 'SYSCTL'
# 网络优化
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.ipv4.tcp_rmem = 4096 87380 67108864
net.ipv4.tcp_wmem = 4096 65536 67108864
net.ipv4.tcp_max_syn_backlog = 8192
net.core.netdev_max_backlog = 5000
net.core.somaxconn = 4096

# 文件句柄
fs.file-max = 2097152
fs.nr_open = 2097152

# 共享内存
kernel.shmmax = 68719476736
kernel.shmall = 4294967296

# 交换分区
vm.swappiness = 1
vm.dirty_ratio = 80
vm.dirty_background_ratio = 5

# 透明大页
vm.nr_hugepages = 1280
SYSCTL

# 应用配置
sysctl -p
```

### 2. 用户限制

```bash
# /etc/security/limits.conf
cat >> /etc/security/limits.conf << 'LIMITS'
*  soft  nofile  1048576
*  hard  nofile  1048576
*  soft  nproc   unlimited
*  hard  nproc   unlimited
*  soft  core    unlimited
*  hard  core    unlimited
*  soft  memlock unlimited
*  hard  memlock unlimited
LIMITS
```

### 3. 磁盘优化

```bash
# SSD优化
# /etc/fstab
/dev/nvme0n1 /data ext4 noatime,nodiratime,discard 0 0

# I/O调度器
echo "none" > /sys/block/nvme0n1/queue/scheduler

# 挂载点优化
mount -o remount,noatime,nodiratime /data
```

---

## 🔒 安全加固

### 1. 防火墙配置

```bash
# 使用firewalld
systemctl enable firewalld
systemctl start firewalld

# 开放必要端口
firewall-cmd --permanent --add-port=8010/tcp  # XWebServer
firewall-cmd --permanent --add-port=27017/tcp # MongoDB
firewall-cmd --permanent --add-port=5672/tcp  # RabbitMQ
firewall-cmd --permanent --add-port=15672/tcp # RabbitMQ管理
firewall-cmd --permanent --add-port=9000/tcp  # ClickHouse

# 限制IP访问
firewall-cmd --permanent --add-rich-rule='
  rule family="ipv4"
  source address="192.168.1.0/24"
  port port="27017" protocol="tcp" accept'

firewall-cmd --reload
```

### 2. MongoDB安全

```javascript
// 创建管理员用户
use admin
db.createUser({
  user: "admin",
  pwd: "StrongPassword123!",
  roles: [
    { role: "root", db: "admin" }
  ]
})

// 创建应用用户
use quantaxis
db.createUser({
  user: "quantaxis_user",
  pwd: "AppPassword456!",
  roles: [
    { role: "readWrite", db: "quantaxis" }
  ]
})

// 启用认证
// /etc/mongod.conf
security:
  authorization: enabled
  
// 启用TLS
net:
  tls:
    mode: requireTLS
    certificateKeyFile: /etc/ssl/mongodb.pem
    CAFile: /etc/ssl/ca.pem
```

### 3. RabbitMQ安全

```bash
# 更改默认密码
rabbitmqctl change_password admin 'NewStrongPassword789!'

# 创建应用用户
rabbitmqctl add_user quantaxis 'AppPassword!'
rabbitmqctl set_permissions -p / quantaxis ".*" ".*" ".*"

# 删除guest用户
rabbitmqctl delete_user guest

# 启用TLS
# /etc/rabbitmq/rabbitmq.conf
listeners.ssl.default = 5671
ssl_options.cacertfile = /etc/ssl/ca.pem
ssl_options.certfile   = /etc/ssl/server.pem
ssl_options.keyfile    = /etc/ssl/server-key.pem
ssl_options.verify     = verify_peer
ssl_options.fail_if_no_peer_cert = true
```

### 4. 应用安全

```python
# config/production.yml
security:
  jwt:
    secret_key: "${JWT_SECRET_KEY}"  # 从环境变量读取
    algorithm: "HS256"
    expire_minutes: 60
  
  cors:
    allowed_origins:
      - "https://quantaxis.example.com"
    allowed_methods: ["GET", "POST"]
  
  rate_limit:
    enabled: true
    requests_per_minute: 100
    
  ssl:
    enabled: true
    cert_file: "/etc/ssl/quantaxis.crt"
    key_file: "/etc/ssl/quantaxis.key"
```

---

## 📊 数据库集群

### 1. MongoDB副本集

```bash
# 初始化副本集
mongo --host mongodb1:27017 << 'MONGO'
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongodb1:27017", priority: 2 },
    { _id: 1, host: "mongodb2:27017", priority: 1 },
    { _id: 2, host: "mongodb3:27017", arbiterOnly: true }
  ]
})
MONGO

# 检查状态
mongo --host mongodb1:27017 --eval "rs.status()"
```

### 2. RabbitMQ集群

```bash
# Node1
rabbitmqctl stop_app
rabbitmqctl reset
rabbitmqctl start_app

# Node2
rabbitmqctl stop_app
rabbitmqctl reset
rabbitmqctl join_cluster rabbit@node1
rabbitmqctl start_app

# Node3
rabbitmqctl stop_app
rabbitmqctl reset
rabbitmqctl join_cluster rabbit@node1
rabbitmqctl start_app

# 设置镜像队列
rabbitmqctl set_policy ha-all "^" '{"ha-mode":"all","ha-sync-mode":"automatic"}'
```

### 3. ClickHouse集群

```xml
<!-- /etc/clickhouse-server/config.xml -->
<yandex>
  <remote_servers>
    <quantaxis_cluster>
      <shard>
        <replica>
          <host>clickhouse1</host>
          <port>9000</port>
        </replica>
        <replica>
          <host>clickhouse2</host>
          <port>9000</port>
        </replica>
      </shard>
    </quantaxis_cluster>
  </remote_servers>
  
  <zookeeper>
    <node>
      <host>zk1</host>
      <port>2181</port>
    </node>
    <node>
      <host>zk2</host>
      <port>2181</port>
    </node>
    <node>
      <host>zk3</host>
      <port>2181</port>
    </node>
  </zookeeper>
</yandex>
```

---

## 🔄 高可用部署

### 1. Nginx负载均衡

```nginx
# /etc/nginx/nginx.conf
upstream xserver_backend {
    least_conn;
    server 192.168.1.11:8010 weight=1 max_fails=3 fail_timeout=30s;
    server 192.168.1.12:8010 weight=1 max_fails=3 fail_timeout=30s;
    server 192.168.1.13:8010 weight=1 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name quantaxis.example.com;
    
    # HTTPS重定向
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name quantaxis.example.com;
    
    ssl_certificate /etc/ssl/quantaxis.crt;
    ssl_certificate_key /etc/ssl/quantaxis.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    location / {
        proxy_pass http://xserver_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # 健康检查
    location /health {
        access_log off;
        proxy_pass http://xserver_backend/health;
    }
}
```

### 2. Keepalived高可用

```bash
# Master节点
# /etc/keepalived/keepalived.conf
vrrp_script check_nginx {
    script "/usr/bin/killall -0 nginx"
    interval 2
    weight 2
}

vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 51
    priority 101
    advert_int 1
    
    authentication {
        auth_type PASS
        auth_pass quantaxis
    }
    
    virtual_ipaddress {
        192.168.1.100/24
    }
    
    track_script {
        check_nginx
    }
}
```

---

## 📈 监控系统

### 1. Prometheus配置

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['localhost:9093']

scrape_configs:
  - job_name: 'xserver'
    static_configs:
      - targets: ['192.168.1.11:8010', '192.168.1.12:8010', '192.168.1.13:8010']
  
  - job_name: 'mongodb'
    static_configs:
      - targets: ['192.168.1.21:9216']
  
  - job_name: 'rabbitmq'
    static_configs:
      - targets: ['192.168.1.31:15692']
  
  - job_name: 'node_exporter'
    static_configs:
      - targets: ['192.168.1.11:9100', '192.168.1.12:9100']
```

### 2. 告警规则

```yaml
# alerts.yml
groups:
  - name: quantaxis
    interval: 30s
    rules:
      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "CPU使用率过高"
          description: "{{ $labels.instance }} CPU使用率: {{ $value }}%"
      
      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100 > 90
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "内存使用率过高"
          description: "{{ $labels.instance }} 内存使用率: {{ $value }}%"
      
      - alert: MongoDBDown
        expr: up{job="mongodb"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "MongoDB服务下线"
          description: "MongoDB {{ $labels.instance }} 无法访问"
      
      - alert: StrategyError
        expr: rate(strategy_errors_total[5m]) > 0.1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "策略错误率过高"
          description: "策略 {{ $labels.strategy }} 错误率: {{ $value }}/s"
```

### 3. Grafana仪表板

```json
{
  "dashboard": {
    "title": "QUANTAXIS生产监控",
    "panels": [
      {
        "title": "系统CPU使用率",
        "targets": [{
          "expr": "100 - (avg by(instance) (irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)"
        }]
      },
      {
        "title": "策略收益曲线",
        "targets": [{
          "expr": "strategy_balance{strategy=\".*\"}"
        }]
      },
      {
        "title": "数据库查询延迟",
        "targets": [{
          "expr": "mongodb_query_latency_seconds"
        }]
      }
    ]
  }
}
```

---

## 🔧 自动化部署

### Ansible Playbook

```yaml
# deploy.yml
---
- name: Deploy QUANTAXIS Production
  hosts: all
  become: yes
  
  vars:
    quantaxis_version: "2.1.0"
    mongodb_version: "5.0"
    
  tasks:
    - name: 安装依赖
      yum:
        name:
          - python3
          - python3-pip
          - nginx
        state: present
    
    - name: 部署MongoDB
      include_role:
        name: mongodb
      when: "'mongodb' in group_names"
    
    - name: 部署RabbitMQ
      include_role:
        name: rabbitmq
      when: "'rabbitmq' in group_names"
    
    - name: 部署QUANTAXIS
      include_role:
        name: quantaxis
      when: "'xserver' in group_names"
    
    - name: 配置监控
      include_role:
        name: monitoring
```

---

## 🔗 相关资源

- **Kubernetes**: [Kubernetes部署](./kubernetes.md)
- **性能优化**: [性能优化指南](../advanced/performance-tuning.md)
- **监控告警**: [部署概览](./overview.md)

---

## 📝 总结

生产环境部署要点：

✅ **高可用**: 多节点集群 + 负载均衡 + 故障转移  
✅ **高性能**: 硬件优化 + 系统调优 + 数据库集群  
✅ **安全性**: 认证加密 + 防火墙 + 审计日志  
✅ **可监控**: Prometheus + Grafana + 告警  
✅ **易维护**: 自动化部署 + 配置管理 + 备份恢复  

---

**作者**: @yutiansut @quantaxis
**最后更新**: 2025-10-25

[返回部署指南](../README.md)

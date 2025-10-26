# Kubernetes部署

**版本**: 2.1.0-alpha2
**作者**: @yutiansut @quantaxis
**更新日期**: 2025-10-25

本文档介绍如何在Kubernetes集群上部署QUANTAXIS完整系统。

---

## 🎯 部署架构

### 系统组件

```
┌─────────────────────────────────────────────┐
│            Kubernetes Cluster               │
│                                             │
│  ┌─────────────┐    ┌─────────────┐        │
│  │   Ingress   │    │   Service   │        │
│  └──────┬──────┘    └──────┬──────┘        │
│         │                  │                │
│  ┌──────▼──────────────────▼──────┐        │
│  │      XWebServer (3 replicas)    │        │
│  └──────┬──────────────────┬──────┘        │
│         │                  │                │
│  ┌──────▼──────┐    ┌─────▼──────┐        │
│  │  MongoDB    │    │  RabbitMQ  │        │
│  │ StatefulSet │    │ StatefulSet│        │
│  └─────────────┘    └────────────┘        │
│                                             │
│  ┌─────────────────────────────────┐       │
│  │   XQuant (Strategy Pods)        │       │
│  └─────────────────────────────────┘       │
└─────────────────────────────────────────────┘
```

---

## 📦 前置要求

### 1. Kubernetes集群

```bash
# 检查集群版本
kubectl version

# 推荐版本
Kubernetes: v1.24+
```

### 2. 存储配置

```yaml
# storage-class.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: quantaxis-storage
provisioner: kubernetes.io/aws-ebs  # 根据云厂商调整
parameters:
  type: gp3
  fsType: ext4
reclaimPolicy: Retain
volumeBindingMode: WaitForFirstConsumer
```

```bash
kubectl apply -f storage-class.yaml
```

---

## 🚀 快速部署

### 1. 创建命名空间

```bash
kubectl create namespace quantaxis
kubectl config set-context --current --namespace=quantaxis
```

### 2. 部署MongoDB

```yaml
# mongodb-statefulset.yaml
apiVersion: v1
kind: Service
metadata:
  name: mongodb
  namespace: quantaxis
spec:
  ports:
  - port: 27017
    name: mongodb
  clusterIP: None
  selector:
    app: mongodb
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mongodb
  namespace: quantaxis
spec:
  serviceName: mongodb
  replicas: 1
  selector:
    matchLabels:
      app: mongodb
  template:
    metadata:
      labels:
        app: mongodb
    spec:
      containers:
      - name: mongodb
        image: mongo:5.0
        ports:
        - containerPort: 27017
          name: mongodb
        env:
        - name: MONGO_INITDB_ROOT_USERNAME
          value: "admin"
        - name: MONGO_INITDB_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mongodb-secret
              key: password
        volumeMounts:
        - name: mongodb-data
          mountPath: /data/db
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "8Gi"
            cpu: "4"
  volumeClaimTemplates:
  - metadata:
      name: mongodb-data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: quantaxis-storage
      resources:
        requests:
          storage: 100Gi
```

```bash
# 创建Secret
kubectl create secret generic mongodb-secret \
  --from-literal=password='your-password-here' \
  -n quantaxis

# 部署MongoDB
kubectl apply -f mongodb-statefulset.yaml
```

### 3. 部署RabbitMQ

```yaml
# rabbitmq-statefulset.yaml
apiVersion: v1
kind: Service
metadata:
  name: rabbitmq
  namespace: quantaxis
spec:
  ports:
  - port: 5672
    name: amqp
  - port: 15672
    name: management
  clusterIP: None
  selector:
    app: rabbitmq
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: rabbitmq
  namespace: quantaxis
spec:
  serviceName: rabbitmq
  replicas: 1
  selector:
    matchLabels:
      app: rabbitmq
  template:
    metadata:
      labels:
        app: rabbitmq
    spec:
      containers:
      - name: rabbitmq
        image: rabbitmq:3.11-management
        ports:
        - containerPort: 5672
          name: amqp
        - containerPort: 15672
          name: management
        env:
        - name: RABBITMQ_DEFAULT_USER
          value: "admin"
        - name: RABBITMQ_DEFAULT_PASS
          valueFrom:
            secretKeyRef:
              name: rabbitmq-secret
              key: password
        volumeMounts:
        - name: rabbitmq-data
          mountPath: /var/lib/rabbitmq
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
  volumeClaimTemplates:
  - metadata:
      name: rabbitmq-data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: quantaxis-storage
      resources:
        requests:
          storage: 20Gi
```

```bash
# 创建Secret
kubectl create secret generic rabbitmq-secret \
  --from-literal=password='your-password-here' \
  -n quantaxis

# 部署RabbitMQ
kubectl apply -f rabbitmq-statefulset.yaml
```

### 4. 部署Web服务

```yaml
# xwebserver-deployment.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: xwebserver-config
  namespace: quantaxis
data:
  config.yml: |
    server:
      host: 0.0.0.0
      port: 8010
    mongodb:
      host: mongodb
      port: 27017
      username: admin
      password: ${MONGO_PASSWORD}
    rabbitmq:
      host: rabbitmq
      port: 5672
      username: admin
      password: ${RABBITMQ_PASSWORD}
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: xwebserver
  namespace: quantaxis
spec:
  replicas: 3
  selector:
    matchLabels:
      app: xwebserver
  template:
    metadata:
      labels:
        app: xwebserver
    spec:
      containers:
      - name: xwebserver
        image: quantaxis/xwebserver:2.1.0
        ports:
        - containerPort: 8010
          name: http
        env:
        - name: MONGO_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mongodb-secret
              key: password
        - name: RABBITMQ_PASSWORD
          valueFrom:
            secretKeyRef:
              name: rabbitmq-secret
              key: password
        volumeMounts:
        - name: config
          mountPath: /app/config
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1"
        livenessProbe:
          httpGet:
            path: /health
            port: 8010
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8010
          initialDelaySeconds: 10
          periodSeconds: 5
      volumes:
      - name: config
        configMap:
          name: xwebserver-config
---
apiVersion: v1
kind: Service
metadata:
  name: xwebserver
  namespace: quantaxis
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 8010
    name: http
  selector:
    app: xwebserver
```

```bash
kubectl apply -f xwebserver-deployment.yaml
```

### 5. 配置Ingress

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: quantaxis-ingress
  namespace: quantaxis
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - quantaxis.example.com
    secretName: quantaxis-tls
  rules:
  - host: quantaxis.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: xwebserver
            port:
              number: 80
```

```bash
kubectl apply -f ingress.yaml
```

---

## 📊 策略Pod部署

### 策略Deployment

```yaml
# strategy-deployment.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: strategy-config
  namespace: quantaxis
data:
  strategy.py: |
    from QUANTAXIS.QAStrategy import QAStrategyCtaBase
    import QUANTAXIS as QA
    
    class MyStrategy(QAStrategyCtaBase):
        def user_init(self):
            self.fast_period = 5
            self.slow_period = 20
        
        def on_bar(self, bar):
            market_data = self.get_code_marketdata(bar.code)
            if len(market_data) < self.slow_period:
                return
            
            close_prices = [x['close'] for x in market_data]
            ma_fast = QA.MA(close_prices, self.fast_period)
            ma_slow = QA.MA(close_prices, self.slow_period)
            
            positions = self.acc.positions
            if ma_fast[-1] > ma_slow[-1] and bar.code not in positions:
                self.BuyOpen(bar.code, 1)
            elif ma_fast[-1] < ma_slow[-1] and bar.code in positions:
                self.SellClose(bar.code, 1)
    
    if __name__ == '__main__':
        strategy = MyStrategy(
            code='rb2501',
            frequence='5min',
            model='live',
            data_host='rabbitmq',
            trade_host='rabbitmq'
        )
        strategy.run()
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: strategy-runner
  namespace: quantaxis
spec:
  replicas: 2
  selector:
    matchLabels:
      app: strategy
  template:
    metadata:
      labels:
        app: strategy
    spec:
      containers:
      - name: strategy
        image: quantaxis/python:2.1.0
        command: ["python", "/app/strategy.py"]
        volumeMounts:
        - name: strategy-code
          mountPath: /app
        env:
        - name: MONGO_HOST
          value: "mongodb"
        - name: RABBITMQ_HOST
          value: "rabbitmq"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
      volumes:
      - name: strategy-code
        configMap:
          name: strategy-config
```

```bash
kubectl apply -f strategy-deployment.yaml
```

---

## 🔧 配置管理

### 1. ConfigMap管理

```bash
# 查看ConfigMap
kubectl get configmap -n quantaxis

# 更新ConfigMap
kubectl edit configmap xwebserver-config -n quantaxis

# 重启Pod应用配置
kubectl rollout restart deployment/xwebserver -n quantaxis
```

### 2. Secret管理

```bash
# 查看Secret
kubectl get secret -n quantaxis

# 更新Secret
kubectl create secret generic mongodb-secret \
  --from-literal=password='new-password' \
  --dry-run=client -o yaml | kubectl apply -f -

# 重启相关Pod
kubectl rollout restart statefulset/mongodb -n quantaxis
```

---

## 📈 监控和日志

### 1. 部署Prometheus

```yaml
# prometheus-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: quantaxis
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    
    scrape_configs:
    - job_name: 'xwebserver'
      kubernetes_sd_configs:
      - role: pod
        namespaces:
          names:
          - quantaxis
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        action: keep
        regex: xwebserver
```

### 2. 查看日志

```bash
# 查看Pod日志
kubectl logs -f deployment/xwebserver -n quantaxis

# 查看特定容器日志
kubectl logs -f statefulset/mongodb -n quantaxis

# 查看最近100行日志
kubectl logs --tail=100 deployment/strategy-runner -n quantaxis

# 导出所有日志
kubectl logs deployment/xwebserver -n quantaxis > xwebserver.log
```

### 3. 事件监控

```bash
# 查看事件
kubectl get events -n quantaxis --sort-by='.lastTimestamp'

# 监控Pod状态
kubectl get pods -n quantaxis -w
```

---

## 🔄 维护操作

### 1. 滚动更新

```bash
# 更新镜像
kubectl set image deployment/xwebserver \
  xwebserver=quantaxis/xwebserver:2.1.1 \
  -n quantaxis

# 查看更新状态
kubectl rollout status deployment/xwebserver -n quantaxis

# 回滚
kubectl rollout undo deployment/xwebserver -n quantaxis

# 查看历史版本
kubectl rollout history deployment/xwebserver -n quantaxis
```

### 2. 扩缩容

```bash
# 手动扩容
kubectl scale deployment/xwebserver --replicas=5 -n quantaxis

# 自动扩容（HPA）
kubectl autoscale deployment/xwebserver \
  --min=3 --max=10 \
  --cpu-percent=80 \
  -n quantaxis
```

### 3. 数据备份

```bash
# MongoDB备份
kubectl exec -it mongodb-0 -n quantaxis -- \
  mongodump --out /backup/$(date +%Y%m%d)

# 复制备份到本地
kubectl cp quantaxis/mongodb-0:/backup ./mongodb-backup
```

---

## ⚠️ 故障排查

### 常见问题

**Q1: Pod无法启动**

```bash
# 查看Pod详情
kubectl describe pod <pod-name> -n quantaxis

# 查看事件
kubectl get events -n quantaxis

# 常见原因：
# 1. 镜像拉取失败 → 检查镜像名称和权限
# 2. 资源不足 → kubectl top nodes
# 3. 配置错误 → kubectl logs <pod-name>
```

**Q2: 服务连接失败**

```bash
# 检查Service
kubectl get svc -n quantaxis

# 测试连接
kubectl run -it --rm debug \
  --image=busybox \
  --restart=Never \
  -n quantaxis \
  -- sh

# 在Pod内测试
nslookup mongodb
telnet rabbitmq 5672
```

**Q3: 存储问题**

```bash
# 查看PVC状态
kubectl get pvc -n quantaxis

# 查看PV
kubectl get pv

# 如果PVC处于Pending状态，检查StorageClass
kubectl describe pvc <pvc-name> -n quantaxis
```

---

## 🔗 相关资源

- **生产环境**: [生产环境部署](./production.md)
- **性能优化**: [性能优化指南](../advanced/performance-tuning.md)
- **Docker**: [Docker部署](./overview.md)

---

## 📝 总结

Kubernetes部署QUANTAXIS提供：

✅ **高可用**: 多副本部署，自动故障转移  
✅ **可扩展**: 水平扩展，弹性伸缩  
✅ **易维护**: 滚动更新，版本管理  
✅ **监控完善**: Prometheus + Grafana  
✅ **存储持久化**: StatefulSet + PV/PVC  

---

**作者**: @yutiansut @quantaxis
**最后更新**: 2025-10-25

[返回部署指南](../README.md)

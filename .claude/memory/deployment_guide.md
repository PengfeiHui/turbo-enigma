---
name: deployment-guide
description: 生产环境部署指南和注意事项
metadata:
  type: project
---

生产环境部署的关键步骤和配置。

**Why:** 确保系统能够稳定、安全地部署到生产环境。

**How to apply:** 部署前检查这些配置和步骤。

## 部署前检查清单

### 环境配置
- [ ] 修改 `backend/.env` 中的 `SECRET_KEY`（生成新的随机密钥）
- [ ] 设置 `DEBUG=False`
- [ ] 配置生产数据库连接
- [ ] 配置 Redis 连接
- [ ] 确认阿里百炼 API Key 有效且有足够余额

### 安全配置
- [ ] 修改默认管理员密码（admin/123456）
- [ ] 配置 CORS 允许的源
- [ ] 启用 HTTPS（生产环境必须）
- [ ] 配置防火墙规则
- [ ] 设置 API 限流

### 数据库
- [ ] 备份现有数据
- [ ] 运行数据库迁移
- [ ] 配置数据库自动备份
- [ ] 优化数据库索引

### 向量库
- [ ] 确保 `data/chroma_db` 目录持久化
- [ ] 备份向量库数据
- [ ] 测试向量检索性能

## Docker 部署（推荐）

### 1. 构建镜像

```bash
cd D:\code\projects\longChain_RAG

# 构建后端镜像
cd backend
docker build -t rag-backend:latest .

# 构建前端镜像（如果需要）
cd ../frontend
npm run build
# 使用 nginx 托管构建产物
```

### 2. 启动服务

```bash
docker-compose up -d
```

### 3. 初始化数据库

```bash
docker exec -it rag_backend python /app/scripts/init_db.py
```

### 4. 健康检查

```bash
curl http://localhost:8000/health
```

## 传统部署

### 后端部署

```bash
# 1. 安装依赖
cd backend
pip install -r requirements.txt

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env

# 3. 初始化数据库
cd ..
python scripts/init_db.py

# 4. 使用 Gunicorn 运行
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### 前端部署

```bash
# 1. 构建生产版本
cd frontend
npm run build

# 2. 部署到 Nginx
# 将 dist 目录内容复制到 nginx 的 html 目录
```

### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端
    location / {
        root /var/www/rag-frontend;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # SSE 支持
        proxy_buffering off;
        proxy_cache off;
        proxy_set_header Connection '';
        proxy_http_version 1.1;
        chunked_transfer_encoding off;
    }
}
```

## 监控和日志

### 应用监控
- 使用 Prometheus + Grafana
- 监控 API 响应时间
- 监控错误率
- 监控资源使用

### 日志配置
```python
# backend/app/main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

## 性能优化

### 数据库
- 添加适当索引
- 配置连接池
- 定期清理旧数据

### 缓存
- Redis 缓存常见查询
- 向量检索结果缓存
- API 响应缓存

### CDN
- 静态资源使用 CDN
- 图片压缩和优化

## 备份策略

### 数据库备份
```bash
# 每天自动备份
0 2 * * * pg_dump rag_db > /backup/rag_db_$(date +\%Y\%m\%d).sql
```

### 向量库备份
```bash
# 备份 Chroma 数据目录
tar -czf chroma_backup_$(date +%Y%m%d).tar.gz data/chroma_db/
```

## 故障恢复

### 数据库恢复
```bash
psql rag_db < /backup/rag_db_20260922.sql
```

### 向量库恢复
```bash
tar -xzf chroma_backup_20260922.tar.gz -C data/
```

## 扩展方案

### 水平扩展
- 多个后端实例 + 负载均衡
- 使用 Redis 共享会话
- 向量库使用分布式方案（Milvus）

### 垂直扩展
- 增加服务器资源
- 优化数据库配置
- 升级到更强的 GPU（如果使用本地模型）

---

**注意**: 生产环境必须修改所有默认密码和密钥！

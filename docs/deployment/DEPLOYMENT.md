# LongChain RAG 系统部署指南

## 📋 目录
- [部署架构](#部署架构)
- [服务器要求](#服务器要求)
- [部署方式对比](#部署方式对比)
- [Docker 部署（推荐）](#docker-部署推荐)
- [传统部署](#传统部署)
- [生产环境优化](#生产环境优化)
- [监控与维护](#监控与维护)

---

## 🏗️ 部署架构

```
                    ┌─────────────────┐
                    │   Nginx (80/443)│
                    │  反向代理 + SSL  │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
          ┌─────────▼──────┐  ┌──────▼──────────┐
          │  Frontend      │  │  Backend API    │
          │  (Vue.js)      │  │  (FastAPI)      │
          │  静态文件       │  │  :8000          │
          └────────────────┘  └────────┬────────┘
                                       │
                              ┌────────┴────────┐
                              │                 │
                    ┌─────────▼──────┐  ┌──────▼──────────┐
                    │  PostgreSQL    │  │  Chroma Vector  │
                    │  数据库         │  │  向量数据库      │
                    └────────────────┘  └─────────────────┘
```

---

## 💻 服务器要求

### 最小配置
- **CPU**: 2核
- **内存**: 4GB
- **硬盘**: 20GB SSD
- **系统**: Ubuntu 20.04/22.04 或 CentOS 7/8

### 推荐配置
- **CPU**: 4核
- **内存**: 8GB
- **硬盘**: 50GB SSD
- **系统**: Ubuntu 22.04 LTS
- **带宽**: 5Mbps 以上

### 注意事项
- 向量数据库（Chroma）需要足够的内存
- 文档上传需要充足的磁盘空间
- AI 模型调用需要稳定的网络连接

---

## 🔄 部署方式对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **Docker Compose** | • 一键部署<br>• 环境隔离<br>• 易于迁移 | • 需要学习 Docker | **推荐**：生产环境 |
| **传统部署** | • 直接控制<br>• 性能最优 | • 配置复杂<br>• 依赖管理困难 | 熟悉 Linux 的用户 |
| **云平台 PaaS** | • 全托管<br>• 自动扩展 | • 成本较高 | 预算充足的企业 |

---

## 🐳 Docker 部署（推荐）

### 1. 创建 Docker 配置文件

#### `Dockerfile.backend`
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY backend/requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY backend/ .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### `Dockerfile.frontend`
```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# 复制依赖文件
COPY frontend/package*.json ./

# 安装依赖
RUN npm ci

# 复制源码
COPY frontend/ .

# 构建
RUN npm run build

# 使用 Nginx 提供静态文件
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### `docker-compose.yml`
```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    container_name: longchain-backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/longchain_rag
      - DASHSCOPE_API_KEY=${DASHSCOPE_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./backend/uploads:/app/uploads
      - ./backend/chroma_db:/app/chroma_db
    depends_on:
      - db
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    container_name: longchain-frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    container_name: longchain-db
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=longchain_rag
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

#### `.env` 文件
```env
# API Keys
DASHSCOPE_API_KEY=your_dashscope_api_key_here

# Security
SECRET_KEY=your_super_secret_key_here_generate_with_openssl

# Database
DATABASE_URL=postgresql://postgres:password@db:5432/longchain_rag
```

### 2. 部署步骤

```bash
# 1. 连接到服务器
ssh user@your-server-ip

# 2. 安装 Docker 和 Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 安装 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 3. 上传项目文件
# 使用 git 或 scp
git clone https://github.com/your-repo/longChain_RAG.git
cd longChain_RAG

# 4. 配置环境变量
nano .env
# 填入实际的 API key 和密钥

# 5. 生成密钥（用于 SECRET_KEY）
openssl rand -hex 32

# 6. 启动服务
docker-compose up -d

# 7. 查看日志
docker-compose logs -f

# 8. 初始化数据库（首次部署）
docker-compose exec backend alembic upgrade head

# 9. 创建管理员账号
docker-compose exec backend python -c "
from app.database import SessionLocal
from app.services.auth_service import auth_service
db = SessionLocal()
auth_service.create_user(db, 'admin', '123456', 'admin')
db.close()
print('Admin user created!')
"
```

### 3. Nginx 配置（带 SSL）

#### `nginx.conf`
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # 前端静态文件
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 代理
    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket 支持（如需要）
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # 文件大小限制
    client_max_body_size 10M;
}
```

### 4. 添加 SSL（Let's Encrypt）

```bash
# 1. 安装 Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# 2. 获取 SSL 证书
sudo certbot --nginx -d yourdomain.com

# 3. 自动续期（已自动配置）
sudo certbot renew --dry-run
```

---

## 🔧 传统部署

### 1. 安装依赖

```bash
# 更新系统
sudo apt-get update && sudo apt-get upgrade -y

# 安装 Python 3.10
sudo apt-get install python3.10 python3.10-venv python3-pip

# 安装 Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装 PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# 安装 Nginx
sudo apt-get install nginx
```

### 2. 部署后端

```bash
# 创建应用目录
sudo mkdir -p /var/www/longchain-rag
sudo chown $USER:$USER /var/www/longchain-rag
cd /var/www/longchain-rag

# 克隆项目
git clone https://github.com/your-repo/longChain_RAG.git .

# 创建虚拟环境
cd backend
python3.10 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
nano .env

# 初始化数据库
alembic upgrade head

# 使用 Supervisor 管理进程
sudo apt-get install supervisor
sudo nano /etc/supervisor/conf.d/longchain-backend.conf
```

#### Supervisor 配置
```ini
[program:longchain-backend]
directory=/var/www/longchain-rag/backend
command=/var/www/longchain-rag/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/longchain-backend.err.log
stdout_logfile=/var/log/longchain-backend.out.log
```

```bash
# 启动服务
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start longchain-backend
```

### 3. 部署前端

```bash
cd /var/www/longchain-rag/frontend

# 安装依赖
npm install

# 修改 API 地址
nano .env.production
# VITE_API_BASE_URL=https://yourdomain.com/api

# 构建
npm run build

# 复制到 Nginx 目录
sudo cp -r dist/* /var/www/html/
```

### 4. 配置 Nginx

```bash
sudo nano /etc/nginx/sites-available/longchain-rag
```

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    client_max_body_size 10M;
}
```

```bash
# 启用站点
sudo ln -s /etc/nginx/sites-available/longchain-rag /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🚀 生产环境优化

### 1. 性能优化

```bash
# 后端：使用 Gunicorn + Uvicorn Workers
pip install gunicorn

# 启动命令
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile /var/log/gunicorn-access.log \
  --error-logfile /var/log/gunicorn-error.log
```

### 2. 数据库优化

```sql
-- PostgreSQL 配置优化
-- /etc/postgresql/15/main/postgresql.conf

shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 4MB
min_wal_size = 1GB
max_wal_size = 4GB
```

### 3. 安全加固

```bash
# 1. 配置防火墙
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# 2. 禁用 root SSH 登录
sudo nano /etc/ssh/sshd_config
# PermitRootLogin no
# PasswordAuthentication no

# 3. 安装 fail2ban
sudo apt-get install fail2ban
sudo systemctl enable fail2ban

# 4. 定期更新
sudo apt-get update && sudo apt-get upgrade -y
```

### 4. 备份策略

```bash
# 创建备份脚本
nano /home/user/backup.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/backup/longchain-rag"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
docker-compose exec -T db pg_dump -U postgres longchain_rag > $BACKUP_DIR/db_$DATE.sql

# 备份文件
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz /var/www/longchain-rag/backend/uploads
tar -czf $BACKUP_DIR/chroma_$DATE.tar.gz /var/www/longchain-rag/backend/chroma_db

# 删除 7 天前的备份
find $BACKUP_DIR -mtime +7 -delete

echo "Backup completed: $DATE"
```

```bash
# 添加到 crontab
chmod +x /home/user/backup.sh
crontab -e
# 每天凌晨 2 点备份
0 2 * * * /home/user/backup.sh >> /var/log/backup.log 2>&1
```

---

## 📊 监控与维护

### 1. 日志管理

```bash
# 查看实时日志
docker-compose logs -f backend

# 查看错误日志
docker-compose logs backend | grep ERROR

# 日志轮转配置
sudo nano /etc/logrotate.d/longchain-rag
```

```
/var/log/longchain-*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    missingok
    create 640 www-data www-data
}
```

### 2. 监控指标

```bash
# 安装监控工具
docker run -d --name=prometheus \
  -p 9090:9090 \
  prom/prometheus

docker run -d --name=grafana \
  -p 3000:3000 \
  grafana/grafana
```

### 3. 健康检查

```bash
# 创建健康检查脚本
nano /home/user/health_check.sh
```

```bash
#!/bin/bash

# 检查后端 API
curl -f http://localhost:8000/api/health || echo "Backend down!" | mail -s "Alert" admin@example.com

# 检查数据库
docker-compose exec -T db pg_isready || echo "Database down!" | mail -s "Alert" admin@example.com

# 检查磁盘空间
df -h | awk '$5 > 80 {print "Disk usage alert: " $0}'
```

---

## 🎯 部署检查清单

- [ ] 服务器满足最低配置要求
- [ ] 已安装 Docker 和 Docker Compose
- [ ] 已配置环境变量（.env）
- [ ] 已生成安全的 SECRET_KEY
- [ ] 已配置数据库
- [ ] 已初始化数据库表
- [ ] 已创建管理员账号
- [ ] 已配置 Nginx 反向代理
- [ ] 已配置 SSL 证书
- [ ] 已配置防火墙规则
- [ ] 已设置自动备份
- [ ] 已配置日志轮转
- [ ] 已测试所有功能
- [ ] 已配置监控告警

---

## 🔗 相关资源

- [Docker 官方文档](https://docs.docker.com/)
- [Nginx 官方文档](https://nginx.org/en/docs/)
- [Let's Encrypt 文档](https://letsencrypt.org/docs/)
- [PostgreSQL 文档](https://www.postgresql.org/docs/)
- [FastAPI 部署指南](https://fastapi.tiangolo.com/deployment/)

---

## 📞 问题排查

### 常见问题

1. **端口被占用**
   ```bash
   sudo lsof -i :8000
   sudo kill -9 <PID>
   ```

2. **数据库连接失败**
   - 检查 DATABASE_URL 配置
   - 确认数据库服务运行中

3. **内存不足**
   - 增加 swap 空间
   - 优化 Chroma 向量库配置

4. **文件上传失败**
   - 检查 Nginx client_max_body_size
   - 检查磁盘空间

---

## 💡 建议

1. **使用 Docker Compose**：最简单、最可靠的部署方式
2. **配置 SSL**：保护用户数据安全
3. **定期备份**：避免数据丢失
4. **监控告警**：及时发现问题
5. **性能优化**：根据实际负载调整配置
6. **文档齐全**：记录所有配置和操作

---

**祝部署顺利！🎉**

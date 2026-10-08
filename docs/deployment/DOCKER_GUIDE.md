# Docker 服务启动指南

## 🚀 快速启动

### 1. 启动所有服务

```bash
# 进入项目目录
cd d:/code/projects/longChain_RAG

# 启动所有服务（数据库、Redis、后端、前端）
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

---

## 🎯 单独启动服务

### 只启动数据库（PostgreSQL）

```bash
# 启动数据库
docker-compose up -d db

# 检查数据库状态
docker-compose ps db

# 查看数据库日志
docker-compose logs -f db

# 连接到数据库
docker-compose exec db psql -U postgres -d longchain_rag
```

### 只启动 Redis

```bash
# 启动 Redis
docker-compose up -d redis

# 检查 Redis 状态
docker-compose ps redis

# 查看 Redis 日志
docker-compose logs -f redis

# 连接到 Redis
docker-compose exec redis redis-cli
```

### 启动数据库 + Redis

```bash
# 同时启动数据库和 Redis
docker-compose up -d db redis

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f db redis
```

---

## 🔧 常用命令

### 查看服务状态

```bash
# 查看所有服务
docker-compose ps

# 查看特定服务
docker-compose ps db
docker-compose ps redis
```

### 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看数据库日志
docker-compose logs -f db

# 查看 Redis 日志
docker-compose logs -f redis

# 查看最后 100 行日志
docker-compose logs --tail 100 db
```

### 停止服务

```bash
# 停止所有服务
docker-compose stop

# 停止特定服务
docker-compose stop db
docker-compose stop redis

# 停止并删除容器
docker-compose down

# 停止并删除容器+数据卷（危险！会删除数据）
docker-compose down -v
```

### 重启服务

```bash
# 重启所有服务
docker-compose restart

# 重启特定服务
docker-compose restart db
docker-compose restart redis
```

---

## 💾 数据管理

### 备份数据库

```bash
# 备份数据库到文件
docker-compose exec -T db pg_dump -U postgres longchain_rag > backup_$(date +%Y%m%d_%H%M%S).sql

# 或使用完整路径
docker-compose exec -T db pg_dump -U postgres longchain_rag > d:/backups/longchain_$(date +%Y%m%d).sql
```

### 恢复数据库

```bash
# 从备份文件恢复
docker-compose exec -T db psql -U postgres longchain_rag < backup.sql
```

### 查看 Redis 数据

```bash
# 进入 Redis 客户端
docker-compose exec redis redis-cli

# 常用 Redis 命令：
# - KEYS * (查看所有键)
# - GET key_name (获取值)
# - DEL key_name (删除键)
# - FLUSHALL (清空所有数据，危险！)
```

---

## 🐛 故障排查

### 问题 1：端口被占用

```bash
# 查看端口占用（Windows）
netstat -ano | findstr :5432
netstat -ano | findstr :6379

# 修改端口（编辑 docker-compose.yml）
# 将 "5432:5432" 改为 "5433:5432"
# 将 "6379:6379" 改为 "6380:6379"
```

### 问题 2：容器启动失败

```bash
# 查看详细错误信息
docker-compose logs db
docker-compose logs redis

# 删除容器重新创建
docker-compose down
docker-compose up -d
```

### 问题 3：数据丢失

```bash
# 检查数据卷
docker volume ls

# 查看数据卷详情
docker volume inspect longchain_rag_postgres_data
docker volume inspect longchain_rag_redis_data
```

### 问题 4：无法连接数据库

```bash
# 检查数据库是否启动
docker-compose ps db

# 检查健康状态
docker-compose exec db pg_isready -U postgres

# 进入容器排查
docker-compose exec db bash
```

---

## 📊 监控和维护

### 查看资源占用

```bash
# 查看容器资源使用情况
docker stats

# 查看特定容器
docker stats longchain-db
docker stats longchain-redis
```

### 清理未使用的资源

```bash
# 清理未使用的镜像
docker image prune

# 清理未使用的容器
docker container prune

# 清理未使用的数据卷（危险！）
docker volume prune

# 清理所有未使用的资源
docker system prune -a
```

---

## 🔐 安全建议

### 修改默认密码

编辑 `.env` 文件：

```env
# 数据库密码（建议使用强密码）
DB_PASSWORD=your_strong_password_here

# 生成随机密码
# openssl rand -base64 32
```

### 限制外部访问

如果只在本地开发，修改 `docker-compose.yml`：

```yaml
ports:
  - "127.0.0.1:5432:5432"  # 只允许本机访问
  - "127.0.0.1:6379:6379"
```

---

## 📝 开发环境 vs 生产环境

### 开发环境（当前配置）

```bash
# 启动所有服务
docker-compose up -d

# 后端使用 --reload 热重载
# 前端使用 npm run dev
```

### 生产环境

```bash
# 使用生产配置
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# 或使用部署脚本
sudo ./deploy.sh
```

---

## 🎯 推荐工作流

### 本地开发

```bash
# 1. 启动数据库和 Redis
docker-compose up -d db redis

# 2. 本地运行后端（方便调试）
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# 3. 本地运行前端（方便调试）
cd frontend
npm install
npm run dev
```

### 测试部署

```bash
# 使用 Docker 完整部署
docker-compose up -d

# 访问 http://localhost
```

### 生产部署

```bash
# 在服务器上
git clone https://gitee.com/huipengfei/long-chain_-rag.git
cd long-chain_-rag
sudo ./deploy.sh
```

---

## 🔗 连接信息

### PostgreSQL

- **主机**: localhost
- **端口**: 5432
- **数据库**: longchain_rag
- **用户名**: postgres
- **密码**: 在 .env 文件中的 DB_PASSWORD

**连接字符串**:
```
postgresql://postgres:postgres123@localhost:5432/longchain_rag
```

### Redis

- **主机**: localhost
- **端口**: 6379
- **密码**: 无（默认）

**连接字符串**:
```
redis://localhost:6379
```

---

## 💡 提示

1. **首次启动**: 第一次启动会下载镜像，需要等待几分钟
2. **数据持久化**: 数据保存在 Docker 卷中，删除容器不会丢失数据
3. **日志查看**: 使用 `docker-compose logs -f` 实时查看日志
4. **端口冲突**: 如果端口被占用，修改 docker-compose.yml 中的端口映射
5. **性能优化**: 生产环境建议分配更多资源

---

**快速开始命令**：

```bash
# 一键启动数据库和 Redis
cd d:/code/projects/longChain_RAG
docker-compose up -d db redis

# 查看状态
docker-compose ps

# 搞定！✅
```

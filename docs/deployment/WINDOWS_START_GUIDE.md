# 快速启动指南 - Windows 环境

## 📋 前提条件检查

### 检查是否已安装 Docker

打开 PowerShell 或 CMD，运行：

```bash
docker --version
docker-compose --version
```

如果显示版本号，说明已安装。如果没有，请按照下面的步骤安装。

---

## 🐳 安装 Docker Desktop（推荐）

### 方法 1：Docker Desktop（最简单）

1. **下载 Docker Desktop**
   - 访问：https://www.docker.com/products/docker-desktop
   - 下载 Windows 版本

2. **安装**
   - 双击安装包
   - 按照提示完成安装
   - 重启电脑

3. **启动 Docker Desktop**
   - 从开始菜单启动 Docker Desktop
   - 等待 Docker 启动完成（状态栏显示绿色）

4. **验证安装**
   ```bash
   docker --version
   docker-compose --version
   ```

---

## 🚀 启动数据库和 Redis

### 方式 1：使用 Docker Compose（推荐）

```bash
# 1. 打开 PowerShell 或 CMD
# 2. 进入项目目录
cd d:\code\projects\longChain_RAG

# 3. 启动数据库和 Redis
docker-compose up -d db redis

# 4. 查看服务状态
docker-compose ps

# 5. 查看日志
docker-compose logs -f db redis
```

### 方式 2：使用 Docker 命令（不推荐）

#### 启动 PostgreSQL

```bash
docker run -d \
  --name longchain-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres123 \
  -e POSTGRES_DB=longchain_rag \
  -p 5432:5432 \
  -v longchain_postgres_data:/var/lib/postgresql/data \
  postgres:15-alpine
```

#### 启动 Redis

```bash
docker run -d \
  --name longchain-redis \
  -p 6379:6379 \
  -v longchain_redis_data:/data \
  redis:7-alpine redis-server --appendonly yes
```

---

## 🔍 验证服务是否启动成功

### 检查容器状态

```bash
# 查看所有运行的容器
docker ps

# 应该看到：
# - longchain-db (PostgreSQL)
# - longchain-redis (Redis)
```

### 测试数据库连接

```bash
# 连接到 PostgreSQL
docker exec -it longchain-db psql -U postgres -d longchain_rag

# 成功后会显示：
# longchain_rag=#

# 退出：输入 \q
```

### 测试 Redis 连接

```bash
# 连接到 Redis
docker exec -it longchain-redis redis-cli

# 测试：
# 127.0.0.1:6379> PING
# 应该返回：PONG

# 退出：输入 exit
```

---

## 💻 本地开发（不使用 Docker）

如果你不想使用 Docker，也可以本地安装：

### 安装 PostgreSQL

1. **下载**：https://www.postgresql.org/download/windows/
2. **安装**：选择默认设置，记住密码
3. **创建数据库**：
   ```sql
   CREATE DATABASE longchain_rag;
   ```

### 安装 Redis

1. **下载**：https://github.com/microsoftarchive/redis/releases
2. **安装**：解压后运行 `redis-server.exe`
3. **测试**：运行 `redis-cli.exe`，输入 `PING`

### 修改配置

编辑 `backend/.env`：

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/longchain_rag
REDIS_HOST=localhost
REDIS_PORT=6379
```

---

## 🎯 推荐的开发流程

### 开发环境设置

```bash
# 1. 启动数据库和 Redis（Docker）
cd d:\code\projects\longChain_RAG
docker-compose up -d db redis

# 2. 启动后端（本地）
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# 3. 启动前端（本地）
# 新开一个终端
cd frontend
npm install
npm run dev

# 4. 访问应用
# 前端：http://localhost:5173
# 后端：http://localhost:8000
# API 文档：http://localhost:8000/docs
```

---

## 🐛 常见问题

### 问题 1：Docker Desktop 启动失败

**解决方案**：
1. 确保启用了 WSL 2（Windows Subsystem for Linux）
2. 在 BIOS 中启用虚拟化（Virtualization）
3. 以管理员身份运行 Docker Desktop

### 问题 2：端口被占用

**错误信息**：
```
Error: bind: address already in use
```

**解决方案**：
```bash
# 查看占用端口的进程
netstat -ano | findstr :5432
netstat -ano | findstr :6379

# 结束进程（替换 PID）
taskkill /PID <进程ID> /F

# 或修改端口
# 编辑 docker-compose.yml，将端口改为：
# - "5433:5432"  # PostgreSQL
# - "6380:6379"  # Redis
```

### 问题 3：容器无法启动

**解决方案**：
```bash
# 查看详细日志
docker-compose logs db
docker-compose logs redis

# 重新创建容器
docker-compose down
docker-compose up -d db redis
```

### 问题 4：数据丢失

**解决方案**：
```bash
# 检查数据卷
docker volume ls

# 查看数据卷位置
docker volume inspect longchain_rag_postgres_data

# 备份数据
docker-compose exec -T db pg_dump -U postgres longchain_rag > backup.sql
```

---

## 📊 服务管理

### 查看服务状态

```bash
# 查看运行的容器
docker-compose ps

# 查看日志
docker-compose logs -f db redis

# 查看资源占用
docker stats longchain-db longchain-redis
```

### 停止服务

```bash
# 停止服务（保留数据）
docker-compose stop

# 停止并删除容器（保留数据）
docker-compose down

# 停止并删除所有（包括数据，危险！）
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

## 🔗 连接信息

### PostgreSQL
- **主机**: localhost
- **端口**: 5432
- **数据库**: longchain_rag
- **用户名**: postgres
- **密码**: postgres123（在 .env 中修改）

### Redis
- **主机**: localhost
- **端口**: 6379

### 数据库工具推荐
- **PostgreSQL**: DBeaver, pgAdmin, DataGrip
- **Redis**: RedisInsight, Another Redis Desktop Manager

---

## ✅ 快速检查清单

- [ ] Docker Desktop 已安装并运行
- [ ] 运行 `docker-compose up -d db redis`
- [ ] 运行 `docker-compose ps` 确认服务启动
- [ ] 测试数据库连接
- [ ] 测试 Redis 连接
- [ ] 后端可以连接数据库
- [ ] 一切正常！🎉

---

## 💡 提示

1. **首次启动慢**：第一次运行会下载镜像，需要几分钟
2. **保存数据**：使用 Docker Volume，删除容器不会丢失数据
3. **定期备份**：重要数据请定期备份
4. **监控日志**：`docker-compose logs -f` 实时查看日志

---

**最简单的启动命令**：

```bash
cd d:\code\projects\longChain_RAG
docker-compose up -d db redis
```

就这么简单！✨

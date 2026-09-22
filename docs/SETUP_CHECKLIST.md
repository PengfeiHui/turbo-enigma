# 环境配置检查清单

## 当前状态
- ❌ Python 依赖未安装
- ❌ Docker 未安装
- ❌ PostgreSQL 未安装

## 选项 A：使用 Docker（推荐，最简单）

### 1. 安装 Docker Desktop
下载：https://www.docker.com/products/docker-desktop/

### 2. 启动所有服务
```bash
cd D:\code\projects\longChain_RAG
docker-compose up -d
```

这会自动启动：
- PostgreSQL 数据库
- Redis 缓存
- 后端 API 服务

## 选项 B：本地安装

### 1. 安装 Python 依赖
```bash
cd D:\code\projects\longChain_RAG\backend
pip install -r requirements.txt
```

### 2. 安装 PostgreSQL
下载：https://www.postgresql.org/download/windows/

安装后创建数据库：
```bash
psql -U postgres
CREATE DATABASE rag_db;
CREATE USER raguser WITH PASSWORD 'ragpass123';
GRANT ALL PRIVILEGES ON DATABASE rag_db TO raguser;
\q
```

### 3. 安装 Redis
下载：https://github.com/tporadowski/redis/releases
解压后运行 redis-server.exe

### 4. 配置阿里百炼 API Key
编辑 backend/.env 文件：
```
DASHSCOPE_API_KEY=你的API Key
```

获取地址：https://dashscope.aliyun.com/

### 5. 初始化数据库
```bash
cd D:\code\projects\longChain_RAG
python scripts/init_db.py
```

### 6. 启动后端
```bash
cd backend
uvicorn app.main:app --reload
```

## 测试后端
访问 http://localhost:8000/docs

---

## 接下来：前端开发

前端开发不需要后端运行，我现在就开始创建前端项目！

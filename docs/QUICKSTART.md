# 🚀 快速启动指南

## 第一步：环境准备

### 1. 安装 PostgreSQL 和 Redis

**Windows 用户：**

**PostgreSQL:**
1. 下载：https://www.postgresql.org/download/windows/
2. 安装时记住设置的密码
3. 创建数据库：
```cmd
psql -U postgres
CREATE DATABASE rag_db;
CREATE USER raguser WITH PASSWORD 'ragpass123';
GRANT ALL PRIVILEGES ON DATABASE rag_db TO raguser;
\q
```

**Redis:**
1. 下载：https://github.com/tporadowski/redis/releases
2. 解压后运行 `redis-server.exe`

**或使用 Docker（推荐）：**
```bash
docker run -d --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=ragpass123 -e POSTGRES_USER=raguser -e POSTGRES_DB=rag_db postgres:15
docker run -d --name redis -p 6379:6379 redis:7-alpine
```

### 2. 配置阿里百炼 API Key

1. 访问：https://dashscope.aliyun.com/
2. 登录阿里云账号
3. 开通"百炼大模型服务"
4. 获取 API Key
5. 编辑 `backend/.env` 文件，替换 `DASHSCOPE_API_KEY` 的值

---

## 第二步：后端部署

```bash
# 1. 进入后端目录
cd backend

# 2. 创建虚拟环境（推荐）
python -m venv venv

# Windows 激活：
venv\Scripts\activate

# Linux/Mac 激活：
# source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 检查 .env 配置
# 确认 DATABASE_URL 和 REDIS_URL 正确

# 5. 初始化数据库
cd ..
python scripts/init_db.py

# 6. 启动后端服务
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

启动成功后访问：
- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

---

## 第三步：数据采集（可选）

### 方案 A：运行爬虫（需要一定时间）

```bash
# 1. 进入爬虫目录
cd crawler

# 2. 安装依赖
pip install -r requirements.txt

# 3. 安装浏览器驱动
playwright install chromium

# 4. 运行爬虫（大约需要 5-10 分钟）
python pdd_crawler.py

# 5. 导入数据到向量库
cd ..
python scripts/import_products.py
```

### 方案 B：直接导入（爬虫生成模拟数据）

爬虫脚本已内置模拟数据生成功能，运行后会自动生成约 150 个商品数据。

```bash
# 运行爬虫（会生成模拟数据）
cd crawler
python pdd_crawler.py

# 导入向量库
cd ..
python scripts/import_products.py
```

---

## 第四步：测试后端 API

### 1. 注册用户

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"testuser\",\"password\":\"123456\"}"
```

### 2. 管理员登录

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"123456\"}"
```

返回示例：
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {...}
}
```

### 3. 创建会话

```bash
curl -X POST "http://localhost:8000/api/conversations" \
  -H "Authorization: Bearer <你的token>" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"测试会话\"}"
```

### 4. 测试问答

访问 API 文档页面 http://localhost:8000/docs，使用交互式界面测试 `/api/chat/ask` 接口。

---

## 第五步：前端部署（待开发）

前端代码将在后续创建。当前可以直接使用 API 文档页面进行测试。

---

## 🎯 使用测试流程

### 场景 1：管理员上传文档

1. 使用 `admin/123456` 登录获取 Token
2. 访问 http://localhost:8000/docs
3. 点击 "Authorize" 输入 Token
4. 使用 `POST /api/kb/upload` 接口上传 PDF/DOCX/TXT 文件
5. 系统自动分割文本并向量化

### 场景 2：用户问答

1. 创建会话：`POST /api/conversations`
2. 提问："有什么好的蓝牙耳机推荐，价格在 1000 元左右？"
3. 系统检索向量库，返回相关商品信息
4. 查看引用来源（sources 字段包含原文片段）

### 场景 3：查看历史记录

1. 获取会话列表：`GET /api/conversations`
2. 获取历史消息：`GET /api/conversations/{id}/messages`

---

## 🐛 常见问题排查

### 问题 1：数据库连接失败

**错误信息：** `could not connect to server`

**解决方案：**
1. 检查 PostgreSQL 是否启动：
   ```bash
   # Windows
   services.msc  # 查找 postgresql 服务
   
   # 或使用 Docker
   docker ps | grep postgres
   ```
2. 检查 `.env` 中的 `DATABASE_URL` 是否正确
3. 尝试手动连接测试：
   ```bash
   psql -h localhost -U raguser -d rag_db
   ```

### 问题 2：Redis 连接失败

**错误信息：** `Error connecting to Redis`

**解决方案：**
1. 检查 Redis 是否启动：
   ```bash
   redis-cli ping
   # 应返回 PONG
   ```
2. Windows 用户确保 `redis-server.exe` 正在运行

### 问题 3：阿里百炼 API 报错

**错误信息：** `Invalid API key` 或 `Rate limit exceeded`

**解决方案：**
1. 检查 API Key 是否正确填写在 `.env` 文件中
2. 登录百炼控制台检查余额
3. 查看 API 调用限制：https://help.aliyun.com/document_detail/2712195.html

### 问题 4：向量库为空，无法问答

**解决方案：**
1. 运行数据导入脚本：
   ```bash
   python scripts/import_products.py
   ```
2. 或上传文档到知识库

### 问题 5：依赖安装失败

**错误信息：** `Could not find a version that satisfies the requirement`

**解决方案：**
1. 升级 pip：
   ```bash
   python -m pip install --upgrade pip
   ```
2. 使用国内镜像：
   ```bash
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

---

## 📊 系统监控

### 查看向量库状态

```python
# 进入 Python 交互式环境
python

# 执行以下代码
import sys
sys.path.append('backend')
from app.services.vector_store_service import vector_store_service

count = vector_store_service.get_collection_count()
print(f"向量库文档数量: {count}")
```

### 查看数据库状态

```bash
# 连接数据库
psql -h localhost -U raguser -d rag_db

# 查看用户数量
SELECT COUNT(*) FROM users;

# 查看会话数量
SELECT COUNT(*) FROM conversations;

# 查看消息数量
SELECT COUNT(*) FROM messages;

# 退出
\q
```

---

## 🎉 成功标志

如果看到以下内容，说明部署成功：

1. ✅ 访问 http://localhost:8000 返回：
   ```json
   {
     "message": "RAG Knowledge Base API",
     "version": "1.0.0",
     "docs": "/docs"
   }
   ```

2. ✅ 访问 http://localhost:8000/docs 可以看到完整的 API 文档

3. ✅ 使用 admin/123456 可以成功登录

4. ✅ 问答接口能返回基于知识库的回答

---

## 📞 获取帮助

如果遇到其他问题：
1. 查看后端日志（终端输出）
2. 检查 `.env` 配置是否正确
3. 确认所有服务（PostgreSQL、Redis）正常运行
4. 查看 README.md 了解更多信息

---

**下一步：** 开发前端界面，提供更友好的用户体验！

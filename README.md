# RAG 企业级知识库问答系统

基于 LangChain 的 RAG（Retrieval-Augmented Generation）企业级知识库问答系统，专注于电商平台商品信息的智能问答。

## 🚀 功能特性

- ✅ **知识库管理**：支持 PDF、DOCX、TXT 文档上传，自动向量化存储
- ✅ **智能问答**：基于 RAG 技术，引用知识库内容回答问题
- ✅ **多用户多会话**：独立会话管理，历史记录持久化
- ✅ **用户认证**：注册登录、密码修改、JWT 认证
- ✅ **权限控制**：管理员专属知识库管理权限
- ✅ **流式响应**：实时流式输出 AI 回答
- ✅ **引用展示**：显示引用的知识库片段及相似度
- ✅ **企业级优化**：Redis 缓存、异步处理、API 限流

## 📦 技术栈

### 后端
- **框架**：FastAPI + Uvicorn
- **AI 框架**：LangChain + 阿里百炼（通义千问）
- **向量数据库**：Chroma
- **关系数据库**：PostgreSQL
- **缓存**：Redis
- **认证**：JWT + bcrypt

### 前端
- **框架**：Vue 3 + TypeScript + Vite
- **UI 组件**：Element Plus
- **状态管理**：Pinia
- **HTTP 客户端**：Axios

### 爬虫
- **框架**：Playwright
- **数据源**：拼多多商品信息

## 📂 项目结构

```
longChain_RAG/
├── backend/          # 后端服务
│   ├── app/
│   │   ├── api/      # API 路由
│   │   ├── models/   # 数据库模型
│   │   ├── schemas/  # 数据验证
│   │   ├── services/ # 业务逻辑
│   │   └── utils/    # 工具函数
│   └── requirements.txt
├── frontend/         # 前端项目
├── crawler/          # 爬虫模块
├── scripts/          # 脚本工具
├── data/             # 数据目录
│   ├── chroma_db/    # 向量数据库
│   └── uploads/      # 上传文档
└── docker-compose.yml
```

## 🛠️ 快速开始

### 1. 环境准备

**前置要求：**
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

### 2. 后端部署

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 复制环境变量配置
cp .env.example .env

# 编辑 .env 文件，填入你的配置：
# - DATABASE_URL：PostgreSQL 连接字符串
# - REDIS_URL：Redis 连接字符串
# - DASHSCOPE_API_KEY：阿里百炼 API Key
# - SECRET_KEY：JWT 密钥

# 初始化数据库
python ../scripts/init_db.py

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000/docs 查看 API 文档

### 3. 爬虫数据采集（可选）

```bash
# 进入爬虫目录
cd crawler

# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium

# 运行爬虫
python pdd_crawler.py

# 导入数据到向量库
cd ..
python scripts/import_products.py
```

### 4. 前端部署（下一步）

前端代码将在后续创建...

### 5. Docker 部署（推荐）

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 🔑 默认账户

- **管理员**：
  - 用户名：`admin`
  - 密码：`123456`
  - 权限：知识库管理、问答功能

## 📖 API 文档

启动后端服务后访问：
- Swagger UI：http://localhost:8000/docs
- ReDoc：http://localhost:8000/redoc

### 主要接口

**认证相关：**
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前用户信息
- `POST /api/auth/change-password` - 修改密码

**会话管理：**
- `POST /api/conversations` - 创建会话
- `GET /api/conversations` - 获取会话列表
- `GET /api/conversations/{id}/messages` - 获取历史消息
- `DELETE /api/conversations/{id}` - 删除会话

**问答：**
- `POST /api/chat/ask` - 流式问答（SSE）

**知识库管理（仅管理员）：**
- `POST /api/kb/upload` - 上传文档
- `GET /api/kb/documents` - 获取文档列表
- `DELETE /api/kb/documents/{id}` - 删除文档

## 🎯 使用说明

### 1. 注册登录
1. 访问前端页面
2. 注册普通用户账号或使用管理员账号登录

### 2. 知识库管理（管理员）
1. 登录管理员账号
2. 进入知识库管理页面
3. 上传 PDF/DOCX/TXT 文档
4. 系统自动分割文本并向量化

### 3. 智能问答
1. 创建新会话
2. 输入问题（例如："有什么蓝牙耳机推荐？"）
3. 系统检索相关商品信息并生成回答
4. 查看引用来源（点击展开查看原文片段）

## 🧪 测试数据

系统已内置模拟商品数据，包含：
- 手机（华为、小米、iPhone 等）
- 耳机（AirPods、索尼、华为等）
- 充电宝（小米、罗马仕、Anker 等）

## 📈 性能优化

- **缓存策略**：Redis 缓存用户会话和常见问题
- **异步处理**：所有 I/O 操作使用 async/await
- **流式响应**：LLM 输出实时推送，提升体验
- **向量检索**：Chroma HNSW 索引，快速相似度搜索
- **API 限流**：防止滥用，保护服务稳定性

## 🔧 配置说明

### LLM 模型配置

在 `.env` 文件中修改：

```env
# 模型选择（qwen-turbo/qwen-plus/qwen-max）
LLM_MODEL=qwen-plus

# 生成温度（0-1，越高越随机）
LLM_TEMPERATURE=0.7

# Embedding 模型
EMBEDDING_MODEL=text-embedding-v2
```

### RAG 参数调优

在 `backend/app/config.py` 中修改：

```python
# 文本分块大小
CHUNK_SIZE: int = 500

# 分块重叠
CHUNK_OVERLAP: int = 100

# 检索 Top-K
RETRIEVAL_TOP_K: int = 5
```

## 🐛 常见问题

### 1. 数据库连接失败
- 检查 PostgreSQL 是否启动
- 确认 DATABASE_URL 配置正确

### 2. Redis 连接失败
- 检查 Redis 是否启动
- 确认 REDIS_URL 配置正确

### 3. 阿里百炼 API 调用失败
- 检查 DASHSCOPE_API_KEY 是否正确
- 确认账户余额充足
- 查看 API 限流策略

### 4. 向量库为空
- 运行 `python scripts/import_products.py` 导入数据
- 或上传文档到知识库

## 📝 开发计划

- [ ] 前端界面开发
- [ ] 多知识库切换
- [ ] 问题推荐功能
- [ ] 答案评价系统
- [ ] 导出对话功能
- [ ] 管理员统计面板

## 📄 许可证

MIT License

## 👥 联系方式

如有问题或建议，欢迎提 Issue。

---

**毕业设计项目** - 基于 LangChain 的 RAG 企业级知识库问答系统

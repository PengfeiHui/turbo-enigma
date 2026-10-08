# 📁 项目目录导航

> 快速找到你需要的文档和文件

---

## 📖 文档目录

### 部署相关 (`docs/deployment/`)

| 文档 | 说明 | 适用场景 |
|------|------|----------|
| [DEPLOYMENT.md](docs/deployment/DEPLOYMENT.md) | 完整部署指南 | 详细了解部署架构和方案 |
| [QUICK_DEPLOY.md](docs/deployment/QUICK_DEPLOY.md) | 快速部署指南 | 云服务器快速部署 |
| [DOCKER_GUIDE.md](docs/deployment/DOCKER_GUIDE.md) | Docker 使用指南 | Docker 命令和故障排查 |
| [WINDOWS_START_GUIDE.md](docs/deployment/WINDOWS_START_GUIDE.md) | Windows 启动指南 | Windows 本地开发环境 |

### 开发指南 (`docs/guides/`)

| 文档 | 说明 | 适用场景 |
|------|------|----------|
| [IMPROVEMENT_SUGGESTIONS.md](docs/guides/IMPROVEMENT_SUGGESTIONS.md) | 改进建议 | 了解项目改进计划（15项） |
| [PROGRESS.md](docs/guides/PROGRESS.md) | 进度跟踪 | 查看当前开发进度 |
| [TEST_GUIDE.md](docs/guides/TEST_GUIDE.md) | 测试指南 | 测试新功能 |
| [SUMMARY.md](docs/guides/SUMMARY.md) | 改进总结 | 查看已完成的改进 |

---

## 🚀 脚本文件 (`scripts/`)

| 脚本 | 说明 | 使用方法 |
|------|------|----------|
| `deploy.sh` | 一键部署脚本（Linux） | `sudo ./scripts/deploy.sh` |
| `start-dev.bat` | 开发环境启动（Windows） | 双击运行 |
| `start-backend.bat` | 单独启动后端 | 双击运行 |
| `start-frontend.bat` | 单独启动前端 | 双击运行 |

---

## 📂 完整目录结构

```
longChain_RAG/
│
├── 📄 README.md                    # 项目说明（从这里开始）
├── 📄 PROJECT_REQUIREMENTS.md      # 项目需求文档
├── 📄 .env.example                 # 环境变量模板
├── 📄 .gitignore                   # Git 忽略配置
├── 📄 docker-compose.yml           # Docker 编排配置
│
├── 📁 backend/                     # 后端目录
│   ├── 📁 app/                     # 应用代码
│   │   ├── 📁 api/                 # API 路由
│   │   │   ├── auth.py            # 认证接口
│   │   │   ├── chat.py            # 对话接口
│   │   │   ├── conversation.py    # 会话管理
│   │   │   ├── knowledge_base.py  # 知识库管理
│   │   │   └── health.py          # 健康检查
│   │   ├── 📁 models/              # 数据库模型
│   │   │   ├── user.py
│   │   │   ├── conversation.py
│   │   │   ├── message.py
│   │   │   ├── knowledge_base.py
│   │   │   └── document.py
│   │   ├── 📁 schemas/             # Pydantic 模型
│   │   ├── 📁 services/            # 业务逻辑
│   │   │   ├── auth_service.py
│   │   │   ├── chat_service.py
│   │   │   ├── document_processor.py
│   │   │   ├── vector_store_service.py
│   │   │   └── embedding_service.py
│   │   └── 📁 utils/               # 工具函数
│   │       ├── text_splitter.py
│   │       └── logger.py          # 日志系统
│   ├── 📁 alembic/                 # 数据库迁移
│   ├── 📁 logs/                    # 日志文件
│   │   ├── app.log                # 所有日志
│   │   └── error.log              # 错误日志
│   ├── 📁 uploads/                 # 上传文件
│   ├── 📁 chroma_db/               # 向量数据库
│   ├── 📄 requirements.txt         # Python 依赖
│   ├── 📄 Dockerfile              # Docker 镜像配置
│   └── 📄 .env                    # 环境变量（不提交）
│
├── 📁 frontend/                    # 前端目录
│   ├── 📁 src/
│   │   ├── 📁 views/              # 页面组件
│   │   │   ├── Login.vue          # 登录页
│   │   │   ├── Dashboard.vue      # 仪表盘
│   │   │   ├── Chat.vue           # 对话页
│   │   │   └── KnowledgeBase.vue  # 知识库管理
│   │   ├── 📁 stores/             # 状态管理
│   │   │   ├── user.ts
│   │   │   └── chat.ts
│   │   ├── 📁 api/                # API 调用
│   │   │   ├── auth.ts
│   │   │   ├── chat.ts
│   │   │   └── kb.ts
│   │   ├── 📁 components/         # 公共组件
│   │   │   ├── SkeletonLoader.vue
│   │   │   └── GlobalLoading.vue
│   │   └── 📁 utils/              # 工具函数
│   │       └── request.ts         # HTTP 请求封装
│   ├── 📁 public/                 # 静态资源
│   ├── 📄 package.json            # 依赖配置
│   ├── 📄 vite.config.ts          # Vite 配置
│   ├── 📄 Dockerfile              # Docker 镜像配置
│   └── 📄 nginx.conf              # Nginx 配置
│
├── 📁 docs/                        # 📖 文档目录
│   ├── 📁 deployment/              # 部署文档
│   │   ├── DEPLOYMENT.md          # 完整部署指南
│   │   ├── QUICK_DEPLOY.md        # 快速部署
│   │   ├── DOCKER_GUIDE.md        # Docker 指南
│   │   └── WINDOWS_START_GUIDE.md # Windows 指南
│   └── 📁 guides/                  # 开发指南
│       ├── IMPROVEMENT_SUGGESTIONS.md  # 改进建议
│       ├── PROGRESS.md            # 进度跟踪
│       ├── TEST_GUIDE.md          # 测试指南
│       └── SUMMARY.md             # 改进总结
│
└── 📁 scripts/                     # 🚀 脚本文件
    ├── deploy.sh                  # 一键部署（Linux）
    ├── start-dev.bat              # 开发启动（Windows）
    ├── start-backend.bat          # 后端启动
    └── start-frontend.bat         # 前端启动
```

---

## 🎯 快速导航

### 我想...

#### 🚀 部署到服务器
→ [快速部署指南](docs/deployment/QUICK_DEPLOY.md)

#### 💻 本地开发
→ [Windows 启动指南](docs/deployment/WINDOWS_START_GUIDE.md)

#### 🐳 使用 Docker
→ [Docker 使用指南](docs/deployment/DOCKER_GUIDE.md)

#### 🧪 测试新功能
→ [测试指南](docs/guides/TEST_GUIDE.md)

#### 📊 查看改进进度
→ [进度跟踪](docs/guides/PROGRESS.md)

#### 💡 了解改进建议
→ [改进建议](docs/guides/IMPROVEMENT_SUGGESTIONS.md)

#### 📝 查看改进总结
→ [改进总结](docs/guides/SUMMARY.md)

---

## 📌 常用文件路径

### 配置文件
- 后端环境变量：`backend/.env`
- 前端配置：`frontend/.env`
- Docker 配置：`docker-compose.yml`

### 日志文件
- 应用日志：`backend/logs/app.log`
- 错误日志：`backend/logs/error.log`

### 数据存储
- 上传文件：`backend/uploads/`
- 向量数据库：`backend/chroma_db/`

---

## 🔗 外部链接

- **代码仓库**: https://gitee.com/huipengfei/long-chain_-rag
- **API 文档**: http://localhost:8000/docs (启动后访问)
- **前端地址**: http://localhost:5173 (开发环境)

---

## 💡 提示

1. **新手入门**：从 `README.md` 开始
2. **本地开发**：查看 `docs/deployment/WINDOWS_START_GUIDE.md`
3. **服务器部署**：查看 `docs/deployment/QUICK_DEPLOY.md`
4. **功能测试**：查看 `docs/guides/TEST_GUIDE.md`
5. **问题排查**：查看日志文件 `backend/logs/`

---

**目录更新日期**: 2024-10-08

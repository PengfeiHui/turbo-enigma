# 项目结构说明

```
longChain_RAG/
├── backend/                    # 后端服务 (FastAPI)
│   ├── app/
│   │   ├── api/               # API路由
│   │   ├── models/            # 数据库模型
│   │   ├── schemas/           # Pydantic模式
│   │   ├── services/          # 业务逻辑
│   │   └── utils/             # 工具函数
│   ├── .env.example           # 环境变量示例
│   ├── Dockerfile             # Docker构建文件
│   └── requirements.txt       # Python依赖
│
├── frontend/                   # 前端应用 (Vue 3 + TypeScript)
│   ├── src/
│   │   ├── api/               # API接口
│   │   ├── stores/            # Pinia状态管理
│   │   ├── views/             # 页面组件
│   │   └── router/            # 路由配置
│   └── package.json           # Node.js依赖
│
├── crawler/                    # 爬虫模块
│   ├── pdd_crawler.py         # 拼多多商品爬虫
│   └── requirements.txt       # 爬虫依赖
│
├── scripts/                    # 工具脚本
│   ├── init_db.py             # 数据库初始化
│   ├── generate_test_docs.py  # 生成测试文档
│   ├── test_*.py              # 各类测试脚本
│   └── check_vector_store.py  # 向量库检查
│
├── tests/                      # 测试资源
│   └── documents/             # 测试用的知识库文档
│
├── docs/                       # 项目文档
│   ├── zh/                    # 中文文档
│   │   ├── 安装指南.md
│   │   ├── 使用指南.md
│   │   └── 项目导航.md
│   ├── QUICKSTART.md          # 快速开始
│   ├── PROJECT_STATUS.md      # 项目状态
│   ├── TESTING.md             # 测试说明
│   └── SETUP_CHECKLIST.md     # 安装清单
│
├── data/                       # 数据目录
│   ├── chroma_db/             # 向量数据库
│   └── uploads/               # 上传文件
│
├── .claude/                    # Claude AI配置
│   └── memory/                # 项目记忆
│
├── docker-compose.yml          # Docker编排
├── PROJECT_REQUIREMENTS.md     # 项目需求文档
├── README.md                   # 项目主文档
│
└── 启动脚本 (Windows)
    ├── check-databases.bat     # 检查数据库状态
    ├── install-dependencies.bat # 安装依赖
    ├── start-backend.bat       # 启动后端
    └── start-frontend.bat      # 启动前端
```

## 主要目录说明

### backend/
后端服务，基于FastAPI框架构建，包含：
- RESTful API接口
- 数据库模型和Schema
- RAG核心业务逻辑
- 向量检索和LLM调用

### frontend/
前端应用，使用Vue 3 + TypeScript + Vite构建，提供：
- 用户登录注册界面
- 知识库管理界面
- 智能问答对话界面
- 会话历史管理

### scripts/
工具脚本集合，用于：
- 数据库初始化和测试
- 生成测试数据
- 系统功能测试
- 向量库状态检查

### tests/documents/
测试用的商品知识库文档，包含：
- 手机类商品信息
- 耳机类商品信息
- 充电宝类商品信息
- 键盘类商品信息

### docs/
项目文档，包含中英文说明文档

## 快速开始

1. **安装依赖**：双击 `install-dependencies.bat`
2. **检查数据库**：双击 `check-databases.bat`
3. **初始化数据库**：`python scripts/init_db.py`
4. **启动后端**：双击 `start-backend.bat`
5. **启动前端**：双击 `start-frontend.bat`
6. **访问应用**：http://localhost:5173

详细说明请查看 [README.md](../README.md)

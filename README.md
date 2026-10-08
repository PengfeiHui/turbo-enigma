# LongChain RAG 智能对话系统

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![Vue](https://img.shields.io/badge/vue-3.x-brightgreen.svg)
![FastAPI](https://img.shields.io/badge/fastapi-0.104+-blue.svg)

基于大语言模型和向量数据库的知识库问答系统

[在线演示](#) | [快速开始](#-快速开始) | [部署指南](QUICK_DEPLOY.md) | [文档](#-文档)

</div>

---

## ✨ 特性

- 🤖 **智能对话**：基于阿里云通义千问大模型，支持上下文理解和多轮对话
- 📚 **知识库管理**：支持上传 PDF、DOCX、TXT 文档，自动分块和向量化
- 🔍 **语义检索**：使用 Chroma 向量数据库，支持高效的相似度搜索
- 🎨 **现代化 UI**：全新设计的界面，摆脱 AI 味，品牌感强
- 📁 **文档分类**：支持创建文件夹，分类管理知识库文档
- 👥 **用户管理**：支持管理员和普通用户角色，权限分离
- 💬 **实时流式输出**：AI 回答实时显示，体验流畅
- 📖 **来源追溯**：展示答案的引用来源和相似度
- 🔐 **安全可靠**：JWT 认证，密码加密，防 SQL 注入

---

## 🏗️ 技术栈

### 后端
- **FastAPI** - 现代化的 Python Web 框架
- **LangChain** - LLM 应用开发框架
- **Chroma** - 向量数据库
- **PostgreSQL** - 关系型数据库
- **SQLAlchemy** - ORM 框架
- **Alembic** - 数据库迁移工具
- **DashScope** - 阿里云通义千问 API

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **TypeScript** - 类型安全的 JavaScript
- **Element Plus** - Vue 3 组件库
- **Vite** - 新一代前端构建工具
- **Pinia** - Vue 状态管理
- **Axios** - HTTP 客户端

### 部署
- **Docker** - 容器化部署
- **Docker Compose** - 多容器编排
- **Nginx** - 反向代理和静态文件服务

---

## 🚀 快速开始

### 前置要求

- Python 3.10+
- Node.js 18+
- PostgreSQL 15+
- Docker & Docker Compose（推荐）

### 方式一：Docker 部署（推荐）

```bash
# 1. 克隆项目
git clone https://gitee.com/your-username/longChain_RAG.git
cd longChain_RAG

# 2. 配置环境变量
cp .env.example .env
nano .env  # 填入你的 API Key 和密钥

# 3. 一键部署
chmod +x deploy.sh
sudo ./deploy.sh

# 4. 访问系统
# 浏览器打开：http://localhost
# 默认账号：admin / admin123456
```

### 方式二：本地开发

#### 后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
nano .env

# 初始化数据库
alembic upgrade head

# 启动后端
uvicorn app.main:app --reload
```

#### 前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问 `http://localhost:5173`

---

## 📖 文档

- [📁 目录导航](DIRECTORY.md) - 快速找到你需要的文档
- [🚀 快速部署指南](docs/deployment/QUICK_DEPLOY.md) - 云服务器部署步骤
- [📋 完整部署文档](docs/deployment/DEPLOYMENT.md) - 详细的部署说明
- [🐳 Docker 使用指南](docs/deployment/DOCKER_GUIDE.md) - Docker 命令和故障排查
- [💻 Windows 启动指南](docs/deployment/WINDOWS_START_GUIDE.md) - Windows 本地开发
- [🧪 测试指南](docs/guides/TEST_GUIDE.md) - 功能测试步骤
- [💡 改进建议](docs/guides/IMPROVEMENT_SUGGESTIONS.md) - 项目改进计划
- [📊 进度跟踪](docs/guides/PROGRESS.md) - 开发进度
- [📝 改进总结](docs/guides/SUMMARY.md) - 已完成的改进
- [📖 API 文档](http://localhost:8000/docs) - FastAPI 自动生成的 API 文档

---

## 📂 项目结构

```
longChain_RAG/
├── backend/                # 后端代码
│   ├── app/
│   │   ├── api/           # API 路由
│   │   ├── models/        # 数据库模型
│   │   ├── schemas/       # Pydantic 模型
│   │   ├── services/      # 业务逻辑
│   │   └── utils/         # 工具函数
│   ├── alembic/           # 数据库迁移
│   ├── logs/              # 日志文件
│   ├── uploads/           # 上传文件存储
│   └── chroma_db/         # 向量数据库
├── frontend/              # 前端代码
│   ├── src/
│   │   ├── views/        # 页面组件
│   │   ├── stores/       # 状态管理
│   │   ├── api/          # API 调用
│   │   ├── components/   # 公共组件
│   │   └── utils/        # 工具函数
│   └── public/           # 静态资源
├── docs/                  # 项目文档
│   ├── deployment/       # 部署相关文档
│   │   ├── DEPLOYMENT.md
│   │   ├── QUICK_DEPLOY.md
│   │   ├── DOCKER_GUIDE.md
│   │   └── WINDOWS_START_GUIDE.md
│   └── guides/           # 开发指南
│       ├── IMPROVEMENT_SUGGESTIONS.md
│       ├── PROGRESS.md
│       ├── TEST_GUIDE.md
│       └── SUMMARY.md
├── scripts/              # 脚本文件
│   ├── deploy.sh        # 一键部署脚本（Linux）
│   ├── start-dev.bat    # 开发环境启动（Windows）
│   ├── start-backend.bat
│   └── start-frontend.bat
├── docker-compose.yml    # Docker 编排配置
├── .env.example          # 环境变量模板
└── README.md             # 项目说明
```

---

## 🔧 配置说明

### 环境变量

```env
# 数据库
DATABASE_URL=postgresql://user:password@localhost:5432/longchain_rag

# API Keys
DASHSCOPE_API_KEY=your_api_key_here

# JWT
SECRET_KEY=your_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=43200

# 文件上传
MAX_UPLOAD_SIZE=10485760  # 10MB

# 向量数据库
CHROMA_PERSIST_DIR=./chroma_db
```

### 获取 DashScope API Key

1. 访问 [阿里云 DashScope](https://dashscope.console.aliyun.com/)
2. 注册/登录账号
3. 创建 API Key
4. 复制 Key 到 `.env` 文件

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！


## ⚠️ 注意事项

1. **API Key**：请妥善保管你的 DashScope API Key，不要泄露
2. **生产部署**：建议配置 SSL 证书，使用 HTTPS
3. **数据备份**：定期备份数据库和上传的文档
4. **安全加固**：修改默认密码，配置防火墙

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 💬 联系方式

- 作者：Pengfei Hui
- Email：3036209006@qq.com
- Gitee：https://gitee.com/huipengfei

---

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的 Python Web 框架
- [LangChain](https://www.langchain.com/) - LLM 应用开发框架
- [Vue.js](https://vuejs.org/) - 渐进式 JavaScript 框架
- [Element Plus](https://element-plus.org/) - Vue 3 组件库
- [Chroma](https://www.trychroma.com/) - 开源向量数据库
- [阿里云 DashScope](https://dashscope.aliyun.com/) - 通义千问 API

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐️ Star 支持一下！**

Made with ❤️ by [Your Name]

</div>

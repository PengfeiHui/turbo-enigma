# 📚 项目导航指南

## 🚀 快速入口

### 新用户
1. 📖 [README.md](../README.md) - 项目概述和主要信息
2. 📋 [快速开始指南](QUICKSTART.md) - 5分钟快速上手
3. 🔧 [安装清单](SETUP_CHECKLIST.md) - 逐步安装检查

### 中文用户
- 🇨🇳 [中文安装指南](zh/安装指南.md)
- 🇨🇳 [中文使用指南](zh/使用指南.md)
- 🇨🇳 [中文项目导航](zh/项目导航.md)

### 开发者
- 📁 [项目结构说明](PROJECT_STRUCTURE.md) - 目录结构详解
- 🧪 [测试文档](TESTING.md) - 如何测试项目
- 📊 [项目状态](PROJECT_STATUS.md) - 当前开发状态

---

## 📂 按功能查找

### 安装和配置
- **首次安装**：运行 `install-dependencies.bat`
- **数据库配置**：查看 [backend/.env.example](../backend/.env.example)
- **环境检查**：运行 `check-databases.bat`

### 启动项目
- **后端服务**：运行 `start-backend.bat` 或 `cd backend && uvicorn app.main:app --reload`
- **前端应用**：运行 `start-frontend.bat` 或 `cd frontend && npm run dev`
- **Docker方式**：`docker-compose up -d`

### 测试和调试
- **初始化数据库**：`python scripts/init_db.py`
- **生成测试数据**：`python scripts/generate_test_docs.py`
- **API测试**：`python scripts/test_api.py`
- **向量库检查**：`python scripts/check_vector_store.py`

### 知识库文档
- **测试文档位置**：[tests/documents/](../tests/documents/)
- **包含商品类型**：手机、耳机、充电宝、键盘等

---

## 🗂️ 核心目录

| 目录 | 说明 | 关键文件 |
|------|------|----------|
| `backend/` | FastAPI后端服务 | `main.py`, `requirements.txt` |
| `frontend/` | Vue3前端应用 | `package.json`, `src/` |
| `scripts/` | 工具脚本 | `init_db.py`, `test_*.py` |
| `docs/` | 项目文档 | 本目录的所有文档 |
| `tests/` | 测试资源 | `documents/` |
| `data/` | 运行时数据 | `chroma_db/`, `uploads/` |

---

## 🔍 常见问题快速查找

### 安装问题
- PostgreSQL未安装 → 查看 `check-databases.bat` 输出
- Python依赖安装失败 → 查看 [安装清单](SETUP_CHECKLIST.md)
- Node.js依赖问题 → 运行 `npm config set registry https://registry.npmmirror.com`

### 运行问题
- 后端启动失败 → 检查 `backend/.env` 配置
- 前端无法访问 → 确认后端服务已启动（http://localhost:8000）
- 数据库连接失败 → 确认PostgreSQL和Redis正在运行

### 功能问题
- 登录失败 → 默认账号 `admin/123456`
- 知识库上传失败 → 检查文件格式（支持.txt, .pdf, .docx）
- 问答无响应 → 检查阿里百炼API Key配置

---

## 📖 文档完整列表

### 英文文档
- [README.md](../README.md) - 项目主文档
- [QUICKSTART.md](QUICKSTART.md) - 快速开始
- [PROJECT_STATUS.md](PROJECT_STATUS.md) - 项目状态
- [TESTING.md](TESTING.md) - 测试说明
- [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) - 安装检查清单
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 项目结构
- [PROJECT_REQUIREMENTS.md](../PROJECT_REQUIREMENTS.md) - 原始需求

### 中文文档
- [安装指南.md](zh/安装指南.md)
- [使用指南.md](zh/使用指南.md)
- [项目导航.md](zh/项目导航.md)

---

## 🛠️ 开发工作流

```
1. 克隆项目
   ↓
2. 安装依赖 (install-dependencies.bat)
   ↓
3. 配置环境变量 (backend/.env)
   ↓
4. 启动数据库 (Docker或本地)
   ↓
5. 初始化数据库 (python scripts/init_db.py)
   ↓
6. 启动后端 (start-backend.bat)
   ↓
7. 启动前端 (start-frontend.bat)
   ↓
8. 访问应用 (http://localhost:5173)
```

---

## 📞 获取帮助

- 查看项目状态：[PROJECT_STATUS.md](PROJECT_STATUS.md)
- 查看测试说明：[TESTING.md](TESTING.md)
- 查看原始需求：[PROJECT_REQUIREMENTS.md](../PROJECT_REQUIREMENTS.md)

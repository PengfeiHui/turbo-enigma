# Claude Code 项目配置

本文件包含 Claude Code 的项目级配置。

## 项目信息

- **项目名称**: RAG 知识库问答系统
- **项目类型**: 全栈 Web 应用
- **主要语言**: Python, TypeScript
- **框架**: FastAPI, Vue 3

## 工作目录

- **后端**: `backend/`
- **前端**: `frontend/`
- **脚本**: `scripts/`
- **数据**: `data/`

## 代码规范

### Python (后端)
- PEP 8 风格
- 类型提示（Type Hints）
- Docstring 使用 Google 风格
- 异步函数优先（async/await）

### TypeScript (前端)
- ESLint 规则
- Vue 3 Composition API
- 函数式组件优先
- 明确的类型定义

## Git 忽略

已配置 `.gitignore`:
- `node_modules/`
- `__pycache__/`
- `.env` 文件
- `data/chroma_db/`（开发时）
- `data/uploads/`（开发时）

## 常用命令

### 开发
```bash
# 后端
cd backend && uvicorn app.main:app --reload

# 前端
cd frontend && npm run dev
```

### 测试
```bash
python scripts/test_all.py
```

### 部署
```bash
docker-compose up -d
```

## 文档位置

- **项目说明**: `README.md`
- **快速开始**: `QUICKSTART.md`, `开始使用.md`
- **项目导航**: `项目导航.md`
- **测试清单**: `TESTING.md`
- **项目状态**: `PROJECT_STATUS.md`

## 注意事项

- 所有敏感信息存储在 `.env` 文件中
- 不要提交 `.env` 到 Git
- 生产环境必须修改默认密码
- 定期备份数据库和向量库

---

**配置版本**: 1.0.0  
**最后更新**: 2026-09-22

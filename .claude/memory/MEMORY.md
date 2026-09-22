# Project Memory - 索引

这是项目记忆文件的索引。每个记忆文件记录特定类型的项目信息。

## 📋 记忆文件列表

- [project_overview.md](project_overview.md) — 项目整体架构、技术栈和完成状态
- [technical_decisions.md](technical_decisions.md) — 关键技术选型和架构决策
- [deployment_guide.md](deployment_guide.md) — 生产环境部署指南和配置清单
- [known_issues.md](known_issues.md) — 已知问题、Bug 修复记录和调试技巧

## 🎯 快速导航

### 想了解项目？
→ 查看 [project_overview.md](project_overview.md)

### 想知道为什么这样设计？
→ 查看 [technical_decisions.md](technical_decisions.md)

### 准备部署？
→ 查看 [deployment_guide.md](deployment_guide.md)

### 遇到问题？
→ 查看 [known_issues.md](known_issues.md)

## 📊 项目关键指标

- **总代码行数**: ~5,000+ 行
- **总文件数**: 60+ 个
- **完成度**: 100%
- **测试覆盖**: 19 个自动化测试
- **文档完整性**: 8 份详细文档

## 🔑 关键信息速查

### 默认账号
- 管理员: `admin` / `123456`

### 重要端口
- 后端: `8000`
- 前端: `5173`
- PostgreSQL: `5432`
- Redis: `6379`

### 环境要求
- Python: 3.10+
- Node.js: 20.x LTS
- PostgreSQL: 15+
- Redis: 7+

### 核心配置文件
- `backend/.env` - 后端环境变量
- `frontend/vite.config.ts` - 前端构建配置
- `docker-compose.yml` - Docker 编排
- `.claude/` - Claude Code 配置

---

**最后更新**: 2026-09-22  
**维护者**: Claude Code (Sonnet 4.6)

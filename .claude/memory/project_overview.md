---
name: project-overview
description: RAG 知识库问答系统的整体架构、技术栈和项目状态
metadata:
  type: project
---

这是一个完整的、企业级的 RAG（Retrieval-Augmented Generation）知识库问答系统。

**Why:** 为毕业设计项目，展示现代全栈开发能力和 AI 应用集成能力。

**How to apply:** 当需要理解整体架构、技术选型、或项目状态时参考。

## 技术架构

**后端**: FastAPI + LangChain + 阿里百炼 + Chroma 向量库  
**前端**: Vue 3 + TypeScript + Element Plus + Pinia  
**数据库**: PostgreSQL（关系数据） + Redis（缓存） + Chroma（向量）  
**部署**: Docker Compose

## 核心功能

1. **用户认证**: JWT Token + 角色权限控制
2. **智能问答**: 基于向量检索的 RAG 问答 + 流式输出
3. **会话管理**: 多会话支持 + 历史记忆（最近 10 条消息）
4. **知识库管理**: 文档上传（PDF/DOCX/TXT）+ 批量处理 + 自动向量化
5. **引用展示**: 显示答案来源和相似度分数

## 项目规模

- **代码文件**: 60+ 个
- **代码行数**: 约 5,000+ 行
- **后端模块**: 30+ 个 Python 文件
- **前端组件**: 20+ 个 TypeScript/Vue 文件
- **API 接口**: 15+ 个
- **数据库表**: 5 个

## 开发状态

- ✅ 后端 API 开发 (100%)
- ✅ 前端界面开发 (100%)
- ✅ 数据采集爬虫 (100%)
- ✅ 部署配置 (100%)
- ✅ 项目文档 (100%)

**总体进度**: 100% 完成

---
name: known-issues
description: 已知问题、Bug 和解决方案
metadata:
  type: feedback
---

记录项目开发过程中遇到的问题和解决方案。

**Why:** 避免重复遇到相同问题，快速定位和解决 Bug。

**How to apply:** 遇到问题时先查看是否已有解决方案。

## 已修复的问题

### 1. 流式输出只显示前几个字 ✅
**症状**: AI 回答只显示"你好"等前几个字就停止

**原因**: LangChain 对阿里百炼的封装有版本兼容问题，流式输出中途报错：
```
Additional kwargs key output_tokens already exists in left dict
```

**解决方案**: 改用阿里百炼原生 SDK（dashscope）
- 文件: `backend/app/services/llm_service.py`
- 直接调用 `dashscope.Generation.call()`
- 设置 `stream=True, incremental_output=True`

---

### 2. POST 请求返回 405 Method Not Allowed ✅
**症状**: 前端发送问题时报错 405

**原因**: 前端使用 `EventSource` 只支持 GET 请求，但后端 API 是 POST

**解决方案**: 使用 fetch API + ReadableStream 手动处理 SSE
- 文件: `frontend/src/api/chat.ts`
- 改用 `fetch()` 发送 POST 请求
- 手动解析 SSE 数据流
- 添加缓冲区处理不完整的数据块

---

### 3. bcrypt 密码哈希失败 ✅
**症状**: 初始化数据库时报错 `password cannot be longer than 72 bytes`

**原因**: bcrypt 版本冲突，旧版本有 Bug

**解决方案**:
- 固定 bcrypt 版本为 4.1.2
- 添加密码长度检查（截断到 72 字节）
- 添加错误处理和备用方案（hashlib）
- 文件: `backend/app/utils/security.py`

---

### 4. Node.js v24 依赖安装失败 ✅
**症状**: `npm install` 报 esbuild 错误

**原因**: Node.js v24 太新，部分包不兼容

**解决方案**:
- 降级包版本使用稳定版本
- 更新 `package.json` 使用兼容的版本号
- 建议使用 Node.js 20.x LTS

---

### 5. 无会话记忆功能 ✅
**症状**: AI 无法记住之前的对话内容

**原因**: RAG 服务没有加载历史消息

**解决方案**:
- 查询最近 10 条历史消息
- 构建历史对话文本
- 添加到 Prompt 中
- 文件: `backend/app/services/rag_service.py`

---

### 6. 无法批量上传文档 ✅
**症状**: 一次只能上传一个文件

**原因**: Upload 组件 `limit="1"`

**解决方案**:
- 设置 `limit="20"` 和 `multiple`
- 修改上传逻辑支持数组
- 添加进度显示
- 文件: `frontend/src/views/KnowledgeBase.vue`

---

## 当前已知问题

### 1. 向量库检索精度
**症状**: 有时检索结果不够相关

**临时方案**: 
- 调整 `RETRIEVAL_TOP_K` 参数
- 优化文档分割策略
- 改进 Embedding 模型

**长期方案**:
- 使用更好的 Embedding 模型
- 添加混合检索（BM25 + 向量）
- 实现重排序（Rerank）

---

### 2. 长文档处理慢
**症状**: 上传大文档时处理时间长

**临时方案**:
- 限制文件大小为 10MB
- 提示用户耐心等待

**长期方案**:
- 异步处理文档
- 添加后台任务队列（Celery）
- 显示处理进度

---

### 3. 会话数量无限制
**症状**: 用户可以创建无限多会话

**临时方案**: 无

**长期方案**:
- 限制每个用户最多 50 个会话
- 自动清理长时间未使用的会话
- 添加归档功能

---

## 边界情况注意事项

### 特殊字符处理
- ✅ Emoji 正常显示
- ✅ HTML 标签被转义（防 XSS）
- ✅ 换行符正常处理
- ⚠️ 某些特殊 Unicode 字符可能显示异常

### 并发请求
- ✅ 支持多用户并发
- ✅ 流式输出互不干扰
- ⚠️ 高并发下可能需要限流

### 大数据量
- ✅ 100+ 条消息的会话正常显示
- ✅ 20+ 个会话列表正常
- ⚠️ 10000+ 文档时检索可能变慢

---

## 调试技巧

### 后端调试
```bash
# 查看详细日志
uvicorn app.main:app --reload --log-level debug

# 测试单个功能
python scripts/test_all.py

# 检查向量库状态
python scripts/check_vector_store.py
```

### 前端调试
1. 打开浏览器开发者工具（F12）
2. Console 标签查看 JavaScript 错误
3. Network 标签查看 API 请求
4. Vue DevTools 查看组件状态

### 数据库调试
```bash
# 连接数据库
psql -U raguser -d rag_db

# 查看表
\dt

# 查询数据
SELECT * FROM users;
SELECT * FROM conversations;
```

---

**维护建议**: 定期更新此文档，记录新发现的问题和解决方案

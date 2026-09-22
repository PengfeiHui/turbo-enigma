---
name: technical-decisions
description: 关键技术决策和选型理由
metadata:
  type: project
---

记录项目中的重要技术决策及其原因。

**Why:** 避免重复讨论已解决的技术选型问题，保持技术栈一致性。

**How to apply:** 当考虑修改技术栈或添加新依赖时，先查看这些决策。

## 后端技术选型

### FastAPI over Flask/Django
**决策**: 使用 FastAPI 作为后端框架  
**原因**:
- 原生异步支持，适合流式 SSE
- 自动生成 API 文档（/docs）
- 类型提示和数据验证（Pydantic）
- 性能优秀

### LangChain 框架
**决策**: 使用 LangChain 构建 RAG 流程  
**原因**:
- 成熟的 RAG 工具链
- 丰富的向量库集成
- 社区活跃，文档完善

### 阿里百炼大模型
**决策**: 使用通义千问（Qwen Plus）  
**原因**:
- 中文支持优秀
- API 稳定可靠
- 价格合理
- 用户已有 API Key

### Chroma 向量数据库
**决策**: 使用 Chroma 作为向量存储  
**原因**:
- 轻量级，易于部署
- 本地持久化
- Python 原生支持
- 无需额外服务（如 Milvus、Pinecone）

## 前端技术选型

### Vue 3 over React
**决策**: 使用 Vue 3 + Composition API  
**原因**:
- 学习曲线平缓
- 响应式系统简洁
- TypeScript 支持良好
- 中文文档完善

### Element Plus UI 库
**决策**: 使用 Element Plus 组件库  
**原因**:
- 企业级组件完整
- 中文文档和示例
- Vue 3 原生支持
- 设计美观

### Pinia 状态管理
**决策**: 使用 Pinia 替代 Vuex  
**原因**:
- Vue 3 官方推荐
- TypeScript 支持更好
- API 更简洁
- 模块化设计

## 架构决策

### 流式 SSE over WebSocket
**决策**: 使用 Server-Sent Events 实现流式输出  
**原因**:
- 单向通信足够（服务器 → 客户端）
- 协议简单，易于实现
- HTTP 协议，部署友好
- 自动重连机制

**注意**: 修复了 EventSource 只支持 GET 的问题，改用 fetch API + ReadableStream

### 会话记忆策略
**决策**: 保留最近 10 条消息（5 轮对话）  
**原因**:
- 平衡上下文理解和 Token 成本
- 避免上下文过长导致响应慢
- 10 条消息足够理解近期对话

### 向量检索 Top-K
**决策**: 默认检索 Top 5 相关文档  
**原因**:
- 5 个文档能提供足够上下文
- 避免 Prompt 过长
- 保持响应速度

## 修复的关键问题

### 1. LangChain 版本兼容问题
**问题**: `Additional kwargs key output_tokens already exists`  
**解决**: 改用阿里百炼原生 SDK（dashscope）替代 LangChain 封装  
**原因**: LangChain 对阿里百炼的封装有版本兼容问题

### 2. SSE 流式传输问题
**问题**: EventSource 只支持 GET，但 API 是 POST  
**解决**: 使用 fetch API + ReadableStream 手动处理 SSE  
**实现**: 添加缓冲区处理不完整的数据块

### 3. bcrypt 密码哈希问题
**问题**: bcrypt 版本冲突导致密码哈希失败  
**解决**: 
- 添加错误处理和备用方案
- 确保密码长度不超过 72 字节
- 固定 bcrypt 版本为 4.1.2

### 4. 前端 Node.js 版本问题
**问题**: Node.js v24 太新，esbuild 不兼容  
**解决**: 降级包版本，使用稳定的依赖版本

## 未来优化方向

### 性能优化
- [ ] Redis 缓存常见问题答案
- [ ] 向量检索结果缓存
- [ ] API 请求限流
- [ ] 数据库查询优化

### 功能扩展
- [ ] 多知识库切换
- [ ] 对话导出功能
- [ ] 问题推荐
- [ ] 答案评价系统
- [ ] 管理员统计面板

### 用户体验
- [ ] 深色模式
- [ ] 语音输入/输出
- [ ] 图片上传识别
- [ ] 移动端优化

---

**原则**: 优先稳定性和可维护性，避免过度工程化

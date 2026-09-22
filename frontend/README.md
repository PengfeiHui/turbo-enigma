# RAG 知识库问答系统 - 前端

基于 Vue 3 + TypeScript + Element Plus 的前端应用。

## 技术栈

- Vue 3 - 渐进式 JavaScript 框架
- TypeScript - 类型安全
- Vite - 快速构建工具
- Element Plus - UI 组件库
- Pinia - 状态管理
- Vue Router - 路由管理
- Axios - HTTP 客户端

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:5173

### 3. 构建生产版本

```bash
npm run build
```

## 功能特性

- ✅ 用户注册登录
- ✅ 多会话管理
- ✅ 流式问答体验
- ✅ 引用来源展示
- ✅ 知识库管理（管理员）
- ✅ Markdown 渲染
- ✅ 响应式设计

## 项目结构

```
frontend/
├── src/
│   ├── api/          # API 调用
│   ├── assets/       # 静态资源
│   ├── components/   # 通用组件
│   ├── router/       # 路由配置
│   ├── stores/       # Pinia 状态管理
│   ├── utils/        # 工具函数
│   ├── views/        # 页面组件
│   ├── App.vue       # 根组件
│   └── main.ts       # 入口文件
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## API 代理配置

开发环境下，API 请求会被代理到后端服务：

```typescript
// vite.config.ts
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

## 环境变量

创建 `.env` 文件配置 API 基础地址：

```
VITE_API_BASE_URL=/api
```

## 默认账号

- 管理员：admin / 123456
- 普通用户：注册后使用

## License

MIT

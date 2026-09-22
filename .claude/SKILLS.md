# Claude Code Skills & Agents

本文档记录项目中可用的 Skills 和 Agents 配置。

## Skills

### 测试相关

#### `/test-all`
运行完整的后端测试套件
实现: `scripts/test_all.py`

#### `/test-api`
测试阿里百炼 API 连接
实现: `scripts/test_dashscope_api.py`

### 数据库相关

#### `/init-db`
初始化数据库表和管理员账户
实现: `scripts/init_db.py`

#### `/check-vector`
检查向量库状态
实现: `scripts/check_vector_store.py`

### 知识库相关

#### `/generate-docs`
生成测试文档
实现: `scripts/generate_test_docs.py`

#### `/import-products`
导入商品数据到向量库
实现: `scripts/import_products.py`

### 安装和配置

#### `/install-deps`
自动安装所有依赖
实现: `install-dependencies.bat`

## Agents

### Explore Agent
用途: 代码搜索和探索

### Plan Agent
用途: 设计实现方案

### General Purpose Agent
用途: 多步骤复杂任务

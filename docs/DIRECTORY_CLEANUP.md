# 🗂️ 目录整理说明

本项目已完成目录结构优化，现在结构更加清晰和易于维护。

## ✅ 已完成的整理

### 1. 文档归档
- **英文文档** → `docs/` 目录
  - QUICKSTART.md
  - PROJECT_STATUS.md
  - TESTING.md
  - SETUP_CHECKLIST.md
  - FINAL_SUMMARY.md
  
- **中文文档** → `docs/zh/` 目录
  - 安装指南.md
  - 使用指南.md
  - 项目导航.md

- **新增文档**
  - docs/PROJECT_STRUCTURE.md - 详细的项目结构说明
  - docs/NAVIGATION.md - 文档导航指南

### 2. 测试资源归档
- `test_documents/` → `tests/documents/`
- 包含18个测试商品文档（手机、耳机、充电宝、键盘）

### 3. 需求文档重命名
- `require.txt` → `PROJECT_REQUIREMENTS.md`
- 原始项目需求文档，保留作为参考

### 4. 脚本路径更新
- 更新了 `check-databases.bat` 中的硬编码路径
- 更新了 `scripts/generate_test_docs.py` 的输出路径

### 5. 清理临时文件
- 删除了 `backend/` 下的所有 `__pycache__` 缓存目录

## 📁 当前根目录结构

```
longChain_RAG/
├── 📄 README.md                    # 项目主文档
├── 📄 PROJECT_REQUIREMENTS.md      # 原始需求文档
├── 📄 docker-compose.yml           # Docker编排配置
├── 📄 .gitignore                   # Git忽略规则
│
├── 🗂️ backend/                     # 后端服务
├── 🗂️ frontend/                    # 前端应用
├── 🗂️ crawler/                     # 爬虫模块
├── 🗂️ scripts/                     # 工具脚本
├── 🗂️ tests/                       # 测试资源
├── 🗂️ docs/                        # 项目文档
├── 🗂️ data/                        # 运行时数据
│
└── 🔧 启动脚本
    ├── check-databases.bat         # 检查数据库状态
    ├── install-dependencies.bat    # 安装所有依赖
    ├── start-backend.bat           # 启动后端
    └── start-frontend.bat          # 启动前端
```

## 🎯 整理原则

1. **根目录简洁**：只保留必要的README、配置文件和启动脚本
2. **文档集中**：所有文档统一放在 `docs/` 目录
3. **测试隔离**：测试资源放在 `tests/` 目录
4. **路径兼容**：保持相对路径引用，不影响项目运行
5. **语言分离**：中英文文档分别存放

## ⚠️ 重要提示

### 不受影响的功能
✅ 所有启动脚本仍可正常使用  
✅ Python脚本路径已更新  
✅ 测试文档路径已更新  
✅ Git历史完整保留（使用git mv）

### 需要注意
- 生成测试文档现在会输出到 `tests/documents/`
- 原有的 `.env` 文件已在 `.gitignore` 中（不会被提交）
- 所有 `__pycache__` 目录会被自动忽略

## 📖 快速查找文档

- **想要快速开始？** → [docs/QUICKSTART.md](QUICKSTART.md)
- **查看项目结构？** → [docs/PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- **找不到文档？** → [docs/NAVIGATION.md](NAVIGATION.md)
- **需要中文说明？** → [docs/zh/](zh/)

## 🔄 Git 提交说明

本次整理通过 `git mv` 命令完成，保留了完整的文件历史。  
所有变更已暂存，等待提交。

```bash
# 查看变更
git status

# 提交整理
git commit -m "重构: 整理项目目录结构"
```

---

**整理完成时间**: 2024-09-22  
**影响范围**: 目录结构优化，功能完全兼容

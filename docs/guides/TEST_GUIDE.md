# 本地测试新功能指南

## ✅ 测试清单

### 已完成的改进功能测试

#### 1. 健康检查接口 ✅
**测试步骤**:
```bash
# 启动后端后访问
http://localhost:8000/api/health

# 应该返回：
{
  "status": "healthy",
  "service": "longchain-rag",
  "version": "1.0.0"
}
```

#### 2. 统一错误处理 ✅
**测试步骤**:
- 尝试用错误的账号密码登录
- 尝试访问不存在的页面
- 尝试上传超大文件
- 观察错误提示是否友好

**预期结果**:
- 400 错误：显示"请求参数错误"
- 401 错误：跳转到登录页
- 404 错误：显示"请求的资源不存在"
- 422 错误：显示表单验证错误
- 500 错误：显示"服务器内部错误"

#### 3. 向量库缓存 ✅
**测试步骤**:
1. 在对话中提问一个问题（如"介绍一下华为 Mate 60 Pro"）
2. 查看后端控制台，应该显示"⚡ 执行向量查询"
3. 再次提问相同的问题
4. 查看后端控制台，应该显示"✓ 缓存命中"

**预期结果**:
- 第一次查询：执行向量搜索
- 第二次查询：从缓存读取，速度明显加快

#### 4. 骨架屏加载 ✅
**测试步骤**:
1. 访问 Dashboard 页面
2. 刷新页面
3. 观察"最近对话"部分

**预期结果**:
- 加载时显示灰色骨架屏动画
- 数据加载完成后显示真实内容

#### 5. 日志系统 ✅
**测试步骤**:
1. 启动后端
2. 进行一些操作（登录、对话、上传文档）
3. 检查日志文件

**预期结果**:
```bash
# 查看日志
cd backend/logs
cat app.log     # 所有日志
cat error.log   # 错误日志

# 日志应该包含：
- API 请求日志
- 响应时间
- 缓存命中情况
- 错误信息（如果有）
```

---

## 🚀 启动步骤

### 方法 1：使用启动脚本（推荐）

创建一个启动脚本：

**`start-dev.bat`** (Windows):
```batch
@echo off
echo ========================================
echo  启动 LongChain RAG 开发环境
echo ========================================

REM 启动后端
echo.
echo [1/2] 启动后端服务...
cd backend
start "后端服务" cmd /k "venv\Scripts\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM 等待后端启动
timeout /t 5 /nobreak

REM 启动前端
echo.
echo [2/2] 启动前端服务...
cd ..\frontend
start "前端服务" cmd /k "npm run dev"

echo.
echo ========================================
echo  服务启动完成！
echo ========================================
echo.
echo  前端地址: http://localhost:5173
echo  后端地址: http://localhost:8000
echo  API 文档: http://localhost:8000/docs
echo.
echo  按任意键退出...
pause > nul
```

**使用方法**:
```bash
# 双击 start-dev.bat 即可启动
```

### 方法 2：手动启动

#### 启动后端
```bash
# 1. 打开终端
cd d:\code\projects\longChain_RAG\backend

# 2. 激活虚拟环境
venv\Scripts\activate

# 3. 启动后端
uvicorn app.main:app --reload
```

#### 启动前端（新开一个终端）
```bash
# 1. 打开新终端
cd d:\code\projects\longChain_RAG\frontend

# 2. 启动前端
npm run dev
```

---

## 🧪 功能测试脚本

### 测试 1：健康检查

```bash
# 使用 curl 或浏览器访问
curl http://localhost:8000/api/health
```

### 测试 2：缓存效果

```python
# test_cache.py
import requests
import time

API_URL = "http://localhost:8000/api/chat/ask"
TOKEN = "你的_JWT_Token"  # 登录后获取

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "conversation_id": 1,
    "question": "介绍一下华为 Mate 60 Pro"
}

# 第一次查询
print("第一次查询...")
start = time.time()
response1 = requests.post(API_URL, json=data, headers=headers)
time1 = time.time() - start
print(f"耗时: {time1:.3f}秒")

# 第二次查询（应该命中缓存）
print("\n第二次查询...")
start = time.time()
response2 = requests.post(API_URL, json=data, headers=headers)
time2 = time.time() - start
print(f"耗时: {time2:.3f}秒")

print(f"\n性能提升: {((time1 - time2) / time1 * 100):.1f}%")
```

### 测试 3：日志记录

```bash
# 查看实时日志
cd backend/logs
tail -f app.log

# 然后在另一个终端进行操作，观察日志输出
```

---

## 📊 性能对比

### 预期改进效果

| 功能 | 改进前 | 改进后 | 提升 |
|------|--------|--------|------|
| 重复查询响应时间 | ~2-3秒 | ~0.1-0.3秒 | 80%+ |
| 错误提示清晰度 | 模糊 | 清晰 | ✅ |
| 页面加载体验 | 空白 | 骨架屏 | ✅ |
| 问题排查效率 | 困难 | 日志完整 | ✅ |

---

## 🐛 测试问题场景

### 场景 1：测试错误处理
```bash
# 1. 错误的登录信息
用户名: wronguser
密码: wrongpass
预期: 显示"用户名或密码错误"

# 2. 访问不存在的 API
http://localhost:8000/api/nonexistent
预期: 显示"请求的资源不存在"

# 3. 上传过大文件
选择 > 10MB 的文件
预期: 显示"文件大小超过限制"
```

### 场景 2：测试缓存
```bash
# 1. 提问："华为 Mate 60 Pro 有哪些特点？"
# 2. 查看后端日志：应显示"执行向量查询"
# 3. 再次提问相同问题
# 4. 查看后端日志：应显示"缓存命中"
# 5. 对比响应时间
```

### 场景 3：测试加载状态
```bash
# 1. 清空浏览器缓存（Ctrl+Shift+Delete）
# 2. 访问 http://localhost:5173
# 3. 登录后进入 Dashboard
# 4. 观察"最近对话"区域
# 5. 应该看到骨架屏动画（灰色闪烁）
```

---

## 📝 测试报告模板

```markdown
## 功能测试报告

**测试日期**: 2024-XX-XX
**测试人员**: XXX

### 1. 健康检查接口
- [ ] 接口正常响应
- [ ] 返回正确的状态信息
- 备注: _______________

### 2. 错误处理
- [ ] 400 错误提示正确
- [ ] 401 自动跳转登录
- [ ] 404 提示清晰
- [ ] 500 错误友好提示
- 备注: _______________

### 3. 缓存功能
- [ ] 第一次查询正常
- [ ] 第二次命中缓存
- [ ] 性能提升明显 (提升 ___%)
- 备注: _______________

### 4. 加载状态
- [ ] 骨架屏正常显示
- [ ] 加载动画流畅
- [ ] 数据加载后正确显示
- 备注: _______________

### 5. 日志系统
- [ ] 日志文件正常生成
- [ ] API 请求被记录
- [ ] 错误被正确记录
- [ ] 日志格式规范
- 备注: _______________

### 总体评价
- 功能完整性: ⭐⭐⭐⭐⭐
- 性能表现: ⭐⭐⭐⭐⭐
- 用户体验: ⭐⭐⭐⭐⭐
```

---

## 💡 测试技巧

1. **使用开发者工具**
   - F12 打开开发者工具
   - Network 标签查看请求
   - Console 标签查看前端日志

2. **观察后端日志**
   - 实时查看 `tail -f backend/logs/app.log`
   - 关注缓存命中情况

3. **性能对比**
   - 使用浏览器 Performance 工具
   - 记录加载时间
   - 对比改进前后

4. **边界测试**
   - 测试极端情况
   - 测试错误场景
   - 测试并发情况

---

## ✅ 测试完成后

### 确认清单
- [ ] 所有新功能都已测试
- [ ] 没有发现严重 Bug
- [ ] 性能提升符合预期
- [ ] 用户体验良好
- [ ] 准备部署到生产环境

### 下一步
- 提交测试报告
- 修复发现的问题
- 准备部署
- 编写用户文档

---

**开始测试吧！** 🚀

如果遇到问题，随时告诉我！
```

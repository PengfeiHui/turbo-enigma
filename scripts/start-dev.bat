@echo off
chcp 65001 >nul
echo ========================================
echo  LongChain RAG 开发环境启动
echo ========================================
echo.

REM 启动后端
echo [1/2] 启动后端服务...
cd backend
if not exist venv (
    echo 虚拟环境不存在，正在创建...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

echo 后端启动中...
start "LongChain 后端" cmd /k "cd /d %~dp0backend && venv\Scripts\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM 等待后端启动
echo 等待后端启动...
timeout /t 5 /nobreak >nul

REM 启动前端
echo.
echo [2/2] 启动前端服务...
cd ..\frontend
start "LongChain 前端" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================
echo  🎉 服务启动完成！
echo ========================================
echo.
echo  📱 前端地址: http://localhost:5173
echo  🔧 后端地址: http://localhost:8000
echo  📖 API 文档: http://localhost:8000/docs
echo  💚 健康检查: http://localhost:8000/api/health
echo.
echo ========================================
echo  测试功能:
echo ========================================
echo  1. 健康检查 - 访问 /api/health
echo  2. 缓存测试 - 提问两次相同问题
echo  3. 错误处理 - 尝试错误操作
echo  4. 加载状态 - 刷新 Dashboard
echo  5. 日志查看 - backend/logs/app.log
echo.
echo  按任意键关闭此窗口...
pause >nul

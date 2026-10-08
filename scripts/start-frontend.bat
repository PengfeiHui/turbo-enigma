@echo off
chcp 65001 >nul
echo ====================================
echo RAG 知识库问答系统 - 前端启动脚本
echo ====================================
echo.

cd /d "%~dp0frontend"

echo [1/3] 检查 Node.js...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js 未安装，请先安装 Node.js
    echo 下载地址: https://nodejs.org/
    pause
    exit /b 1
)
node --version
echo.

echo [2/3] 检查依赖...
if not exist "node_modules\" (
    echo 📦 首次运行，正在安装依赖...
    echo 这可能需要几分钟时间，请耐心等待...
    call npm install
    if %errorlevel% neq 0 (
        echo.
        echo ❌ 依赖安装失败，请检查网络连接
        echo 💡 提示：可以尝试使用国内镜像:
        echo    npm config set registry https://registry.npmmirror.com
        pause
        exit /b 1
    )
    echo ✅ 依赖安装完成
    echo.
) else (
    echo ✅ 依赖已存在
    echo.
)

echo [3/3] 启动开发服务器...
echo.
echo 🚀 前端服务启动中...
echo 📍 访问地址: http://localhost:5173
echo.
echo 💡 提示:
echo    - 确保后端服务已启动 (http://localhost:8000)
echo    - 使用 Ctrl+C 停止服务
echo.
echo ====================================
echo.

npm run dev

pause

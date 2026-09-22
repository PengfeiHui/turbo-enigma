@echo off
chcp 65001 >nul
echo ====================================
echo RAG 知识库问答系统 - 后端启动脚本
echo ====================================
echo.

cd /d "%~dp0backend"

echo [1/4] 检查 Python...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 未安装，请先安装 Python 3.10+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo.

echo [2/4] 检查依赖...
python -c "import fastapi" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 首次运行，正在安装依赖...
    echo 这可能需要几分钟时间，请耐心等待...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo.
        echo ❌ 依赖安装失败
        echo 💡 提示：可以尝试使用国内镜像:
        echo    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
        pause
        exit /b 1
    )
    echo ✅ 依赖安装完成
    echo.
) else (
    echo ✅ 依赖已存在
    echo.
)

echo [3/4] 检查环境配置...
if not exist ".env" (
    echo ⚠️  警告: .env 文件不存在
    echo 💡 请先配置 .env 文件:
    echo    1. 复制 .env.example 为 .env
    echo    2. 填入阿里百炼 API Key
    echo.
    pause
    exit /b 1
)
echo ✅ 环境配置文件存在
echo.

echo [4/4] 启动后端服务...
echo.
echo 🚀 后端服务启动中...
echo 📍 API 文档: http://localhost:8000/docs
echo 📍 健康检查: http://localhost:8000/health
echo.
echo 💡 提示:
echo    - 确保 PostgreSQL 和 Redis 已启动
echo    - 首次运行请先执行: python ../scripts/init_db.py
echo    - 使用 Ctrl+C 停止服务
echo.
echo ====================================
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause

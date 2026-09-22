@echo off
chcp 65001 >nul
echo ========================================
echo RAG 知识库问答系统 - 依赖安装脚本
echo ========================================
echo.

cd /d "%~dp0"

echo [步骤 1/5] 检查 Python 环境...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 未安装
    echo.
    echo 请先安装 Python 3.10 或更高版本
    echo 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
python --version
echo ✅ Python 已安装
echo.

echo [步骤 2/5] 安装后端依赖...
cd backend
echo 📦 正在安装 Python 包（这可能需要几分钟）...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  使用默认源重试...
    pip install -r requirements.txt
)
echo ✅ 后端依赖安装完成
echo.

cd ..

echo [步骤 3/5] 检查 Node.js 环境...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js 未安装
    echo.
    echo 请先安装 Node.js (LTS 版本)
    echo 下载地址: https://nodejs.org/
    echo.
    echo 安装完成后，重新运行此脚本
    pause
    exit /b 1
)
node --version
npm --version
echo ✅ Node.js 已安装
echo.

echo [步骤 4/5] 安装前端依赖...
cd frontend
echo 📦 设置 npm 国内镜像...
call npm config set registry https://registry.npmmirror.com
echo 📦 正在安装前端依赖（这可能需要几分钟）...
call npm install
if %errorlevel% neq 0 (
    echo.
    echo ❌ 前端依赖安装失败
    echo 💡 请检查网络连接后重试
    pause
    exit /b 1
)
echo ✅ 前端依赖安装完成
echo.

cd ..

echo [步骤 5/5] 安装爬虫依赖（可选）...
cd crawler
echo 📦 正在安装爬虫依赖...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if %errorlevel% neq 0 (
    pip install -r requirements.txt
)
echo 📦 正在安装 Playwright 浏览器...
playwright install chromium
echo ✅ 爬虫依赖安装完成
echo.

cd ..

echo ========================================
echo ✅ 所有依赖安装完成！
echo ========================================
echo.
echo 📋 下一步操作:
echo.
echo 1. 确保 PostgreSQL 和 Redis 已启动
echo    - 如果使用 Docker: docker-compose up -d postgres redis
echo    - 如果本地安装: 手动启动服务
echo.
echo 2. 初始化数据库（首次运行）
echo    python scripts\init_db.py
echo.
echo 3. 启动后端
echo    双击: start-backend.bat
echo.
echo 4. 启动前端
echo    双击: start-frontend.bat
echo.
echo 5. 访问应用
echo    http://localhost:5173
echo    用户名: admin
echo    密码: 123456
echo.
echo ========================================
pause

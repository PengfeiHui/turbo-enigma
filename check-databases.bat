@echo off
chcp 65001 >nul
echo ========================================
echo 数据库和 Redis 安装检查
echo ========================================
echo.

echo [检查 1] PostgreSQL 状态...
echo.

REM 检查 PostgreSQL 服务
sc query postgresql-x64-15 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ PostgreSQL 服务已安装
    sc query postgresql-x64-15 | findstr "RUNNING" >nul
    if %errorlevel% equ 0 (
        echo ✅ PostgreSQL 正在运行
    ) else (
        echo ⚠️  PostgreSQL 未运行，正在启动...
        net start postgresql-x64-15
    )
) else (
    echo ❌ PostgreSQL 未安装
    echo.
    echo 📥 请安装 PostgreSQL:
    echo    1. 访问: https://www.postgresql.org/download/windows/
    echo    2. 下载并安装 PostgreSQL 15 或更高版本
    echo    3. 安装时记住设置的密码
    echo    4. 安装完成后运行此脚本
    echo.
)

echo.
echo [检查 2] Redis 状态...
echo.

REM 检查 Redis 是否运行
tasklist /FI "IMAGENAME eq redis-server.exe" 2>nul | findstr "redis-server.exe" >nul
if %errorlevel% equ 0 (
    echo ✅ Redis 正在运行
) else (
    echo ❌ Redis 未运行
    echo.
    echo 📥 请安装 Redis:
    echo    1. 访问: https://github.com/tporadowski/redis/releases
    echo    2. 下载 Redis-x64-xxx.zip
    echo    3. 解压到 C:\Redis
    echo    4. 双击运行 redis-server.exe
    echo.
    echo 💡 或者使用 Docker:
    echo    docker run -d -p 6379:6379 --name redis redis:7-alpine
    echo.
)

echo.
echo ========================================
echo 📋 总结
echo ========================================

REM 检查 Docker
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo.
    echo ✅ Docker 已安装
    echo.
    echo 💡 推荐使用 Docker 启动数据库:
    echo    docker-compose up -d postgres redis
    echo.
) else (
    echo.
    echo ⚠️  Docker 未安装
    echo.
    echo 如果想使用 Docker (推荐):
    echo    1. 访问: https://www.docker.com/products/docker-desktop/
    echo    2. 下载并安装 Docker Desktop
    echo    3. 重启电脑
    echo    4. 运行: docker-compose up -d postgres redis
    echo.
)

echo ========================================
pause

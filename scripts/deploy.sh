#!/bin/bash

# LongChain RAG 一键部署脚本
# 适用于 Ubuntu 20.04/22.04

set -e

echo "=========================================="
echo "  LongChain RAG 系统部署脚本"
echo "=========================================="
echo ""

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then
    echo "请使用 sudo 运行此脚本"
    exit 1
fi

# 1. 更新系统
echo "📦 更新系统软件包..."
apt-get update && apt-get upgrade -y

# 2. 安装 Docker
if ! command -v docker &> /dev/null; then
    echo "🐳 安装 Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    systemctl enable docker
    systemctl start docker
    echo "✅ Docker 安装完成"
else
    echo "✅ Docker 已安装"
fi

# 3. 安装 Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "🔧 安装 Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo "✅ Docker Compose 安装完成"
else
    echo "✅ Docker Compose 已安装"
fi

# 4. 配置环境变量
echo ""
echo "⚙️  配置环境变量..."

if [ ! -f .env ]; then
    cp .env.example .env

    echo ""
    echo "请输入以下配置信息："
    echo ""

    # 生成随机密码
    DB_PASSWORD=$(openssl rand -base64 16)
    SECRET_KEY=$(openssl rand -hex 32)

    read -p "请输入 DashScope API Key: " DASHSCOPE_API_KEY

    # 更新 .env 文件
    sed -i "s/your_secure_db_password_here/$DB_PASSWORD/g" .env
    sed -i "s/your_dashscope_api_key_here/$DASHSCOPE_API_KEY/g" .env
    sed -i "s/your_super_secret_key_here_at_least_32_characters_long/$SECRET_KEY/g" .env

    echo "✅ 环境变量配置完成"
else
    echo "⚠️  .env 文件已存在，跳过配置"
fi

# 5. 配置防火墙
echo ""
echo "🔥 配置防火墙..."
if command -v ufw &> /dev/null; then
    ufw allow 22
    ufw allow 80
    ufw allow 443
    echo "y" | ufw enable
    echo "✅ 防火墙配置完成"
fi

# 6. 构建并启动服务
echo ""
echo "🚀 构建并启动服务..."
docker-compose down
docker-compose build
docker-compose up -d

# 7. 等待服务启动
echo ""
echo "⏳ 等待服务启动..."
sleep 10

# 8. 初始化数据库
echo ""
echo "💾 初始化数据库..."
docker-compose exec -T backend alembic upgrade head

# 9. 创建管理员账号
echo ""
echo "👤 创建管理员账号..."
read -p "请输入管理员用户名 [admin]: " ADMIN_USERNAME
ADMIN_USERNAME=${ADMIN_USERNAME:-admin}

read -s -p "请输入管理员密码: " ADMIN_PASSWORD
echo ""

docker-compose exec -T backend python -c "
from app.database import SessionLocal
from app.services.auth_service import auth_service
db = SessionLocal()
try:
    auth_service.create_user(db, '$ADMIN_USERNAME', '$ADMIN_PASSWORD', 'admin')
    print('✅ 管理员账号创建成功')
except Exception as e:
    print(f'⚠️  管理员账号可能已存在: {e}')
finally:
    db.close()
"

# 10. 显示服务状态
echo ""
echo "=========================================="
echo "  部署完成！"
echo "=========================================="
echo ""
echo "📊 服务状态："
docker-compose ps
echo ""
echo "🌐 访问地址："
echo "   前端: http://$(curl -s ifconfig.me)"
echo "   后端 API: http://$(curl -s ifconfig.me)/api"
echo ""
echo "👤 管理员账号："
echo "   用户名: $ADMIN_USERNAME"
echo "   密码: (您刚才输入的密码)"
echo ""
echo "📝 常用命令："
echo "   查看日志: docker-compose logs -f"
echo "   停止服务: docker-compose down"
echo "   启动服务: docker-compose up -d"
echo "   重启服务: docker-compose restart"
echo ""
echo "📖 详细文档请查看 DEPLOYMENT.md"
echo ""

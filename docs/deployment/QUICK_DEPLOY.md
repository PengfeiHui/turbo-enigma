# 快速部署指南 - 云服务器部署步骤

## 📋 前提条件
- 云服务器（阿里云/腾讯云/华为云等）
- 操作系统：Ubuntu 20.04/22.04 或 CentOS 7/8
- 最低配置：2核 4GB 内存 20GB 硬盘
- 已获取服务器的 SSH 登录信息

---

## 🚀 部署步骤（推荐方式 - Docker）

### 步骤 1：连接到服务器

```bash
# 使用 SSH 连接到你的云服务器
ssh root@你的服务器IP地址

# 或使用密钥登录
ssh -i /path/to/your-key.pem root@你的服务器IP地址
```

### 步骤 2：安装 Git

```bash
# Ubuntu/Debian
apt-get update
apt-get install -y git

# CentOS
yum install -y git
```

### 步骤 3：克隆项目到服务器

```bash
# 创建项目目录
mkdir -p /opt/apps
cd /opt/apps

# 克隆项目（如果已上传到 Git）
git clone https://github.com/你的用户名/longChain_RAG.git
cd longChain_RAG

# 或者使用 scp 从本地上传
# 在本地执行：
# scp -r d:/code/projects/longChain_RAG root@服务器IP:/opt/apps/
```

### 步骤 4：运行一键部署脚本

```bash
# 给脚本执行权限
chmod +x deploy.sh

# 运行部署脚本
sudo ./deploy.sh
```

**脚本会自动完成以下操作：**
- ✅ 安装 Docker 和 Docker Compose
- ✅ 配置环境变量
- ✅ 配置防火墙
- ✅ 构建并启动所有服务
- ✅ 初始化数据库
- ✅ 创建管理员账号

### 步骤 5：配置环境变量（如果手动部署）

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑环境变量
nano .env
```

填入以下信息：
```env
# 数据库密码（自己设置一个强密码）
DB_PASSWORD=your_secure_password_123

# DashScope API Key（从阿里云获取）
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx

# JWT 密钥（生成随机密钥）
SECRET_KEY=执行命令生成：openssl rand -hex 32
```

### 步骤 6：启动服务

```bash
# 构建镜像
docker-compose build

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 步骤 7：初始化数据库

```bash
# 运行数据库迁移
docker-compose exec backend alembic upgrade head

# 创建管理员账号
docker-compose exec backend python -c "
from app.database import SessionLocal
from app.services.auth_service import auth_service
db = SessionLocal()
auth_service.create_user(db, 'admin', 'admin123456', 'admin')
db.close()
print('管理员账号创建成功：admin / admin123456')
"
```

### 步骤 8：配置域名（可选）

如果你有域名，修改 Nginx 配置：

```bash
# 编辑 Nginx 配置
nano frontend/nginx.conf
```

修改 `server_name`:
```nginx
server {
    listen 80;
    server_name yourdomain.com;  # 改成你的域名
    ...
}
```

重启前端服务：
```bash
docker-compose restart frontend
```

### 步骤 9：配置 SSL（推荐）

```bash
# 安装 Certbot
apt-get install certbot python3-certbot-nginx

# 获取 SSL 证书
certbot --nginx -d yourdomain.com

# 证书会自动续期
```

---

## 🔍 验证部署

### 1. 检查服务状态

```bash
# 查看所有容器
docker-compose ps

# 应该看到 3 个服务都在运行：
# - longchain-backend (running)
# - longchain-frontend (running)
# - longchain-db (running)
```

### 2. 测试后端 API

```bash
# 测试健康检查接口
curl http://localhost:8000/api/health

# 应该返回：{"status":"healthy"}
```

### 3. 访问前端

在浏览器中访问：
- `http://你的服务器IP`
- 或 `http://你的域名`

应该能看到登录页面

### 4. 登录测试

使用创建的管理员账号登录：
- 用户名：admin
- 密码：admin123456（或你设置的密码）

---

## 📦 如果没有 Git，手动上传部署

### 方式 1：使用 SCP 上传

```bash
# 在本地电脑执行（Windows 使用 Git Bash 或 PowerShell）
scp -r d:/code/projects/longChain_RAG root@服务器IP:/opt/apps/

# 然后连接到服务器
ssh root@服务器IP
cd /opt/apps/longChain_RAG
sudo ./deploy.sh
```

### 方式 2：使用 FTP 工具

1. 下载 FileZilla 或 WinSCP
2. 连接到服务器
3. 上传整个 `longChain_RAG` 文件夹到 `/opt/apps/`
4. SSH 登录服务器执行部署脚本

---

## 🛠️ 常用管理命令

```bash
# 查看日志
docker-compose logs -f                    # 所有服务
docker-compose logs -f backend           # 只看后端
docker-compose logs -f frontend          # 只看前端

# 重启服务
docker-compose restart                   # 重启所有
docker-compose restart backend          # 重启后端

# 停止服务
docker-compose stop                      # 停止所有
docker-compose down                      # 停止并删除容器

# 重新构建
docker-compose build --no-cache         # 清除缓存重新构建
docker-compose up -d --build            # 构建并启动

# 进入容器
docker-compose exec backend bash        # 进入后端容器
docker-compose exec db psql -U postgres # 进入数据库

# 查看资源占用
docker stats                            # 查看 CPU/内存使用
```

---

## 🔧 故障排查

### 问题 1：端口被占用

```bash
# 查看端口占用
netstat -tulnp | grep :80
netstat -tulnp | grep :8000

# 停止占用端口的服务
systemctl stop nginx  # 如果装了 Nginx
systemctl stop apache2  # 如果装了 Apache

# 或修改端口
nano docker-compose.yml
# 把 "80:80" 改成 "8080:80"
```

### 问题 2：内存不足

```bash
# 添加 Swap 空间
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

### 问题 3：Docker 安装失败

```bash
# 使用国内镜像
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```

### 问题 4：无法访问

```bash
# 检查防火墙
ufw status
ufw allow 80
ufw allow 443

# 云服务器安全组
# 需要在云服务器控制台添加安全组规则：
# - 入站规则：允许 TCP 80 端口
# - 入站规则：允许 TCP 443 端口
```

---

## 🔐 安全建议

### 1. 修改默认密码

```bash
# 登录后立即修改管理员密码
# 在前端：个人中心 -> 修改密码
```

### 2. 配置防火墙

```bash
# 只开放必要端口
ufw default deny incoming
ufw default allow outgoing
ufw allow 22    # SSH
ufw allow 80    # HTTP
ufw allow 443   # HTTPS
ufw enable
```

### 3. 禁用 root 密码登录

```bash
nano /etc/ssh/sshd_config

# 修改以下配置
PermitRootLogin no
PasswordAuthentication no

systemctl restart sshd
```

### 4. 定期备份

```bash
# 创建备份脚本（详见 DEPLOYMENT.md）
nano /root/backup.sh

# 设置定时任务
crontab -e
# 每天凌晨 2 点备份
0 2 * * * /root/backup.sh
```

---

## 📞 需要帮助？

如果遇到问题，请提供以下信息：

```bash
# 1. 系统信息
cat /etc/os-release

# 2. Docker 版本
docker --version
docker-compose --version

# 3. 服务状态
docker-compose ps

# 4. 错误日志
docker-compose logs backend --tail 50
docker-compose logs frontend --tail 50
```

---

## ✅ 部署成功检查清单

- [ ] 服务器可以正常 SSH 连接
- [ ] Docker 和 Docker Compose 安装成功
- [ ] 项目文件已上传到服务器
- [ ] 环境变量配置完成
- [ ] 所有容器正常运行（docker-compose ps）
- [ ] 数据库初始化成功
- [ ] 管理员账号创建成功
- [ ] 可以通过 IP 访问前端
- [ ] 可以正常登录系统
- [ ] 防火墙/安全组配置正确
- [ ] 如有域名，DNS 解析正确
- [ ] SSL 证书配置完成（可选）

---

**🎉 部署完成后，记得修改默认密码并定期备份数据！**

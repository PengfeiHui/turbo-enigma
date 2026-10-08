---
name: github-ssh-key
description: GitHub SSH 公钥信息
metadata:
  type: reference
---

GitHub SSH 公钥已配置并添加到 GitHub 账户。

**公钥类型**: ed25519
**公钥指纹**: `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINszl6NYDizL94jNM2U/tjb6T00pZawI+vRn7TpLuBG0`

**用途**:
- 用于 GitHub 仓库的 SSH 认证
- 无需每次输入密码即可推送代码

**GitHub 仓库**:
- SSH: `git@github.com:PengfeiHui/turbo-enigma.git`
- HTTPS: `https://github.com/PengfeiHui/turbo-enigma.git`

**相关配置**:
```bash
# 查看远程仓库
git remote -v

# origin: Gitee (SSH)
# github: GitHub (HTTPS，已配置)
```

**注意**: SSH 密钥私钥应妥善保管，不要泄露。

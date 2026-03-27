# PlayStation 游戏查询 Telegram Bot - 部署指南

## 部署方式

### 方式一：Docker 部署（推荐）

#### 1. 构建镜像

```bash
git clone https://github.com/Lariya-aa/psntelegrambot.git
cd psntelegrambot
docker build -t psntelegrambot:latest .
```

#### 2. 运行容器

```bash
docker run -d \
  --name ps-game-bot \
  -e TELEGRAM_BOT_TOKEN=your_telegram_bot_token \
  -e NOTION_TOKEN=your_notion_token \
  -e DATABASE_ID=2d09071e8c8480b491efe553bc776324 \
  notion-psbot:latest
```

#### 3. 验证运行

```bash
docker logs ps-game-bot
```

### 方式二：Docker Compose 部署

#### 1. 配置环境变量

```bash
cp .env.example .env
vim .env  # 编辑填入配置
```

#### 2. 启动服务

```bash
docker-compose up --build -d
```

#### 3. 查看日志

```bash
docker-compose logs -f
```

## GitHub Container Registry 部署

### 1. GitHub Actions 自动构建

推送到 main 分支后，GitHub Actions 会自动：
- 构建 Docker 镜像
- 推送到 ghcr.io

镜像地址：`ghcr.io/Lariya-aa/psntelegrambot:latest`

### 2. 拉取镜像

```bash
# 登录 GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u Lariya-aa --password-stdin

# 拉取镜像
docker pull ghcr.io/Lariya-aa/psntelegrambot:latest
```

### 3. 运行

```bash
docker run -d \
  --name ps-game-bot \
  -e TELEGRAM_BOT_TOKEN=your_token \
  -e NOTION_TOKEN=your_token \
  ghcr.io/Lariya-aa/psntelegrambot:latest
```

## 生产环境建议

### 1. 使用 Systemd 管理服务

创建 `/etc/systemd/system/ps-game-bot.service`：

```ini
[Unit]
Description=PlayStation Game Bot
Requires=docker.service
After=network-online.target docker.socket

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/bin/docker start ps-game-bot
ExecStop=/usr/bin/docker stop ps-game-bot
Restart=on-failure
RestartSec=10s

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable ps-game-bot
sudo systemctl start ps-game-bot
```

### 2. 使用 Nginx 反向代理（可选）

如果需要 Webhook 或其他 HTTP 服务：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8080;
    }
}
```

### 3. 监控

检查容器健康状态：

```bash
docker inspect --format='{{.State.Health.Status}}' ps-game-bot
```

查看资源使用：

```bash
docker stats ps-game-bot
```

## 卸载

```bash
# 停止容器
docker stop ps-game-bot

# 删除容器
docker rm ps-game-bot

# 删除镜像
docker rmi notion-psbot:latest
```

## 聊天权限配置

### 配置说明

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| ALLOW_PRIVATE_CHAT | true | 是否允许私聊 |
| ALLOWED_GROUP_IDS | (空) | 允许的群组 ID，逗号分隔 |

### 使用示例

**只允许私聊：**
```bash
docker run -d \
  --name ps-game-bot \
  -e TELEGRAM_BOT_TOKEN=your_token \
  -e NOTION_TOKEN=your_token \
  -e ALLOW_PRIVATE_CHAT=true \
  ghcr.io/Lariya-aa/psntelegrambot:latest
```

**只允许特定群组（禁用私聊）：**
```bash
docker run -d \
  --name ps-game-bot \
  -e TELEGRAM_BOT_TOKEN=your_token \
  -e NOTION_TOKEN=your_token \
  -e ALLOW_PRIVATE_CHAT=false \
  -e ALLOWED_GROUP_IDS=-1001234567890,-1009876543210 \
  ghcr.io/Lariya-aa/psntelegrambot:latest
```

### 获取群组 ID

把机器人加入群后，发送任意消息，然后访问：
```
https://api.telegram.org/bot<TOKEN>/getUpdates
```
找到 `chat.id` 就是群组 ID（通常是负数，如 `-1001234567890`）

## 常见问题

### Q: 如何更新 Bot？

```bash
git pull
docker-compose up --build -d
```

### Q: 如何查看日志？

```bash
docker-compose logs -f bot
```

### Q: 如何进入容器调试？

```bash
docker exec -it ps-game-bot /bin/bash
```

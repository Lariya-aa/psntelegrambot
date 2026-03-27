# PlayStation 游戏查询 Telegram Bot

一个连接 Notion 数据库的 Telegram Bot，用于查询 PlayStation 会免游戏和二档/三档订阅库游戏。

## 功能特性

- 搜索游戏名称
- 查询会免游戏信息（会免日期、版本）
- 查询订阅库游戏信息（入库日期、状态、档位）
- 支持 Docker 部署

## 快速开始

### 前置要求

- Python 3.11+
- Telegram Bot Token（从 [@BotFather](https://t.me/botfather) 获取）
- Notion Integration Token
- Notion 数据库

### 环境变量配置

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
NOTION_TOKEN=your_notion_token
DATABASE_ID=your_notion_database_id
ALLOW_PRIVATE_CHAT=true
ALLOWED_GROUP_IDS=
```

### 本地运行

```bash
pip install -r requirements.txt
python bot.py
```

### Docker 运行

```bash
docker build -t notion-psbot:latest .
docker run -d \
  --name ps-game-bot \
  -e TELEGRAM_BOT_TOKEN=your_token \
  -e NOTION_TOKEN=your_token \
  notion-psbot:latest
```

## 项目结构

```
notion_bot/
├── .github/
│   └── workflows/
│       └── docker-publish.yml  # GitHub Actions 构建
├── docs/
│   ├── README_zh.md           # 中文说明文档
│   └── DEPLOYMENT_zh.md       # 部署指南
├── config.py           # 配置管理
├── notion_api.py       # Notion API 封装
├── bot.py              # Telegram Bot 主程序
├── requirements.txt    # Python 依赖
├── Dockerfile          # Docker 镜像
├── docker-compose.yml  # Docker Compose 配置
├── .env.example        # 环境变量示例
├── .gitignore          # Git 忽略文件
├── CHANGELOG.md        # 版本更新日志
└── README.md           # 项目文档
```

## 使用方法

1. 发送 `/start` 给 Bot 开始使用
2. 直接发送游戏名称搜索，如：`潜水员戴夫`
3. 或使用 `/search <关键词>` 命令搜索

## 聊天权限

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| ALLOW_PRIVATE_CHAT | true | 是否允许私聊 (true/false) |
| ALLOWED_GROUP_IDS | (空) | 允许的群组 ID，逗号分隔 |

## 输出示例

**订阅库游戏：**
```
游戏名称: 潜水员戴夫
英文名称: DAVE THE DIVER
入库日期: 2024-04-16
状态: 在库
档位: 2档
```

**会免游戏：**
```
🎮 潜水员戴夫
   英文名称: DAVE THE DIVER
   版本: PS5, PS4
   会免日期: 2024-04-16
```

## 相关文档

- [中文说明文档](./docs/README_zh.md)
- [部署指南](./docs/DEPLOYMENT_zh.md)
- [版本更新日志](./CHANGELOG.md)

## License

MIT

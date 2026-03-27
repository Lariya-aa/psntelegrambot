# PlayStation 游戏查询 Telegram Bot - 说明文档

## 项目概述

本项目是一个基于 Python 的 Telegram Bot，通过 Notion API 连接 PlayStation 游戏数据库，提供游戏信息查询功能。

## 数据库结构

### 一档(会免)数据库

| 属性名 | 类型 | 说明 |
|--------|------|------|
| 游戏名称 | title | 游戏中文名称 |
| 英文名称 | rich_text | 游戏英文名称 |
| 版本 | multi_select | PS5 / PS4 |
| 会免日期 | rich_text | 每月会免日期 |
| Date | date | 日期 |

### 二档/三档(订阅库)数据库

| 属性名 | 类型 | 说明 |
|--------|------|------|
| 游戏名称 | title | 游戏中文名称 |
| 英文名称 | rich_text | 游戏英文名称 |
| 入库日期 | date | 加入订阅库日期 |
| 出库日期 | date | 退出订阅库日期（为空表示仍在库） |
| 档位 | select | 2档 / 3档 |
| 版本 | multi_select | PS5 / PS4 |

## 核心模块

### config.py

配置管理模块，从环境变量读取配置：

| 变量 | 说明 | 来源 |
|------|------|------|
| TELEGRAM_BOT_TOKEN | Telegram Bot Token | 环境变量 |
| NOTION_TOKEN | Notion Integration Token | 环境变量 |
| DATABASE_ID | Notion 数据库 ID | 环境变量 |

### notion_api.py

Notion API 封装模块：

- `search_db1_free_tier()` - 搜索一档(会免)数据库
- `search_db2_subscription()` - 搜索二档/三档(订阅库)数据库
- `search_all_databases()` - 并行搜索所有数据库
- `format_game()` - 格式化游戏信息输出

### bot.py

Telegram Bot 主程序，处理以下命令：

| 命令 | 功能 |
|------|------|
| /start | 欢迎信息和开始使用 |
| /help | 显示帮助信息 |
| /search \<关键词\> | 搜索游戏 |
| 直接发送文本 | 搜索游戏 |

## 环境变量

| 变量 | 必需 | 默认值 | 说明 |
|------|------|--------|------|
| TELEGRAM_BOT_TOKEN | 是 | - | 从 @BotFather 获取 |
| NOTION_TOKEN | 是 | - | Notion Integration Token |
| DATABASE_ID | 否 | 2d09071e8c8480b491efe553bc776324 | Notion 数据库 ID |
| NOTION_API_VERSION | 否 | 2025-09-03 | Notion API 版本 |
| ALLOW_PRIVATE_CHAT | 否 | true | 是否允许私聊 (true/false) |
| ALLOWED_GROUP_IDS | 否 | (空) | 允许的群组 ID，逗号分隔 |

## 依赖包

| 包名 | 版本 | 说明 |
|------|------|------|
| python-telegram-bot | 21.6 | Telegram Bot SDK |
| notion-client | 2.2.1 | Notion API 客户端 |
| python-dotenv | 1.0.1 | 环境变量管理 |

## 故障排除

### 问题：Bot 无响应

1. 检查 Telegram Bot Token 是否正确
2. 检查 Bot 是否已启动：`docker ps` 或 `ps aux | grep bot.py`

### 问题：搜索不到游戏

1. 检查 Notion Token 是否有效
2. 确认 Notion 数据库已分享给 Integration
3. 检查 DATABASE_ID 是否正确

### 问题：数据库查询错误

1. 确认 Notion API 版本是否支持
2. 检查网络连接是否正常

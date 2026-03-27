# 更新日志

所有重要的版本更新都会记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。

## [0.0.3] - 2026-03-27

### Fixed

- 修复 `notion_client.py` 与 `notion-client` 包名冲突问题，重命名为 `notion_api.py`

### Added

- 私聊权限控制 (`ALLOW_PRIVATE_CHAT`)
- 群组白名单功能 (`ALLOWED_GROUP_IDS`)

## [0.0.2] - 2026-03-27

### Added

- 初始版本发布
- Telegram Bot 基础功能
  - `/start` - 欢迎命令
  - `/help` - 帮助命令
  - `/search <关键词>` - 搜索命令
  - 直接发送文本搜索

- Notion 数据库集成
  - 一档(会免)游戏数据库查询
  - 二档/三档(订阅库)游戏数据库查询
  - 自动区分数据库类型

- 搜索功能
  - 并行搜索两个数据库
  - 游戏信息格式化输出
  - 状态自动判断（在库/已出库）

- Docker 支持
  - Dockerfile 构建
  - docker-compose 编排
  - GitHub Actions 自动构建

### Environment Variables

| Variable | Description |
|----------|-------------|
| TELEGRAM_BOT_TOKEN | Telegram Bot Token |
| NOTION_TOKEN | Notion Integration Token |
| DATABASE_ID | Notion Database ID |
| NOTION_API_VERSION | Notion API Version (default: 2025-09-03) |

### Database Schema

**一档(会免) Database:**
- 游戏名称 (title)
- 英文名称 (rich_text)
- 版本 (multi_select: PS5/PS4)
- 会免日期 (rich_text)
- Date (date)

**二档/三档(订阅库) Database:**
- 游戏名称 (title)
- 英文名称 (rich_text)
- 入库日期 (date)
- 出库日期 (date)
- 档位 (select: 2档/3档)
- 版本 (multi_select: PS5/PS4)

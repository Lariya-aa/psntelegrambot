"""
配置管理模块
从环境变量读取配置，支持 .env 文件
"""

import os
from dotenv import load_dotenv

# 加载 .env 文件（如果存在）
load_dotenv()

# Telegram Bot Token (必需)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Notion 配置
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_API_VERSION = os.getenv("NOTION_API_VERSION", "2025-09-03")

# 数据库 ID (两个数据库共用此 ID，通过 filter 属性区分)
DATABASE_ID = os.getenv("DATABASE_ID", "2d09071e8c8480b491efe553bc776324")


def validate_config():
    """验证必需配置"""
    missing = []
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not NOTION_TOKEN:
        missing.append("NOTION_TOKEN")

    if missing:
        raise ValueError(f"缺少必需配置: {', '.join(missing)}")

    return True

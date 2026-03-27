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

# 聊天权限配置
# 是否允许私聊
ALLOW_PRIVATE_CHAT = os.getenv("ALLOW_PRIVATE_CHAT", "true").lower() == "true"

# 允许的群组 ID 列表（留空则允许所有群）
# 格式: -1001234567890,-1009876543210
_ALLOWED_GROUPS = os.getenv("ALLOWED_GROUP_IDS", "")
ALLOWED_GROUP_IDS = [int(gid.strip()) for gid in _ALLOWED_GROUPS.split(",") if gid.strip()] if _ALLOWED_GROUPS else []


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


def is_chat_allowed(chat_type: str, chat_id: int) -> bool:
    """
    检查聊天是否被允许

    Args:
        chat_type: 'private', 'group', 'supergroup'
        chat_id: 聊天 ID

    Returns:
        True 如果允许，否则 False
    """
    if chat_type == 'private':
        return ALLOW_PRIVATE_CHAT
    elif chat_type in ('group', 'supergroup'):
        # 如果配置了白名单，检查是否在白名单中
        if ALLOWED_GROUP_IDS:
            return chat_id in ALLOWED_GROUP_IDS
        # 如果没有配置白名单，允许所有群
        return True
    return False

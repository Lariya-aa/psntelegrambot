"""
Notion API 封装模块
使用 Search API 查询，兼容多数据源数据库
"""

import logging
from notion_client import Client

from config import NOTION_TOKEN

logger = logging.getLogger(__name__)

# Notion 客户端
notion = Client(auth=NOTION_TOKEN)


def search_games(keyword: str, limit: int = 10) -> list:
    """
    使用 Search API 搜索游戏

    Args:
        keyword: 搜索关键词
        limit: 返回结果数量限制

    Returns:
        游戏信息列表
    """
    try:
        # 扩大搜索范围，因为搜索 API 只返回部分匹配
        response = notion.search(
            query=keyword,
            filter={"property": "object", "value": "page"},
            page_size=50  # 获取更多结果以便过滤
        )

        results = []
        for page in response.get('results', []):
            props = page.get('properties', {})

            # 尝试多种属性名获取游戏名称
            name = (
                props.get('Name', {}).get('title', [{}])[0].get('plain_text', '') or
                props.get('游戏名称', {}).get('title', [{}])[0].get('plain_text', '') or
                props.get('title', {}).get('title', [{}])[0].get('plain_text', '')
            )

            if not name:
                continue

            # 关键词精确匹配（不区分大小写）
            if keyword.lower() not in name.lower():
                continue

            # 过滤：必须有游戏相关属性（版本 multi_select 或 档位 select）
            has_version = bool(props.get('版本', {}).get('multi_select'))
            has_tier = bool(props.get('档位', {}).get('select'))

            # 既没有版本也没有档位，说明不是游戏页面
            if not has_version and not has_tier:
                continue

            # 尝试获取英文名称
            en_name = (
                ''.join([t.get('plain_text', '') for t in props.get('英文名称', {}).get('rich_text', [])]) or
                ''.join([t.get('plain_text', '') for t in props.get('English Name', {}).get('rich_text', [])])
            )

            # 判断是订阅库还是会免游戏
            if has_tier:
                # 订阅库游戏
                entry_date = props.get('入库日期', {}).get('date')
                exit_date = props.get('出库日期', {}).get('date')
                versions = [s['name'] for s in props.get('版本', {}).get('multi_select', [])]

                results.append({
                    'name': name,
                    'en_name': en_name,
                    'entry_date': entry_date.get('start') if entry_date else None,
                    'exit_date': exit_date.get('start') if exit_date else None,
                    'tier': props.get('档位', {}).get('select', {}).get('name'),
                    'versions': versions,
                    'db_type': 2
                })
            else:
                # 会免游戏
                versions = [s['name'] for s in props.get('版本', {}).get('multi_select', [])]
                free_date = ''.join([t.get('plain_text', '') for t in props.get('会免日期', {}).get('rich_text', [])])
                date = props.get('Date', {}).get('date')

                results.append({
                    'name': name,
                    'en_name': en_name,
                    'versions': versions,
                    'free_date': free_date,
                    'date': date.get('start') if date else None,
                    'db_type': 1
                })

        # 按关键词匹配度排序并限制数量
        return results[:limit]

    except Exception as e:
        logger.error(f"搜索错误: {e}")
        return []


def format_game(game: dict) -> str:
    """
    格式化游戏信息

    Args:
        game: 游戏信息字典

    Returns:
        格式化的游戏信息字符串
    """
    if game.get('db_type') == 1:
        # 一档(会免)游戏
        name = game.get('name', '未知')
        en_name = game.get('en_name', '')
        versions = game.get('versions', [])
        free_date = game.get('free_date', '')
        date = game.get('date', '')

        msg = f"🎮 {name}\n"
        if en_name:
            msg += f"   英文名称: {en_name}\n"
        msg += f"   版本: {', '.join(versions) if versions else '未知'}\n"
        msg += f"   会免日期: {free_date or '未知'}\n"
        if date:
            msg += f"   Date: {date}"
        return msg

    else:
        # 二档/三档(订阅库)游戏
        name = game.get('name', '未知')
        en_name = game.get('en_name', '')
        entry_date = game.get('entry_date', '未知')
        exit_date = game.get('exit_date')
        tier = game.get('tier', '未知')
        versions = game.get('versions', [])

        # 状态判断
        status = "已出库" if exit_date else "在库"

        msg = f"游戏名称: {name}\n"
        if en_name:
            msg += f"英文名称: {en_name}\n"
        msg += f"入库日期: {entry_date}\n"
        msg += f"状态: {status}\n"
        msg += f"档位: {tier}"
        if versions:
            msg += f"\n版本: {', '.join(versions)}"

        return msg


def search_and_format(keyword: str, limit: int = 10) -> list:
    """
    搜索游戏并格式化结果

    Args:
        keyword: 搜索关键词
        limit: 返回结果数量限制

    Returns:
        格式化后的游戏信息列表
    """
    games = search_games(keyword, limit)
    return [format_game(game) for game in games]

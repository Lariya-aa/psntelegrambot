"""
Notion API 封装模块
通过 filter 属性区分一档(会免)数据库和二档/三档(订阅库)数据库
"""

import logging
import concurrent.futures
from notion_client import Client

from config import NOTION_TOKEN, NOTION_API_VERSION, DATABASE_ID

logger = logging.getLogger(__name__)

# Notion 客户端
notion = Client(auth=NOTION_TOKEN, notion_api_version=NOTION_API_VERSION)


def search_db1_free_tier(keyword: str, limit: int = 10) -> list:
    """
    搜索一档(会免)数据库
    一档数据库没有"档位"属性，通过 NOT 档位 来排除二档数据

    Args:
        keyword: 搜索关键词
        limit: 返回结果数量限制

    Returns:
        游戏信息列表
    """
    try:
        # 使用 NOT 组合排除二档数据：一档没有"档位"属性
        response = notion.databases.query(
            database_id=DATABASE_ID,
            filter={
                "and": [
                    {
                        "property": "游戏名称",
                        "rich_text": {"contains": keyword}
                    },
                    {
                        "not": {
                            "property": "档位",
                            "select": {"is_not_empty": True}
                        }
                    }
                ]
            },
            page_size=limit
        )

        results = []
        for page in response.get('results', []):
            props = page['properties']
            name = props.get('游戏名称', {}).get('title', [{}])[0].get('plain_text', '')
            en_name = ''.join([t.get('plain_text', '') for t in props.get('英文名称', {}).get('rich_text', [])])
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

        return results

    except Exception as e:
        logger.error(f"一档数据库搜索错误: {e}")
        return []


def search_db2_subscription(keyword: str, limit: int = 10) -> list:
    """
    搜索二档/三档(订阅库)数据库
    二档数据库有"档位"属性

    Args:
        keyword: 搜索关键词
        limit: 返回结果数量限制

    Returns:
        游戏信息列表
    """
    try:
        response = notion.databases.query(
            database_id=DATABASE_ID,
            filter={
                "and": [
                    {
                        "property": "游戏名称",
                        "rich_text": {"contains": keyword}
                    },
                    {
                        "property": "档位",
                        "select": {"is_not_empty": True}
                    }
                ]
            },
            page_size=limit
        )

        results = []
        for page in response.get('results', []):
            props = page['properties']
            name = props.get('游戏名称', {}).get('title', [{}])[0].get('plain_text', '')
            en_name = ''.join([t.get('plain_text', '') for t in props.get('英文名称', {}).get('rich_text', [])])

            # 入库日期
            entry_date = props.get('入库日期', {}).get('date')
            entry_date_str = entry_date.get('start') if entry_date else None

            # 出库日期 - 用于判断状态
            exit_date = props.get('出库日期', {}).get('date')
            exit_date_str = exit_date.get('start') if exit_date else None

            # 档位
            tier = props.get('档位', {}).get('select', {})
            tier_name = tier.get('name') if tier else None

            # 版本
            versions = [s['name'] for s in props.get('版本', {}).get('multi_select', [])]

            results.append({
                'name': name,
                'en_name': en_name,
                'entry_date': entry_date_str,
                'exit_date': exit_date_str,
                'tier': tier_name,
                'versions': versions,
                'db_type': 2
            })

        return results

    except Exception as e:
        logger.error(f"二档数据库搜索错误: {e}")
        return []


def search_all_databases(keyword: str, limit: int = 10) -> list:
    """
    搜索所有数据库（会免 + 订阅库）

    Args:
        keyword: 搜索关键词
        limit: 返回结果数量限制

    Returns:
        游戏信息列表
    """
    # 并行搜索两个数据库
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_db1 = executor.submit(search_db1_free_tier, keyword, limit)
        future_db2 = executor.submit(search_db2_subscription, keyword, limit)

        results_db1 = future_db1.result()
        results_db2 = future_db2.result()

    # 合并结果
    all_results = results_db1 + results_db2
    return all_results[:limit]


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
    games = search_all_databases(keyword, limit)
    return [format_game(game) for game in games]

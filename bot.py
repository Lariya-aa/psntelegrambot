"""
PlayStation 游戏查询 Telegram Bot
使用 Notion API 查询会免游戏和订阅库游戏
"""

import logging
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from config import TELEGRAM_BOT_TOKEN, validate_config, is_chat_allowed
from notion_api import search_and_format

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /start 命令"""
    await update.message.reply_text(
        "🎮 PlayStation 游戏查询 Bot\n\n"
        "发送游戏名称即可搜索，如：潜水员戴夫\n"
        "支持查询会免游戏和二档/三档订阅库游戏\n\n"
        "命令列表：\n"
        "/start - 开始使用\n"
        "/help - 显示帮助\n"
        "/search <关键词> - 搜索游戏"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /help 命令"""
    await update.message.reply_text(
        "📖 帮助信息\n\n"
        "命令列表：\n"
        "/start - 开始使用\n"
        "/help - 显示帮助\n"
        "/search <关键词> - 搜索游戏\n\n"
        "直接发送游戏名也可搜索"
    )


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /search 命令"""
    # 检查聊天是否允许
    if not is_chat_allowed(update.effective_chat.type, update.effective_chat.id):
        return

    keyword = ' '.join(context.args) if context.args else ''

    if not keyword:
        await update.message.reply_text("请提供搜索关键词，如：/search 潜水员戴夫")
        return

    await update.message.reply_text(f"🔍 搜索「{keyword}」...")

    try:
        results = search_and_format(keyword)

        if not results:
            await update.message.reply_text(f"没有找到「{keyword}」相关的游戏 😅")
            return

        await update.message.reply_text(f"找到 {len(results)} 条结果：\n")

        for game in results[:10]:
            await update.message.reply_text(game)

    except Exception as e:
        logger.error(f"搜索错误: {e}")
        await update.message.reply_text("搜索时发生错误，请稍后重试")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理普通文本消息"""
    # 检查聊天是否允许
    if not is_chat_allowed(update.effective_chat.type, update.effective_chat.id):
        return

    # 调试日志
    logger.info(f"收到消息: '{update.message.text}' | chat_type: {update.effective_chat.type}")

    keyword = update.message.text.strip()

    # 群组消息：只处理 @mention 机器人 的消息
    if update.effective_chat.type in ('group', 'supergroup'):
        # 检查是否 @提到了机器人
        mentioned = False
        for entity in update.message.entities or []:
            if entity.type == 'mention':
                mentioned = True
                break

        if not mentioned:
            # 群聊中没有 @mention，不处理
            return

    # 去掉 @mention 部分（如 "@botname 游戏" -> "游戏"）
    keyword = re.sub(r'@\w+\s*', '', keyword).strip()

    logger.info(f"处理后关键词: '{keyword}'")

    if not keyword:
        return

    try:
        results = search_and_format(keyword)

        if not results:
            await update.message.reply_text(f"没有找到「{keyword}」相关的游戏 😅")
            return

        await update.message.reply_text(f"🔍 「{keyword}」搜索结果：\n")

        for game in results[:10]:
            await update.message.reply_text(game)

    except Exception as e:
        logger.error(f"搜索错误: {e}")
        await update.message.reply_text("搜索时发生错误，请稍后重试")


def main():
    """启动 Bot"""
    # 验证配置
    try:
        validate_config()
    except ValueError as e:
        print(f"配置错误: {e}")
        return

    # 构建应用
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # 注册命令处理器
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("search", search_command))

    # 处理普通消息
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("🤖 Bot 已启动!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

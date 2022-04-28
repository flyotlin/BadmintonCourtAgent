from telegram import Update
from telegram.ext import CommandHandler, CallbackContext


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        '椰～歡迎使用羽球場預約小幫手 - 阿椰！\n\n'
        '以下為小幫手支援的指令：\n'
        '/apply: 預約場地\n'
        '/check: 查看目前 17-fit 上最新可預約場地資訊\n'
        '/check_now: 查看系統 cache 中可預約場地資訊\n'
        '/toggle: 開啟/關閉每兩週的例行預約提醒 (目前只有 30 秒後提醒功能)\n'
    )


HelpHandler = CommandHandler("help", help_command)

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext


def check_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /check is issued."""
    update.message.reply_text(
        '椰～歡迎使用羽球場預約小幫手 - 阿椰！\n\n'
        '以下為小幫手支援的指令：\n'
        '/help: 查看可用的阿椰指令\n'
        '/check: 檢查羽球場現有的空場地\n'
        '/reserve: 預約某場地\n'
        '/toggle_check: 每天於固定時間自動檢查且回傳空場地資訊\n'
        '/toggle_reserve: 每天於固定時間自動預約 (週三/週五 20:00, 21:00 任一場地)\n'
    )


CheckHandler = CommandHandler("check", check_command)

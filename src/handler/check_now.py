import datetime
import os

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext


def check_now_command(update: Update, context: CallbackContext) -> None:
    if os.path.isfile('./court-info-cache'):
        reply_str = ''
        with open('./court-info-cache', 'r') as f:
            reply_str = f.read()
        raw_time = os.path.getmtime("./court-info-cache")
        converted_time = datetime.fromtimestamp(raw_time).strftime('%Y-%m-%d %H:%M:%S')
        update.message.reply_text(f'Cached Time: {converted_time}\n\n' + reply_str)
    else:
        update.message.reply_text('目前無可預約場地 cache 資料，請使用指令 /check')


CheckNowHandler = CommandHandler("check_now", check_now_command)

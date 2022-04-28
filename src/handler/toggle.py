import datetime

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext


def toggle_alarm(update: Update, context: CallbackContext) -> None:
    now = datetime.datetime.now()
    context.job_queue.run_once(
        notify,
        when=now + datetime.timedelta(seconds=30),
        context=update.message.chat_id
    )
    update.message.reply_text('Run once in 30 seconds!')


def notify(context: CallbackContext):
    job = context.job
    context.bot.send_message(job.context, text="椰，30 秒後的提醒")


ToggleHandler = CommandHandler("toggle", toggle_alarm)

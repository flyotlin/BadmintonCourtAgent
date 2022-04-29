from datetime import time
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext


def toggle_poll_command(update: Update, context: CallbackContext) -> None:
    job_name = "poll_create_by_toggle"

    if len(context.args) == 1 and context.args[0] == 'delete':
        jobs = context.job_queue.get_jobs_by_name(job_name)
        for j in jobs:
            j.job.remove()
        update.message.reply_text('成功移除設定')
        return

    poll_job = list(filter(lambda x: x.name == job_name, context.job_queue.jobs()))
    if len(poll_job) == 0:
        context.job_queue.run_daily(
            callback=create_poll,
            time=time(hour=20 - 8, minute=0),
            days=(1, 3),
            name=job_name,
            context=update.message.chat_id
        )
        update.message.reply_text('成功設定週二/四晚上八點自動建立投票')
    else:
        update.message.reply_text('不能重複設定椰')


def create_poll(context: CallbackContext):
    question = "椰～打球嗎？"
    choices = ["打求", "不打求"]
    job = context.job

    context.bot.send_poll(
        job.context,
        question,
        choices,
        is_anonymous=False,
        allows_multiple_answers=True,
    )


TogglePollHandler = CommandHandler("toggle_poll", toggle_poll_command)

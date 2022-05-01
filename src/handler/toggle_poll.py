import re

from datetime import time
from typing import Tuple
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, Job

from src.handler.util import agent_argument_error, agent_command_error, agent_success


COMMAND = 'toggle_poll'
REMIND_JOB_NAME = 'poll_created_by_toggle'


def toggle_poll_command(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 2:
        agent_argument_error(update, COMMAND)
        return

    if len(context.args) == 1:
        delete_poll(update, context)
        return
    else:
        create_poll(update, context)
        return


def poll_callback(context: CallbackContext):
    question = "椰～明天打球嗎？"
    choices = ["打求", "不打求"]
    job = context.job

    context.bot.send_poll(
        job.context,
        question,
        choices,
        is_anonymous=False,
        allows_multiple_answers=True,
    )


def create_poll(update: Update, context: CallbackContext):
    DEFAULT_JOB_CONF = ((1, 3), "15:00")    # Saturday, 15:00 (day, time)

    existing_poll_jobs = list(filter(lambda x: x.name == REMIND_JOB_NAME, context.job_queue.jobs()))
    if len(existing_poll_jobs) > 0:
        agent_command_error(update, '不能重複設定椰')
        return

    if len(context.args) == 2:
        _days = context.args[0]
        _time = context.args[1]
        if not re.match("([0-1][0-9]|2[0-3])\:([0-5][0-9])", _time):
            agent_command_error(update, '時間格式錯誤椰')
            return
        if not re.match("([0-6]\,)*([0-6])", _days):
            agent_command_error(update, '星期格式錯誤椰')
            return
        _hour, _minute = _time.split(':')
        _days = tuple(map(int, _days.split(',')))
    else:
        _hour, _minute = DEFAULT_JOB_CONF[1].split(':')
        _days = DEFAULT_JOB_CONF[0]
    _hour = int(_hour)
    _minute = int(_minute)

    context.job_queue.run_daily(
        callback=poll_callback,
        time=time(hour=_hour - 8, minute=_minute),
        days=_days,
        name=REMIND_JOB_NAME,
        context=update.message.chat_id
    )
    agent_success(update, f"椰～於 {_hour}:{_minute} 設定成功！")
    return


def delete_poll(update: Update, context: CallbackContext) -> None:
    if context.args[0] != 'delete':
        agent_argument_error(update, COMMAND)
        return

    jobs: Tuple[Job] = context.job_queue.get_jobs_by_name(REMIND_JOB_NAME)
    for j in jobs:
        j.job.remove()
    update.message.reply_text('成功移除設定')
    return


TogglePollHandler = CommandHandler("toggle_poll", toggle_poll_command)

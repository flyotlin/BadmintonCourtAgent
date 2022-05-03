from datetime import time
from typing import Tuple
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, Job

from src.util import (
    agent_argument_error,
    agent_command_error,
    agent_success,
    store_job_to_file,
    remove_job_from_file
)
from src.callbacks import reserve_callback


COMMAND = 'toggle_reserve'
RESERVE_JOB_NAME = 'reserve_created_by_toggle'
RESERVE_RUN_TIME = ['10', '15', '20']


def toggle_reserve_command(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 1:
        agent_argument_error(update, COMMAND)
        return

    if len(context.args) == 1:
        delete_reserve(update, context)
        return
    else:
        create_reserve(update, context)
        return


def create_reserve(update: Update, context: CallbackContext):
    for i in RESERVE_RUN_TIME:
        job_name = RESERVE_JOB_NAME + i
        existing_poll_jobs = list(filter(lambda x: x.name == job_name, context.job_queue.jobs()))
        if len(existing_poll_jobs) > 0:
            agent_command_error(update, '不能重複設定椰')
            return

        _hour = ((int(i) + 24) - 8) % 24
        store_job_to_file({
            'name': job_name,
            'hour': _hour,
            'minute': 0,
            'days': [x for x in range(0, 7)],
            'context': update.message.chat_id,
            'callback': 'reserve_callback'
        })
        context.job_queue.run_daily(
            callback=reserve_callback,
            time=time(hour=_hour, minute=0),
            name=job_name,
            context=update.message.chat_id
        )
        agent_success(update, f"椰～於 {i}:00 設定成功！")
    return


def delete_reserve(update: Update, context: CallbackContext) -> None:
    if context.args[0] != 'delete':
        agent_argument_error(update, COMMAND)
        return

    for i in RESERVE_RUN_TIME:
        job_name = RESERVE_JOB_NAME + i
        remove_job_from_file(job_name)
        jobs: Tuple[Job] = context.job_queue.get_jobs_by_name(job_name)
        for j in jobs:
            j.job.remove()
        agent_success(update, f'成功移除設定 {job_name}')
    return


ToggleReserveHandler = CommandHandler("toggle_reserve", toggle_reserve_command)

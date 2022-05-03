import json
import os
from datetime import time
from telegram import Update
from telegram.ext import JobQueue
from typing import List, TypedDict

from src.callbacks import poll_callback, remind_callback, reserve_callback


Job = TypedDict('Job', {
    'name': str,
    'hour': int,
    'minute': int,
    'days': List[int],
    'context': str,
    'callback': str
})
JOB_QUEUE_FILE = '.job_queue'


def agent_argument_error(update: Update, command: str):
    update.message.reply_text(f'阿椰不懂你的指令，請參考 /help {command}\n')


def agent_command_error(update: Update, error_msg: str):
    update.message.reply_text(error_msg)


def agent_internal_error(update: Update, error_msg: str):
    update.message.reply_text(error_msg)


def agent_success(update: Update, success_msg: str):
    update.message.reply_text(success_msg)


def store_job_to_file(job: Job) -> None:
    open_mode = 'a' if os.path.isfile(JOB_QUEUE_FILE) else 'w'

    with open(JOB_QUEUE_FILE, open_mode, encoding='utf8') as f:
        f.write(json.dumps(job))
        f.write('\n')


def remove_job_from_file(job_name: str) -> None:
    with open(JOB_QUEUE_FILE, 'r', encoding='utf8') as f:
        lines = f.read().strip().split('\n')
        lines = list(map(json.loads, lines))
        job_idx = next((idx for (idx, item) in enumerate(lines) if item["name"] == job_name), -1)
        if job_idx != -1:
            lines.pop(job_idx)

    with open(JOB_QUEUE_FILE, 'w', encoding='utf8') as f:
        for line in lines:
            f.write(json.dumps(line))
            f.write('\n')


def load_jobs_from_file(job_queue: JobQueue, job_file: str = JOB_QUEUE_FILE) -> None:
    if not os.path.isfile(job_file):
        return

    with open(JOB_QUEUE_FILE, 'r', encoding='utf8') as f:
        lines = f.read().strip().split('\n')
        lines = list(map(json.loads, lines))
        for line in lines:
            print(line)

            if line['callback'] == 'poll_callback':
                _func = poll_callback
            elif line['callback'] == 'remind_callback':
                _func = remind_callback
            elif line['callback'] == 'reserve_callback':
                _func = reserve_callback

            job_queue.run_daily(
                callback=_func,
                time=time(hour=line['hour'], minute=line['minute']),
                days=line['days'],
                name=line['name'],
                context=line['context']
            )

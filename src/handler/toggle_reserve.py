import os

from datetime import datetime, time, timedelta
import traceback
from typing import Tuple
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, Job

from src.handler.util import agent_argument_error, agent_command_error, agent_success
from src.BatmintonReserveAgent import BatmintonReserveAgent


COMMAND = 'toggle_reserve'
RESERVE_JOB_NAME = 'reserve_created_by_toggle'
RESERVE_RUN_TIME = ['10', '15', '20']
TOKEN_FILE = '.token'


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


def reserve_callback(context: CallbackContext):
    job = context.job

    # Token
    _token = {
        'PHPSESSID': '',
        'XSRF-TOKEN': '',
        '17fit_system_session': ''
    }
    if not os.path.isfile(TOKEN_FILE):
        context.bot.send_message(chat_id=job.context, text='請使用指令 /token 設定 token')
        return

    with open(TOKEN_FILE, 'r', encoding='utf8') as f:
        lines = f.read().strip().split('\n')
        _token['PHPSESSID'] = lines[0]
        _token['XSRF-TOKEN'] = lines[1]
        _token['17fit_system_session'] = lines[2]

    # Reserve arguments
    _court = ('近講臺中')

    now = datetime.now()
    last_delta = now.weekday() - 1
    next_delta = 8 - now.weekday()
    _time = []
    _time.extend([now - timedelta(last_delta + i * 7) for i in range(2)])
    _time.extend([now + timedelta(next_delta + i * 7) for i in range(2)])
    _reserve_times = []
    for t in ["20:00", "21:00"]:
        for d in _time:
            _reserve_times.extend([f"{d.year}-{d.month:02}-{d.day:02} {t}:00"])

    # Reserve with `Token` and `Arguments`
    try:
        agent = BatmintonReserveAgent(_token)

        court_and_datetimes = []
        for reserve_time in _reserve_times:
            court_and_datetimes += agent.check(time=reserve_time, courts=_court)

        for court_and_datetime in court_and_datetimes:
            agent.go(court_and_datetime)

            # TODO: send success preserve message to telegram (by Cliff)
            context.bot.send_message(chat_id=job.context, text=f"reserve court {court_and_datetime['court']['member_name']} at {court_and_datetime['datetime']['datetime']} success!")
        else:
            context.bot.send_message(chat_id=job.context, text='您指定的場地已經被預約了椰')
    except Exception:
        print(traceback.print_exc())
        context.bot.send_message(chat_id=job.context, text='預約失敗，可能的原因為 token 失效、場地已被預約...')


def create_reserve(update: Update, context: CallbackContext):
    for i in RESERVE_RUN_TIME:
        job_name = RESERVE_JOB_NAME + i
        existing_poll_jobs = list(filter(lambda x: x.name == job_name, context.job_queue.jobs()))
        if len(existing_poll_jobs) > 0:
            agent_command_error(update, '不能重複設定椰')
            return

        context.job_queue.run_daily(
            callback=reserve_callback,
            time=time(hour=int(i) - 8, minute=0),
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
        jobs: Tuple[Job] = context.job_queue.get_jobs_by_name(job_name)
        for j in jobs:
            j.job.remove()
        agent_success(update, f'成功移除設定 {job_name}')
    return


ToggleReserveHandler = CommandHandler("toggle_reserve", toggle_reserve_command)

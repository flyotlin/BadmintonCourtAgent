import os
import traceback
from datetime import datetime, timedelta
from telegram.ext import CallbackContext

from src.agent import BadmintonReserveAgent


TOKEN_FILE = '.token'


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
        agent = BadmintonReserveAgent(_token)

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


def remind_callback(context: CallbackContext):
    job = context.job
    context.bot.send_message(chat_id=job.context, text='記得預約羽球場喔～')

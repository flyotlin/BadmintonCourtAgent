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
    _date = get_date([3, 5])
    _court = get_court([2])
    _time = get_time(['21:00'])

    # Reserve with `Token` and `Arguments`
    try:
        not_available_courts = []
        available_courts = []
        agent = BadmintonReserveAgent(_token)
        for i in _court:
            for j in _date:
                for k in _time:
                    if agent.go(court=i, date=j, time=k):
                        available_courts.append([i, j, k])
                    else:
                        not_available_courts.append([i, j, k])
    except Exception:
        print(traceback.print_exc())
        context.bot.send_message(chat_id=job.context, text='預約失敗，可能的原因為 token 失效、場地已被預約...')
    finally:
        if len(available_courts) > 0:
            reply_str = '成功預約:\n'
            for i in available_courts:
                reply_str += f'{i[1]} {i[2]} @ 第{i[0]} 場\n'
            reply_str += '阿椰期待與你打求～'
            context.bot.send_message(chat_id=job.context, text=reply_str)
        # if len(not_available_courts) > 0:
        #     reply_str = '某些場地無法自動預約椰～\n'
        #     for i in not_available_courts:
        #         reply_str += f'{i[1]} {i[2]} @ 第{i[0]} 場\n'
        #     context.bot.send_message(chat_id=job.context, text=reply_str)


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


def get_court(courts: list):
    return tuple(courts)


def get_time(times: list):
    return tuple(times)


def get_date(days: list):
    now = datetime.now()
    _date = []

    for d in days:
        d = d - 1
        next_delta = ((d + 7) - now.weekday()) % 7
        _date.extend([now + timedelta(next_delta + i * 7) for i in range(2)])

    _date = tuple(map(lambda x: f'{x.month:02}-{x.day:02}', _date))

    return _date

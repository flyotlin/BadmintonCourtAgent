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
    now = datetime.now()
    next_delta = 9 - now.weekday()
    _date = []
    _date.extend([now + timedelta(next_delta + i * 7) for i in range(2)])
    _date.extend([now + timedelta((next_delta + 2) + i * 7) for i in range(2)])
    _date = tuple(map(lambda x: f'{x.month:02}-{x.day:02}', _date))
    _court = (1, 3)
    _time = ("20:00", "21:00")

    # Reserve with `Token` and `Arguments`
    try:
        not_available_courts = []
        agent = BadmintonReserveAgent(_token)
        for i in _court:
            for j in _date:
                for k in _time:
                    if agent.go(court=i, date=j, time=k):
                        context.bot.send_message(chat_id=job.context, text=f'椰～成功自動預約第 {_court} 場 @ {_date} {_time}！')
                    else:
                        not_available_courts.append([i, j, k])
    except Exception:
        print(traceback.print_exc())
        context.bot.send_message(chat_id=job.context, text='預約失敗，可能的原因為 token 失效、場地已被預約...')
    finally:
        if len(not_available_courts) == 0:
            return
        reply_str = '某些場地無法自動預約\n'
        # for i in not_available_courts:
        #     reply_str += f'{i[1]} {i[2]} @ 第{i[0]} 場\n'
        context.bot.send_message(chat_id=job.context, text=reply_str)


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

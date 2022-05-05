from datetime import datetime
import os
import traceback

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters

from src.util import agent_internal_error, agent_success
from agent import BadmintonReserveAgent


STAGE_COURT, STAGE_DATE, STAGE_TIME = range(3)
COURTS = ['近講臺右', '近講臺中', '近講臺左', '近門口右', '近門口中', '近門口左']
TOKEN_FILE = '.token'


def reserve(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        '你好，我是羽球場預約小幫手 - 阿椰！\n'
        '接下來我會幫助你預約羽球場，請依照指示填入要預約的羽球場資訊\n'
        '傳送 /cancel 能夠取消此次的預約流程\n\n'
        '請問你要預約的是第幾場？ (1-6)'
    )
    context.user_data['reserve_info'] = {
        'court': '',
        'date': '',
        'time': ''
    }
    return STAGE_COURT


def reserve_court(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('請問你要預約的日期是？ (只有個位數的請補零，e.g., 05-03)')
    context.user_data['reserve_info']['court'] = update.message.text
    return STAGE_DATE


def reserve_date(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('請問你要預約的時間是？ (請以 24 小時制輸入，0 ~ 9 點請補零，e.g., 07:00, 16:00)')
    context.user_data['reserve_info']['date'] = update.message.text
    return STAGE_TIME


def reserve_time(update: Update, context: CallbackContext) -> int:
    context.user_data['reserve_info']['time'] = update.message.text

    # Token
    _token = {
        'PHPSESSID': '',
        'XSRF-TOKEN': '',
        '17fit_system_session': ''
    }
    if not os.path.isfile(TOKEN_FILE):
        agent_internal_error(update, '請使用指令 /token 設定 token')
        return

    with open(TOKEN_FILE, 'r', encoding='utf8') as f:
        lines = f.read().strip().split('\n')
        _token['PHPSESSID'] = lines[0]
        _token['XSRF-TOKEN'] = lines[1]
        _token['17fit_system_session'] = lines[2]

    # Reserve arguments
    _court = tuple(COURTS[int(context.user_data['reserve_info']['court']) - 1])
    _time = f"{datetime.now().year}-{context.user_data['reserve_info']['date']} {context.user_data['reserve_info']['time']}:00"
    _reserve_times = [_time]

    # Reserve with `Token` and `Arguments`
    try:
        agent = BadmintonReserveAgent(_token)

        court_and_datetimes = []
        for reserve_time in _reserve_times:
            court_and_datetimes += agent.check(time=reserve_time, courts=_court)

        for court_and_datetime in court_and_datetimes:
            agent.go(court_and_datetime)

            # TODO: send success preserve message to telegram (by Cliff)
            agent_success(update, 'reserve court {} at {} success!'.format(court_and_datetime['court']['member_name'], court_and_datetime['datetime']['datetime']))
        else:
            agent_internal_error(update, '您指定的場地已經被預約了椰')
    except Exception:
        print(traceback.print_exc())
        agent_internal_error(update, '預約失敗，可能的原因為 token 失效、場地已被預約...')

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    update.message.reply_text(
        '椰，取消成功', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


ReserveHandler = ConversationHandler(
    entry_points=[CommandHandler('reserve', reserve)],
    states={
        STAGE_COURT: [MessageHandler(Filters.regex('^[1-6]$'), reserve_court)],
        STAGE_DATE: [MessageHandler(Filters.regex('^(1[0-2]|0[1-9])\-([0-2][1-9]|3[0-1])$'), reserve_date)],
        STAGE_TIME: [MessageHandler(Filters.regex('^(0[1-9]|1[0-9]|2[0-4]):00$'), reserve_time)]
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

import os
import re
import traceback

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from src.util import agent_argument_error, agent_internal_error
from src.agent import BadmintonReserveAgent


COMMAND = 'check'
TOKEN_FILE = '.token'
COURTS = ['近講臺右', '近講臺中', '近講臺左', '近門口右', '近門口中', '近門口左']


def check_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /check is issued."""
    if len(context.args) != 2:
        agent_argument_error(update, COMMAND)
        return

    # Argument: date and court
    _court = context.args[1]
    _date = context.args[0]
    if not re.match("([1-6]\,)*([1-6])", _court) and _court != "all":
        agent_argument_error(update, COMMAND)
        return
    if not re.match("(0[1-9]|1[0-2])\-([0-2][1-9]|3[0-1])", _date):
        agent_argument_error(update, COMMAND)
        return

    if _court == "all":
        _court = tuple(x for x in range(1, 7))
    else:
        _court = tuple(map(int, _court.split(',')))

    # Token
    if not os.path.isfile(TOKEN_FILE):
        agent_internal_error(update, '請使用指令 /token 設定 token')
        return

    _token = {
        'PHPSESSID': '',
        'XSRF-TOKEN': '',
        '17fit_system_session': ''
    }
    with open(TOKEN_FILE, 'r', encoding='utf8') as f:
        lines = f.read().strip().split('\n')
        _token['PHPSESSID'] = lines[0]
        _token['XSRF-TOKEN'] = lines[1]
        _token['17fit_system_session'] = lines[2]

    # Check
    try:
        agent = BadmintonReserveAgent(_token)
        check_results = agent.check(date=_date, courts=tuple(map(int, _court)))

        reply_str = ''
        for i in check_results:
            reply_str += f"第 {i['court_idx']} 場: {i['date']} {i['time']}\n"
        update.message.reply_text(reply_str)
    except Exception:
        traceback.print_exc()
        agent_internal_error(update, "內部發生一些錯誤椰～")
        return


CheckHandler = CommandHandler("check", check_command)

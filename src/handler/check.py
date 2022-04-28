import logging
import os

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from threading import Thread

from src.checker import Checker


logger = logging.getLogger('app')


class CheckerThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return


def subprocess_method_for_check(court_id):
    checker = Checker()
    checker.login()
    checker.check_single(court_id)
    print(checker.court_info_records)
    checker.logout()
    checker.bye()
    return checker.court_info_records


def check_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('小幫手阿椰正在查詢目前尚可預約的場地，請稍候...\n\n若急需得知結果，可以使用指令 /check_now 獲取可預約場地 cache 資料。')
    logger.info('小幫手阿椰正在查詢目前尚可預約的場地，請稍候...')

    threads = []
    for i in range(1, 7):
        threads.append(CheckerThread(target=subprocess_method_for_check, args=(i, )))
        threads[i - 1].start()

    results = []
    for i in range(6):
        res = threads[i].join()
        for j in res:
            results.append(j)

    logger.info(results)
    reply_str = ''
    for i in results:
        reply_str += f"第{i['court_id']}場\t{i['date']}\t{i['time']}\n"

    # Cache the result
    if os.path.isfile('./court-info-cache'):
        os.remove('./court-info-cache')
    with open('./court-info-cache', 'w') as f:
        f.write(reply_str)

    update.message.reply_text(reply_str)


CheckHandler = CommandHandler("check", check_command)

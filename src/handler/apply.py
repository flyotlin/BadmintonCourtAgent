import logging
import threading

from datetime import date
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters
from time import sleep

from src.applier import Applier


logger = logging.getLogger('app')

# Set up apply's 3 states
COURT, DATE, TIME = range(3)


def apply(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        '你好，我是羽球場預約小幫手 - 阿椰！\n'
        '接下來我會幫助你預約羽球場，請依照指示填入要預約的羽球場資訊\n'
        '傳送 /cancel 能夠取消此次的預約流程\n\n'
        '請問你要預約的是第幾場？ (1-6)'
    )

    return COURT


def apply_court(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('請問你要預約的日期是？ (只有個位數的請補零，e.g., 05/03)')
    logger.info(update.message.text)
    context.user_data['court'] = update.message.text
    return DATE


def apply_date(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('請問你要預約的時間是？ (請以 24 小時制輸入，0 ~ 9 點請補零，e.g., 07:00, 16:00)')
    logger.info(update.message.text)
    context.user_data['date'] = update.message.text
    return TIME


def apply_time(update: Update, context: CallbackContext) -> int:
    context.user_data['time'] = update.message.text

    thread = threading.Thread(
        target=submethod_for_apply,
        args=[update, context]
    )
    thread.daemon = True
    thread.start()

    update.message.reply_text(
        '小幫手阿椰正在幫您預約場地中，請稍候'
    )

    return ConversationHandler.END


def submethod_for_apply(update: Update, context: CallbackContext):
    import traceback

    day0 = date.today()
    month, day = context.user_data['date'].split('/')
    day1 = date(day0.year, int(month), int(day))
    delta = (day1 - day0).days
    date_id = delta + 4

    try:
        applier = Applier()
        applier.login()
        print(
            context.user_data['court'],
            date_id,
            context.user_data['time']
        )
        applier.apply(
            context.user_data['court'],
            str(date_id),
            context.user_data['time'],
        )
        logger.info('預約成功！')
        update.message.reply_text(
            '預約成功！阿椰期待與你打求'
        )
    except Exception as err:
        logger.info(err)
        update.message.reply_text('預約失敗...')
        traceback.print_exc()
    finally:
        sleep(2)
        applier.logout()
        applier.bye()


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        '椰，取消成功', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


ApplyHandler = ConversationHandler(
    entry_points=[CommandHandler('apply', apply)],
    states={
        COURT: [MessageHandler(Filters.regex('^[1-6]$'), apply_court)],
        DATE: [MessageHandler(Filters.regex('^(1[0-2]|0[1-9])\/([0-2][1-9]|3[0-1])$'), apply_date)],
        TIME: [MessageHandler(Filters.regex('^(0[1-9]|1[0-9]|2[0-4]):00$'), apply_time)]
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

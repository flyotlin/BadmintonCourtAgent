from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters

PHP, XSRF, SYS_SESSION = range(3)


def token_command(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        '設定 token 讓阿椰正常運作\n\n'
        '分別需要設定 php_session, xsrf_token, system_session\n\n'
        '別擔心，這些可以在瀏覽器登入 17fit 後取得，對資工系的人來說並不會很難 (once said by a wise man)\n\n'
    )
    update.message.reply_text('php_session: \n')

    return PHP


def php(update: Update, context: CallbackContext) -> int:
    context.user_data['php_session'] = update.message.text
    update.message.reply_text('xsrf_token: \n')
    return XSRF


def xsrf(update: Update, context: CallbackContext) -> int:
    context.user_data['xsrf_token'] = update.message.text
    update.message.reply_text('system_session: \n')
    return SYS_SESSION


def sys_session(update: Update, context: CallbackContext) -> int:
    context.user_data['system_session'] = update.message.text

    with open('token', 'w', encoding='utf-8') as f:
        f.write(context.user_data['php_session'])
        f.write('\n')
        f.write(context.user_data['xsrf_token'])
        f.write('\n')
        f.write(context.user_data['system_session'])
        f.write('\n')

    update.message.reply_text('椰，token 設定成功！')

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        '椰，成功取消 token 設定流程', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


TokenHandler = ConversationHandler(
    entry_points=[CommandHandler('token', token_command)],
    states={
        PHP: [MessageHandler(Filters.regex('^.*$'), php)],
        XSRF: [MessageHandler(Filters.regex('^.*$'), xsrf)],
        SYS_SESSION: [MessageHandler(Filters.regex('^.*$'), sys_session)]
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

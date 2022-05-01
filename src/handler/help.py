from telegram import Update
from telegram.ext import CommandHandler, CallbackContext


def help_main(update: Update):
    update.message.reply_text(
        '椰～歡迎使用羽球場預約小幫手 - 阿椰！\n'
        '以下為小幫手支援的指令：\n\n'
        '/help <command>: 查看可用的阿椰指令，加上 command(optional) 後有更詳細說明\n'
        '/token: 設定 token\n'
        # '/check: 檢查羽球場現有的空場地\n'
        '/reserve: 預約場地\n'
        # '/toggle_check: 每天於固定時間自動檢查且回傳空場地資訊\n'
        '/toggle_reserve: 自動預約場地\n'
        '/toggle_poll: 自動開啟投票\n'
        '/toggle_remind: 自動傳送預約提醒訊息\n'
    )


def help_token(update: Update):
    update.message.reply_text(
        '/token: 設定 token\n\n'
        'token 包含: php_session, xsrf_token, system_session\n'
        '桌面瀏覽器登入 17fit 後可以從 developer tools -> application -> Cookies 中取得\n'
    )


def help_reserve(update: Update):
    update.message.reply_text(
        '/reserve: 預約場地\n\n'
        '提供 第幾場、日期、時間 等資訊後\n'
        '阿椰會自動幫您預約場地\n'
    )


def help_toggle_poll(update: Update):
    update.message.reply_text(
        '/toggle_poll: 自動開啟投票\n\n'
        '目前預設 每週二 / 四 晚上 8:00 開啟隔天是否打球的投票\n'
    )


def help_toggle_remind(update: Update):
    update.message.reply_text(
        '/toggle_remind: 自動傳送預約提醒訊息\n\n'
        '目前於 每週六 自動傳送預約提醒訊息\n'
    )


def help_toggle_reserve(update: Update):
    update.message.reply_text(
        '/toggle_reserve: 自動預約場地\n\n'
        '預設預約 週三/週五 20:00, 21:00 任一場地\n'
    )


all_available_commands = [
    ['token', help_token],
    ['reserve', help_reserve],
    ['toggle_poll', help_toggle_poll],
    ['toggle_remind', help_toggle_remind],
    ['toggle_reserve', help_toggle_reserve]
]


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    if len(context.args) > 1:
        return

    if len(context.args) == 0:
        help_main(update)
        return

    for command in all_available_commands:
        if context.args[0] == command[0]:
            command[1](update)


HelpHandler = CommandHandler("help", help_command)

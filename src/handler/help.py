from telegram import Update
from telegram.ext import CommandHandler, CallbackContext


def help_main(update: Update):
    update.message.reply_text(
        '椰～歡迎使用羽球場預約小幫手 - 阿椰！\n'
        '以下為小幫手支援的指令：\n\n'
        '/help <command>: 查看可用的阿椰指令，加上 command(optional) 後有更詳細說明\n'
        '/token: 設定 token\n'
        '/check: 查詢空場地\n'
        '/reserve: 預約場地\n'
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


def help_check(update: Update):
    update.message.reply_text(
        '/check <date> <court>: 查詢空場地\n\n'
        'date: 欲查詢的日期, e.g., "05-01"\n'
        'court: 欲查詢的場地(1-6)，以逗號分隔, e.g., "1,2,4"\n'
        '所有場地可輸入 "all"\n'
    )


def help_reserve(update: Update):
    update.message.reply_text(
        '/reserve: 預約場地\n\n'
        '提供 第幾場、日期、時間 等資訊後\n'
        '阿椰會自動幫您預約場地\n'
    )


def help_toggle_poll(update: Update):
    update.message.reply_text(
        '/toggle_poll [ <check | delete <id> | <days> <times> ]: 自動開啟投票\n\n'
        '設定於固定時間自動開啟投票\n'
        'check: 檢查已經設定的自動開啟投票排程\n'
        'delete: 字串 "delete" 可以刪除設定的預約提醒\n'
        'id: 於 check 中查詢\n'
        'days: 星期一 ~ 星期日 (0 ~ 6)，以逗號分隔, e.g., 0,2,3\n'
        'times: 台灣時間，24 小時制，以逗號分隔 (e.g., 14:28,15:00)\n'
    )


def help_toggle_remind(update: Update):
    update.message.reply_text(
        '/toggle_remind [ <check | delete <id> | <days> <times> ]: 自動傳送預約提醒訊息\n\n'
        '設定於固定時間自動傳送提醒訊息\n'
        'check: 檢查已經設定的自動開啟投票排程\n'
        'delete: 字串 "delete" 可以刪除設定的預約提醒\n'
        'id: 於 check 中查詢\n'
        'days: 星期一 ~ 星期日 (0 ~ 6)，以逗號分隔, e.g., 0,2,3\n'
        'times: 台灣時間，24 小時制，以逗號分隔 (e.g., 14:28,15:00)\n'
    )


def help_toggle_reserve(update: Update):
    update.message.reply_text(
        '/toggle_reserve [ <check | delete <id> | <days> <times> ]: 自動預約場地\n\n'
        '設定於固定時間自動預約第 1, 3 場，星期三、五，晚上 8:00, 9:00\n'
        'check: 檢查已經設定的自動開啟投票排程\n'
        'delete: 字串 "delete" 可以刪除設定的預約提醒\n'
        'id: 於 check 中查詢\n'
        'days: 星期一 ~ 星期日 (0 ~ 6)，以逗號分隔, e.g., 0,2,3\n'
        'times: 台灣時間，24 小時制，以逗號分隔 (e.g., 14:28,15:00)\n'
    )


all_available_commands = [
    ['token', help_token],
    ['reserve', help_reserve],
    ['check', help_check],
    ['toggle_reserve', help_toggle_reserve],
    ['toggle_poll', help_toggle_poll],
    ['toggle_remind', help_toggle_remind]
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

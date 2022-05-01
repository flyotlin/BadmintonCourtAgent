from telegram import Update


def agent_argument_error(update: Update, command: str):
    update.message.reply_text(f'阿椰不懂你的指令，請參考 /help {command}\n')


def agent_command_error(update: Update, error_msg: str):
    update.message.reply_text(error_msg)


def agent_internal_error(update: Update, error_msg: str):
    update.message.reply_text(error_msg)


def agent_success(update: Update, success_msg: str):
    update.message.reply_text(success_msg)

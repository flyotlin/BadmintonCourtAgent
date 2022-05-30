from telegram import Update
from telegram.ext import CommandHandler, CallbackContext


def help_main(update: Update):
    update.message.reply_text(
        '歡迎使用動得很厲害的國家機器 - 阿椰！\n'
        '壞掉請找 IT 大臣 Cliff Chen 急救\n'
        '以下為國家機器支援的指令：\n\n'
        '/fix: 呼叫 IT 大臣進行急救\n'
        '/300 <person>: 檢舉造謠者 <person>，罰款三百萬\n'
        '/responsible: 我負責\n'
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    if len(context.args) > 1:
        return

    if len(context.args) == 0:
        help_main(update)
        return


MachineHandler = CommandHandler("machine", help_command)

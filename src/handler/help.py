from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from src.json_reader import MessageReader


class HelpHandler(CommandHandler):
    def __init__(self):
        self.handler_command = "help"
        self.reader = MessageReader()

        super().__init__(self.handler_command, self.help_command())

    def help_command(self) -> callable:
        def callback(update: Update, context: CallbackContext):
            args_num = len(context.args)

            if args_num > 1:    # invalid arguments
                return
            if args_num == 0:   # show all commands
                self.help_main(update)
                return
            # individual command
            arg_command = context.args[0]
            self.help_individual_command(arg_command, update)
        return callback

    def help_main(self, update: Update) -> callable:
        key = "help_main"
        username = update.message.from_user.username
        user_id = update.message.from_user.id

        reply_msg = self.reader.get(key, username=username, id=user_id)
        update.message.reply_text(reply_msg)

    def help_individual_command(self, command: str, update: Update):
        key = f"help_{command}"
        try:
            reply_msg = self.reader.get(key)
        except Exception as e:
            reply_msg = self.reader.get("help_error", command=command)
        update.message.reply_text(reply_msg)

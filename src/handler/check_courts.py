import re
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from src.handler.help import HelpHandler
from src.json_reader import MessageReader
from src.service import VacantCourtService


class CheckCourtsHandler(CommandHandler):
    def __init__(self):
        self.handler_command = "check_courts"
        self.reader = MessageReader()

        super().__init__(self.handler_command, self.check_courts_command())

    def check_courts_command(self) -> callable:
        def callback(update: Update, context: CallbackContext):
            if self.is_help(context.args):
                self.help(update)
                return
            if self.is_check_courts(context.args):
                self.check_courts(update, context)
                return
            self.reply("command_error", update, get_options={"command": context.args[0]})
        return callback

    def check_courts(self, update: Update, context: CallbackContext):
        user_id = update.message.from_user.id
        date = context.args[0]
        court = int(context.args[1])

        service = VacantCourtService()
        courts = service.check(user_id, court, date)
        if courts is None:
            self.reply("token_not_exist_error", update)
        reply_msg = service.gen_reply_msg(courts)
        self.reply(f"{self.handler_command}_main", update, get_options={"message": reply_msg})

    def is_help(self, args) -> bool:
        if args[0] == "help" and len(args) == 1:
            return True
        return False

    def is_check_courts(self, args) -> bool:
        if len(args) != 2:
            return False

        date_rule = "^(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[0-1])$"
        date = args[0]
        if not re.match(date_rule, date):
            return False

        court = args[1]
        if not court.isnumeric():
            return False
        if int(court) < 0 or int(court) > 6:
            return False
        return True

    def help(self, update: Update):
        helpHandler = HelpHandler()
        helpHandler.help_individual_command(self.handler_command, update)

    def reply(self, key, update: Update, get_options: dict={}, reply_options: dict={}):
        reply_msg = self.reader.get(key, **get_options)
        update.message.reply_text(reply_msg, **reply_options)

import re
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from src.handler.help import HelpHandler
from src.json_reader import MessageReader
from src.parser import AyeParser
from src.service import VacantCourtService


class CheckCourtsHandler(CommandHandler):
    def __init__(self, engine):
        self._engine = engine

        self.handler_command = "check_courts"
        self.reader = MessageReader()

        super().__init__(self.handler_command, self.check_courts_command())

    def check_courts_command(self) -> callable:
        def callback(update: Update, context: CallbackContext):
            parser = AyeParser(context.args)
            ret = parser.parse_check_courts()
            if ret == 0:
                self.help(update)
            elif ret == 1:
                self.check_courts(update, context)
            else:
                self.reply("command_error", update, replaced_vars={"command": context.args[0]})
        return callback

    def check_courts(self, update: Update, context: CallbackContext):
        user_id = update.message.from_user.id
        date = context.args[0]
        court = int(context.args[1])

        service = VacantCourtService(update, context, self._engine)
        courts = service.check(user_id, court, date)
        if courts is None:
            self.reply("token_not_exist_error", update)
        reply_msg = service.gen_reply_msg(courts)
        self.reply(f"{self.handler_command}_main", update, replaced_vars={"message": reply_msg})

    def help(self, update: Update):
        helpHandler = HelpHandler()
        helpHandler.help_individual_command(self.handler_command, update)

    def reply(self, key, update: Update, replaced_vars: dict = {}, reply_options: dict = {}):
        reply_msg = self.reader.get(key, **replaced_vars)
        update.message.reply_text(reply_msg, **reply_options)

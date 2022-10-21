from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from src.handler.handler import AyeHandler

from src.parser import AyeParser
from src.service import VacantCourtService


class CheckCourtsHandler(CommandHandler):
    def __init__(self, engine):
        self._h = AyeHandler(command="check_courts", engine=engine)

        super().__init__(self._h._command, self.check_courts_command())

    def check_courts_command(self) -> callable:
        def callback(update: Update, context: CallbackContext):
            parser = AyeParser(context.args)
            ret = parser.parse_check_courts()
            if ret == 0:
                self._h.help_command(self._h._command, update)
            elif ret == 1:
                self.check_courts(update, context)
            else:
                self._h.reply("command_error", update, replaced_vars={"command": context.args[0]})
        return callback

    def check_courts(self, update: Update, context: CallbackContext):
        user_id = update.message.from_user.id
        date = context.args[0]
        court = int(context.args[1])

        service = VacantCourtService(update, context, self._h._engine)
        courts = service.check(user_id, court, date)
        if courts is None:
            self._h.reply("token_not_exist_error", update)
        reply_msg = service.gen_reply_msg(courts)
        self._h.reply(f"{self._h._command}_main", update, replaced_vars={"message": reply_msg})

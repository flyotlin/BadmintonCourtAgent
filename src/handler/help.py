from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from src.handler.handler import AyeHandler

from src.parser import AyeParser


class HelpHandler(CommandHandler):
    def __init__(self, engine):
        self._h = AyeHandler(command="help", engine=engine)
        super().__init__(self._h._command, self.help_command())

    def help_command(self) -> callable:
        def callback(update: Update, context: CallbackContext):
            parser = AyeParser(context.args)
            ret = parser.parse_help()
            if ret == 0:
                self._h._logger.debug("[help]: show all commands")
                self._h.help_command("main", update, {
                    "username": update.message.from_user.username,
                    "id": update.message.from_user.id
                })
            elif ret == 1:
                self._h._logger.debug(f"[help]: show individual command <{context.args[0]}>")
                self._h.help_command(context.args[0], update)
            else:
                self._h._logger.info(f"[help]: invalid arguments <{context.args}>")
                self._h.reply("command_parse_error", update)
        return callback

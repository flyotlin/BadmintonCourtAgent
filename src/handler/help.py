from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from src.json_reader import MessageReader
from src.logger import AyeLogger
from src.parser import AyeParser


class HelpHandler(CommandHandler):
    def __init__(self, engine):
        self._engine = engine
        self._logger = AyeLogger.get()

        self.handler_command = "help"
        self.reader = MessageReader()

        super().__init__(self.handler_command, self.help_command())

    def help_command(self) -> callable:
        def callback(update: Update, context: CallbackContext):
            parser = AyeParser(context.args)
            ret = parser.parse_help()
            if ret == 0:
                self._logger.debug("[help]: show all commands")
                self.help_main(update)
            elif ret == 1:
                self._logger.debug(f"[help]: show individual command <{context.args[0]}>")
                self.help_individual_command(context.args[0], update)
            else:
                self._logger.info(f"[help]: invalid arguments <{context.args}>")
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
        except Exception:
            self._logger.info("[help]: individual command <{command}> doesn't exist")
            reply_msg = self.reader.get("help_error", command=command)
        update.message.reply_text(reply_msg)

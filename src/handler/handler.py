from telegram import Update

from src.json_reader import MessageReader
from src.logger import AyeLogger


class AyeHandler:
    def __init__(self, command: str, engine):
        self._command = command
        self._engine = engine
        self._logger = AyeLogger().get()
        self._reader = MessageReader()

    def reply(self, key: str, update: Update, replaced_vars: dict = {}, reply_options: dict = {}):
        reply_msg = self._reader.get(key, **replaced_vars)
        update.message.reply_text(reply_msg, **reply_options)

    def help_command(self, command: str, update: Update, replaced_vars: dict = {}):
        key = f"help_{command}"
        self.reply(key, update, replaced_vars=replaced_vars)

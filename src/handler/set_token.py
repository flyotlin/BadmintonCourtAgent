from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler, Filters, MessageHandler

from src.handler.help import HelpHandler
from src.json_reader import MessageReader
from src.object import User


class SetTokenHandler(ConversationHandler):
    STAGE_PHP, STAGE_XSRF, STAGE_SYS_SESSION = range(3)

    def __init__(self):
        self.handler_command = "set_token"
        self.user_in_userdata = "user"
        self.reader = MessageReader()

        regex_rules = "^.*$"
        super().__init__(
            entry_points=[CommandHandler(self.handler_command, self.set_token_command())],
            states={
                self.STAGE_PHP: [MessageHandler(Filters.regex(regex_rules), self.stage_php())],
                self.STAGE_XSRF: [MessageHandler(Filters.regex(regex_rules), self.stage_xsrf())],
                self.STAGE_SYS_SESSION: [MessageHandler(Filters.regex(regex_rules), self.stage_sys_session())]
            },
            fallbacks=[CommandHandler("cancel", self.cancel())]
        )

    def set_token_command(self) -> callable:
        def callback(update: Update, context: CallbackContext):
            args_len = len(context.args)
            if args_len == 0:
                self.reply(f"{self.handler_command}_main", update)
                return self.STAGE_PHP
            if context.args[0] == "help" and args_len == 1:
                self.help(update)
                return
            self.reply("command_error", update, replaced_vars={"command": context.args[0]})
        return callback

    def stage_php(self) -> callable:
        def callback(update: Update, context: CallbackContext) -> int:
            from_user = update.message.from_user

            user = User(from_user.username, from_user.id)
            user.set_php_session(update.message.text)
            context.user_data[self.user_in_userdata] = user

            self.reply(f"{self.handler_command}_stage_php", update)
            return self.STAGE_XSRF
        return callback

    def stage_xsrf(self) -> callable:
        def callback(update: Update, context: CallbackContext) -> int:
            user = context.user_data[self.user_in_userdata]
            user.set_xsrf_token(update.message.text)
            context.user_data[self.user_in_userdata] = user

            self.reply(f"{self.handler_command}_stage_xsrf", update)
            return self.STAGE_SYS_SESSION
        return callback

    def stage_sys_session(self) -> callable:
        def callback(update: Update, context: CallbackContext) -> int:
            user = context.user_data[self.user_in_userdata]
            user.set_system_session(update.message.text)
            user.save()
            return ConversationHandler.END
        return callback

    def cancel(self) -> callable:
        def callback(update: Update, context: CallbackContext) -> int:
            self.reply(f"{self.handler_command}_cancel", update, reply_options={
                "reply_markup": ReplyKeyboardRemove()
            })
            return ConversationHandler.END
        return callback

    def help(self, update: Update):
        helpHandler = HelpHandler()
        helpHandler.help_individual_command(self.handler_command, update)

    def reply(self, key, update: Update, replaced_vars: dict = {}, reply_options: dict = {}):
        reply_msg = self.reader.get(key, **replaced_vars)
        update.message.reply_text(reply_msg, **reply_options)

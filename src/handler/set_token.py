from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler, Filters, MessageHandler
from src.handler.handler import AyeHandler

from src.object import User
from src.parser import AyeParser


class SetTokenHandler(ConversationHandler):
    STAGE_PHP, STAGE_XSRF, STAGE_SYS_SESSION = range(3)

    def __init__(self, engine):
        self._h = AyeHandler(command="set_token", engine=engine)
        self.user_in_userdata = "user"

        regex_rules = "^.*$"
        super().__init__(
            entry_points=[CommandHandler(self._h._command, self.set_token_command())],
            states={
                self.STAGE_PHP: [MessageHandler(Filters.regex(regex_rules), self.stage_php())],
                self.STAGE_XSRF: [MessageHandler(Filters.regex(regex_rules), self.stage_xsrf())],
                self.STAGE_SYS_SESSION: [MessageHandler(Filters.regex(regex_rules), self.stage_sys_session())]
            },
            fallbacks=[CommandHandler("cancel", self.cancel())]
        )

    def set_token_command(self) -> callable:
        def callback(update: Update, context: CallbackContext):
            parser = AyeParser(context.args)
            ret = parser.parse_set_token()
            if ret == 0:
                self._h._logger.debug("[set_token]: Start the set_token conversation")
                self._h.reply(f"{self._h._command}_main", update)
                return self.STAGE_PHP
            elif ret == 1:
                self.logger.debug("[set_token]: Show help of set_token")
                self._h.help_command(self._h._command, update)
                return
            else:
                self._h._logger.info(f"[set_token]: invalid arguments <{context.args}>")
                self._h.reply("command_error", update, replaced_vars={"command": context.args[0]})
        return callback

    def stage_php(self) -> callable:
        def callback(update: Update, context: CallbackContext) -> int:
            from_user = update.message.from_user

            user = User(from_user.username, from_user.id, engine=self._h._engine)
            user.set_php_session(update.message.text)
            context.user_data[self.user_in_userdata] = user

            self._h._logger.debug(f"[set_token]: user {from_user.username}[{from_user.id}] set PHP <{update.message.text}>")
            self._h.reply(f"{self._h._command}_stage_php", update)
            return self.STAGE_XSRF
        return callback

    def stage_xsrf(self) -> callable:
        def callback(update: Update, context: CallbackContext) -> int:
            user = context.user_data[self.user_in_userdata]
            user.set_xsrf_token(update.message.text)
            context.user_data[self.user_in_userdata] = user

            self._h._logger.debug(f"[set_token]: user {user._name}[{user._user_id}] set XSRF <{update.message.text}>")
            self._h.reply(f"{self._h._command}_stage_xsrf", update)
            return self.STAGE_SYS_SESSION
        return callback

    def stage_sys_session(self) -> callable:
        def callback(update: Update, context: CallbackContext) -> int:
            user = context.user_data[self.user_in_userdata]
            user.set_system_session(update.message.text)
            user.save()
            self._h._logger.debug(f"[set_token]: user {user._name}[{user._user_id}] set SYS_SESSION <{update.message.text}>")
            return ConversationHandler.END
        return callback

    def cancel(self) -> callable:
        def callback(update: Update, context: CallbackContext) -> int:
            self._h._logger.debug(f"[set_token]: user {update.message.from_user.username} cancelled conversation")
            self._h.reply(f"{self._h._command}_cancel", update, reply_options={
                "reply_markup": ReplyKeyboardRemove()
            })
            return ConversationHandler.END
        return callback

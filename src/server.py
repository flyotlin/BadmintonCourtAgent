import configparser
from sqlalchemy.engine import Engine
from typing import TypedDict
from telegram.ext import Updater

from src.db_mgr import SqliteEngine
from src.handler.check_courts import CheckCourtsHandler
from src.handler.help import HelpHandler
from src.handler.set_token import SetTokenHandler
from src.handler.snap_court import SnapCourtHandler
from src.logger import AyeLogger


class AyeServer:
    """
    Choose either `start_polling()` or `start_webhook()`
    """
    TypeBotConf = TypedDict("TypeBotConf", {
        "token": str
    })

    def __init__(self, path: str = "") -> None:
        self._set_logger()
        self.bot_conf = self._get_bot_conf(path)
        self.updater = Updater(token=self.bot_conf["token"])
        self._set_handlers(engine=SqliteEngine.get())
        self._logger = AyeLogger.get()

    def start_polling(self):
        self._logger.debug("Start server using polling...")
        self.updater.start_polling()
        self.updater.idle()

    def start_webhook(self):
        self._logger.debug("Start server using webhook...")

    def _set_logger(self):
        AyeLogger.initialize()

    def _get_bot_conf(self, path: str):
        config = configparser.ConfigParser()
        config.read(path)
        return {
            "token": config["bot"]["token"]
        }

    def _set_handlers(self, engine: Engine):
        self.dispatcher = self.updater.dispatcher

        self.dispatcher.add_handler(CheckCourtsHandler(engine))
        self.dispatcher.add_handler(HelpHandler(engine))
        self.dispatcher.add_handler(SetTokenHandler(engine))
        self.dispatcher.add_handler(SnapCourtHandler(engine))

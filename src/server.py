import configparser
import logging
from typing import TypedDict
from telegram.ext import Updater

from src.handler.check_courts import CheckCourtsHandler
from src.handler.help import HelpHandler
from src.handler.set_token import SetTokenHandler
from src.handler.snap_courts import SnapCourtsHandler


"""
Choose either `start_polling()` or `start_webhook()`
"""
class AyeServer:
    TypeBotConf = TypedDict("TypeBotConf", {
        "token": str
    })

    def __init__(self, path: str = "") -> None:
        self._set_logger()
        self.bot_conf = self._get_bot_conf(path)
        self.updater = Updater(token=self.bot_conf["token"])
        self._set_handlers()

    def start_polling(self):
        self.updater.start_polling()
        self.updater.idle()

    def start_webhook(self):
        pass

    def _set_logger(self):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        logger = logging.getLogger(__name__)

    def _get_bot_conf(self, path: str):
        config = configparser.ConfigParser()
        config.read(path)
        return {
            "token": config["bot"]["token"]
        }

    def _set_handlers(self):
        self.dispatcher = self.updater.dispatcher

        self.dispatcher.add_handler(CheckCourtsHandler())
        self.dispatcher.add_handler(HelpHandler())
        self.dispatcher.add_handler(SetTokenHandler())
        self.dispatcher.add_handler(SnapCourtsHandler())

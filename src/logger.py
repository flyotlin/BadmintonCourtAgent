import logging
import os
import time
from logging import Formatter, StreamHandler
from logging.handlers import RotatingFileHandler


class AyeLogger:
    _logger_name = f"{__name__}_aye_logger"

    @classmethod
    def get(cls) -> logging.Logger:
        return logging.getLogger(cls._logger_name)

    @classmethod
    def initialize(cls):
        cls._set_level()
        cls._set_handler_with_formatter()

    @classmethod
    def _set_level(cls):
        logger = cls.get()
        logger.setLevel(logging.DEBUG)

    @classmethod
    def _set_handler_with_formatter(cls):
        logger = AyeLogger.get()

        # logging to stdout
        handler = cls._get_handler(StreamHandler())
        logger.addHandler(handler)

        # logging to file
        pwd = os.path.abspath(os.path.dirname(__file__))
        filename = os.path.join(pwd, "../badminton-court-agent.log")
        handler = cls._get_handler(RotatingFileHandler(
            filename=filename,
            mode="a",
            maxBytes=100*1e6,
            backupCount=10,
            encoding="utf-8",
            delay=False
        ))
        logger.addHandler(handler)

    @classmethod
    def _get_handler(cls, handler: logging.Handler):
        formatter = Formatter(
            "<%(levelname)s> -- {%(asctime)s} in {%(filename)s:%(lineno)s}: [ %(message)s ]",
            datefmt="%Y-%m-%dT%H:%M:%S+00:00"
        )
        formatter.converter = time.gmtime
        handler.setFormatter(formatter)
        return handler

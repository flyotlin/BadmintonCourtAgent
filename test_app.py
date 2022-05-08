import logging

from telegram.ext import Updater

from src.job_worker.callbacks import (
    remind_callback,
    poll_callback,
    reserve_callback
)
from src.enums import WorkerTypeEnum
from src.handler.help import HelpHandler
from src.handler.token import TokenHandler
from src.handler.check import CheckHandler
from src.handler.reserve import ReserveHandler
from src.handler.base_toggle import BaseToggle
from src.util import load_jobs_from_file


# Need to set webhook on
TOKEN = ""


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    updater = Updater(token=TOKEN)
    load_jobs_from_file(updater.job_queue)

    dispatcher = updater.dispatcher

    # telegram Bot dispatchers
    dispatcher.add_handler(HelpHandler)
    dispatcher.add_handler(TokenHandler)
    dispatcher.add_handler(CheckHandler)
    dispatcher.add_handler(ReserveHandler)
    dispatcher.add_handler(BaseToggle.get_toggle_handler("toggle_remind", remind_callback, WorkerTypeEnum.REMIND))
    dispatcher.add_handler(BaseToggle.get_toggle_handler("toggle_poll", poll_callback, WorkerTypeEnum.POLL))
    dispatcher.add_handler(BaseToggle.get_toggle_handler("toggle_reserve", reserve_callback, WorkerTypeEnum.RESERVE))

    updater.start_polling()

    updater.idle()

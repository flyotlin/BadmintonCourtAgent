import logging
import os

from telegram.ext import Updater

from src.handler.help import HelpHandler
from src.handler.token import TokenHandler
from src.handler.check import CheckHandler
from src.handler.reserve import ReserveHandler
from src.handler.toggle_poll import TogglePollHandler
from src.handler.toggle_remind import ToggleRemindHandler
from src.handler.toggle_reserve import ToggleReserveHandler
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
    dispatcher.add_handler(TogglePollHandler)
    dispatcher.add_handler(ToggleRemindHandler)
    dispatcher.add_handler(ToggleReserveHandler)

    port = int(os.environ.get('PORT', 27017))
    updater.start_webhook(listen='0.0.0.0', port=port, url_path='', webhook_url='')

    updater.idle()

import configparser
import logging
import os

from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, Updater

from src.handler.help import HelpHandler
from src.handler.token import TokenHandler
from src.handler.check import CheckHandler
from src.handler.reserve import ReserveHandler
from src.handler.toggle_poll import TogglePollHandler
from src.handler.toggle_remind import ToggleRemindHandler
from src.handler.toggle_reserve import ToggleReserveHandler
from src.util import load_jobs_from_file

# Need to set webhook on
config = configparser.ConfigParser()
config.read('.telegram-bot-token')
TELEGRAM_BOT_TOKEN = config['bot'].get('token')

# Flask server
app = Flask(__name__)

# telegram Bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Updater and Load job queues
updater = Updater(token=TELEGRAM_BOT_TOKEN)
load_jobs_from_file(updater.job_queue)

# telegram Bot dispatchers
dispatcher = Dispatcher(bot, None)
dispatcher.add_handler(HelpHandler)
dispatcher.add_handler(TokenHandler)
dispatcher.add_handler(CheckHandler)
dispatcher.add_handler(ReserveHandler)
dispatcher.add_handler(TogglePollHandler)
dispatcher.add_handler(ToggleRemindHandler)
dispatcher.add_handler(ToggleReserveHandler)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


@app.route('/webhook', methods=['POST'])
def hook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'


@app.route('/ping')
def ping():
    return ("pong", 200)


# TODO: replace flask's default http server from werkzeug to gunicorn
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 27017))
    app.run(host='0.0.0.0', port=port)

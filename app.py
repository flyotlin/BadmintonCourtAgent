import logging
import os
import telegram

from flask import Flask, request
from telegram.ext import Dispatcher

from src.handler.help import HelpHandler
from src.handler.token import TokenHandler
from src.handler.toggle_poll import TogglePollHandler

# Need to set webhook on
TOKEN = ""

# Flask server
app = Flask(__name__)

# telegram Bot
bot = telegram.Bot(token=TOKEN)

# telegram Bot dispatchers
dispatcher = Dispatcher(bot, None)
dispatcher.add_handler(HelpHandler)
dispatcher.add_handler(TokenHandler)
dispatcher.add_handler(TogglePollHandler)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


@app.route('/webhook', methods=['POST'])
def hook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'


@app.route('/ping')
def ping():
    return ("pong", 200)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 27017))
    app.run(host='0.0.0.0', port=port)

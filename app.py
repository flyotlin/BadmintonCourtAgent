import logging
import os
import telegram

from flask import Flask, request
from telegram.ext import Dispatcher

from src.handler.start import StartHandler
from src.handler.help import HelpHandler
from src.handler.check import CheckHandler
from src.handler.check_now import CheckNowHandler
from src.handler.apply import ApplyHandler
from src.handler.toggle import ToggleHandler


# Need to set webhook on
TOKEN = ""

# Flask server
app = Flask(__name__)

# telegram Bot
bot = telegram.Bot(token=TOKEN)

# telegram Bot dispatchers
dispatcher = Dispatcher(bot, None)
dispatcher.add_handler(StartHandler)
dispatcher.add_handler(HelpHandler)
dispatcher.add_handler(CheckHandler)
dispatcher.add_handler(CheckNowHandler)
dispatcher.add_handler(ToggleHandler)
dispatcher.add_handler(ApplyHandler)

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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 27017))
    app.run(host='0.0.0.0', port=port)

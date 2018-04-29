import sys

import uuid

import json

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


SERVER_MODE = False


class Config:
    _instance = None
    default_conf = 'config.json'

    def __init__(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.server = data['server']
            self.token = data['token']
            Config._instance = self

    @staticmethod
    def instance():
        if Config._instance is None:
            Config(Config.default_conf)
        return Config._instance


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def get_link(bot, update):
    """Send a message when the command /start is issued."""

    uid = uuid.UUID(update.message.chat.id)

    # TODO: Save uuid
    update.message.reply_text('{}/statistic/{}'.format(
                                    Config.instance().server,
                                    uid))

    print(update)
    print(update.message)
    print(update.message.chat.id)


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def get_message(bot, update):
    """Echo the user message."""
    # TODO: save messages
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    print('Allo')
    if len(sys.argv) > 1:
        global SERVER_MODE
        SERVER_MODE = True

    Config('config.json')

    updater = Updater(Config.instance().token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("stat", get_link))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(MessageHandler(Filters.text, get_message))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

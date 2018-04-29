import sys

from telegram import Bot
from telegram.ext import Dispatcher
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from flask import Flask

from config import Config
from handlers import get_message, get_link, help
from server import webhook_listener, get_stats

import psycopg2


conn = psycopg2.connect('postgresql://bot:12345@104.236.57.85:5432/chats')


app = Flask('StatStatBot')
app.add_url_rule('/stats/<chat_hash>', '', view_func=get_stats)

# app.run()


def setup_server(token):

    app.add_url_rule('/stats/<str:hash>', methods=['GET'], view_func=webhook_listener)

    # Create bot, update queue and dispatcher instances
    bot = Bot(token)

    dispatcher = Dispatcher(bot, None, workers=0)

    return dispatcher


def register_handlers(dispatcher):

    dispatcher.add_handler(CommandHandler("stat", get_link))
    dispatcher.add_handler(CommandHandler("help", help))

    dispatcher.add_handler(MessageHandler(Filters.text, get_message))
    return dispatcher


def setup_updater(token):
    updater = Updater(token)
    dp = updater.dispatcher
    register_handlers(dp)
    updater.start_polling()
    updater.idle()
    print('after')


def main():

    Config('config.json')

    Config.add_connection(conn)

    token = Config.instance().token
    webhook = Config.instance().is_webhook

    setup = setup_server if webhook else setup_updater

    setup(token)


if __name__ == '__main__':
    main()

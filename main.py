import psycopg2

from telegram import Bot
from telegram.ext import Dispatcher, Updater, CommandHandler,\
    MessageHandler, Filters
from flask import Flask

from lib import Config
from lib.handlers import get_message, get_link, get_help
from lib.server import webhook_listener, get_stats


conn = psycopg2.connect('postgresql://bot:12345@10.8.0.1:5432/chats')


app = Flask('StatStatBot')
app.add_url_rule('/statistic/<chat_hash>', 'stat', view_func=get_stats)


def setup_server(token):

    app.add_url_rule(Config.instance().hook_key, 'hook',
                     methods=['GET', 'POST'],
                     view_func=webhook_listener)

    bot = Bot(token)
    Config.add_bot(bot)

    s = bot.setWebhook(Config.instance().hook_url + Config.instance().hook_key,
                       certificate=open(Config.instance().cert, 'rb'))

    print('webhook setup ' + 'ok' if s else 'failed')

    dispatcher = Dispatcher(bot, None, workers=0)
    register_handlers(dispatcher)

    return dispatcher


def setup_updater(token):
    updater = Updater(token)
    dp = updater.dispatcher
    register_handlers(dp)
    updater.start_polling()

    return dp


def register_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler('stat', get_link))
    dispatcher.add_handler(CommandHandler('help', get_help))
    dispatcher.add_handler(MessageHandler(Filters.text, get_message))


def main():
    Config('config.json')
    Config.add_connection(conn)

    token = Config.instance().token
    webhook = Config.instance().is_webhook

    setup = setup_server if webhook else setup_updater
    dp = setup(token)
    Config.add_dispatcher(dp)

    app.run()


if __name__ == '__main__':
    main()

import logging
from hashlib import sha224

from config import Config
import psycopg2


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def get_link(bot, update):

    chat_id = update.message.chat.id

    salt = Config.instance().crypto_salt
    m = sha224(bytes(chat_id))
    m.update(salt.encode())

    postfix = m.hexdigest()

    conn = Config.instance().connection
    cur = conn.cursor()
    sql = """INSERT INTO links 
                    (hash, chat_id) 
              VALUES(%s, %s)"""
    try:
        cur.execute(sql, (postfix, chat_id))
    except psycopg2.IntegrityError:
        # chat already exists
        pass
    conn.commit()

    update.message.reply_text('{}/statistic/{}'.format(
                                    Config.instance().server,
                                    postfix))

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

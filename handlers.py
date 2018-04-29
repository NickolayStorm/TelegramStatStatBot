import re
import logging
from hashlib import sha224

import psycopg2

from config import Config
import utils


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
        conn.commit()
    except psycopg2.IntegrityError:
        # chat already exists
        pass

    update.message.reply_text('{}/statistic/{}'.format(
                                    Config.instance().server,
                                    postfix))

    print(update)
    print(update.message)
    print(update.message.chat.id)


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help! I need somebody help...')


def get_message(_, update):
    chat_id = update.message.chat.id
    text = update.message.text

    conn = Config.instance().connection
    cur = conn.cursor()
    sql = """CREATE TABLE IF NOT EXISTS public.chat%s (w TEXT);"""
    cur.execute(sql, (chat_id, ))

    text = re.sub(' +', ' ', text)
    # TODO: remove symbols like ! ; , .

    words = text.split(' ')

    words = filter(utils.is_good_word, words)

    args_str = ','.join(cur.mogrify('(%s)', (w,)).decode('utf-8') for w in words)
    cur.execute("INSERT INTO {} VALUES ".format('public.chat{}'
                                        .format(chat_id))
                + args_str)
    conn.commit()

    update.message.reply_text(update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

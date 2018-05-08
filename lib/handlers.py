import logging
from hashlib import sha224

import psycopg2

from lib import Config


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def get_link(_, update):

    chat_id = update.message.chat.id

    salt = Config.instance().crypto_salt
    m = sha224(bytes(abs(chat_id)))
    m.update(salt.encode())

    postfix = m.hexdigest()

    conn = Config.instance().connection
    cur = conn.cursor()
    sql = """INSERT INTO links 
                    (hash, chat_id) 
              VALUES(%s, %s)"""
    try:
        cur.execute(sql, (postfix, abs(chat_id)))
        conn.commit()
    except psycopg2.IntegrityError:
        # Chat already exists but it's okay
        conn.rollback()

    update.message.reply_text('{}/statistic/{}'.format(
                                    Config.instance().server,
                                    postfix))


def get_help(_, update):
    update.message.reply_text('Help! I need somebody help...')


def get_message(_, update):
    chat_id = abs(update.message.chat.id)
    text = update.message.text

    if not text:
        return

    conn = Config.instance().connection
    cur = conn.cursor()
    sql = """CREATE TABLE IF NOT EXISTS public.chat%s (w TEXT);"""
    cur.execute(sql, (chat_id, ))

    sql = """
    INSERT INTO public.chat{} (w) 
    SELECT lexeme FROM unnest(to_tsvector('russian', %s));
    """.format(chat_id)
    cur.execute(sql, (text, ))
    conn.commit()


def error(_, update, err):
    logger.warning('Update "%s" caused error "%s"', update, err)

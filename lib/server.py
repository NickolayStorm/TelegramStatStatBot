from flask import request
from prettytable import PrettyTable
from telegram import Update

from lib.config import Config


def get_stats(chat_hash):
    sql = 'SELECT chat_id FROM links WHERE hash = %s'
    conn = Config.instance().connection
    curs = conn.cursor()
    curs.execute(sql, (chat_hash,))
    chat_id_tuple = curs.fetchone()

    sql = """
        select count(*) as cnt, w
        from public.chat%s 
        group by w
        order by cnt desc
        limit 10;
    """
    curs.execute(sql, (abs(chat_id_tuple[0]), ))
    stats = curs.fetchall()

    table = PrettyTable()
    table.field_names = ['Count', 'Word']

    for stat in stats:
        table.add_row(stat)

    return '<font face = "serif"> ' + \
        str(table).replace('\n', '<br/>').replace(' ', '&nbsp;') + \
        '</font>'


def webhook_listener():
    if request.method == 'POST':
        bot = Config.instance().bot
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher = Config.instance().dispatcher
        dispatcher.process_update(update)
    return 'ok'

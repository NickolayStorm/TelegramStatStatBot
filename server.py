from flask import request

from config import Config


def get_stats(chat_hash):
    sql = 'SELECT chat_id FROM links WHERE hash = %s'
    curs = Config.instance().cursor
    curs.execute(sql, (chat_hash,))
    print(curs.fetchall())
    return 'stats for' + chat_hash


def webhook_listener():
    print('Hocked')
    if request.method == "POST":
        print(request.get_json())
        # retrieve the message in JSON and then transform it to Telegram object
        # update = telegram.Update.de_json(request.get_json(force=True))
        #
        # chat_id = update.message.chat.id
        #
        # # Telegram understands UTF-8, so encode text for unicode compatibility
        # text = update.message.text.encode('utf-8')
        #
        # # repeat the same message back (echo)
        # bot.sendMessage(chat_id=chat_id, text=text)

    return 'ok'

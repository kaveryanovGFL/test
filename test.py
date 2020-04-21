# new
from settings import token, admin_id, url, login, password, db_name

'''use pip install python-telegram-bot apiai pytube --upgrade'''
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,\
    MessageHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext.dispatcher import run_async
import MySQLdb
import gc

updater = Updater(token=token)
dispatcher = updater.dispatcher

'Create queries'
select_query = "select chat_id from users"
insert_query = """insert into users(chat_id, name) values (%s, %s);"""

'Create text answer'
cancel_text = "Жаль, но не смогу"
starts_day_text = {"first": "Провожу уколы", "inter": "и"}
answer_user_on_day_text = {"first": "Запись от", "inter": "на дату"}
new_user_text = "Хорошо, я сообщу когда будет запись"
new_user_exist_text = "Вы уже подписаны, я сообщу когда будет запись"
cancel_answer_text = "Жаль, ждем в след раз"
complite_answer = "Поздравляем вы записаны"
message_from_user = "Сообщение от"
'new comment'

def query_to_DB(sql_select_Query, user_data=None):
    print(user_data)
    try:
        db = MySQLdb.connect(url, login, password, db=db_name)
        cursor = db.cursor()
        if user_data is None:
            print("None")
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()
            list_chat_ids = [list(i)[0] for i in records]
            return list_chat_ids
        else:
            print("else")
            cursor.execute(sql_select_Query, user_data)
            db.commit()
    except MySQLdb.Error as e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
    finally:
        db.close()
        gc.collect()


def start(bot, update):
    chat_id = update.message.chat_id
    name = update.effective_user.name
    'Get all chat_ids'
    list_chat_ids = query_to_DB(select_query)

    if chat_id == admin_id:
        days = [int(s) for s in update.message.text.split() if s.isdigit()]
        start_day = days[0]
        end_day = days[1]
        keyboard = [[InlineKeyboardButton(start_day, callback_data=start_day),
                    InlineKeyboardButton(end_day, callback_data=end_day)],
                    [InlineKeyboardButton(cancel_text, callback_data="No")]]

        reply_mark = InlineKeyboardMarkup(keyboard)
        for chat_ids in list_chat_ids:
            bot.send_message(chat_ids, "{first} {} {inter} {}".format(
                start_day, end_day, **starts_day_text), reply_markup=reply_mark)
    else:
        if chat_id not in list_chat_ids:
            query_to_DB(insert_query, (chat_id, name))
            bot.send_message(chat_id=chat_id, text=new_user_text)
        else:
            bot.send_message(chat_id=chat_id, text=new_user_exist_text)


def answer(bot, update):
    answer = update.callback_query.data
    if answer == ("No"):
        update.callback_query.edit_message_text(cancel_answer_text)
    else:
        update.callback_query.edit_message_text(complite_answer)
        bot.send_message(chat_id=admin_id, text="{first} {} {inter} {}".format(
            update.effective_user.name, answer, **starts_day_text))


@run_async
def textMessage(bot, update):
    bot.send_message(chat_id=admin_id, text="{} {}:\n{}".format(
        message_from_user, update.effective_user.name, update.message.text))


def main():
    '''Create comand'''
    start_command_handler = CommandHandler('start', start)
    answer_command_handler = CallbackQueryHandler(answer)
    text_message_handler = MessageHandler(Filters.text, textMessage)
    ''' Add hendlers in dispetcher '''
    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(answer_command_handler)
    dispatcher.add_handler(text_message_handler)
    ''' Find Update '''
    updater.start_polling(clean=True)
    ''' Close bot if push Ctrl + C '''
    updater.idle()


if __name__ == '__main__':
    main()

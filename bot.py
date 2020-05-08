# -*- coding: utf-8 -*-
from settings import token, file_path, confirm_text, registred_user, end_work
from yobit import price, etherium
''' For install telegram.ext and apiai use
    pip3 install python-telegram-bot pytube3 apiai --upgrade'''
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async
import apiai
import json
from time import sleep
# from pytube import YouTube
import requests as req
from bs4 import BeautifulSoup

chat_ids = [line.split(',') for line in open(r"{}".format(file_path), 'r')]
chat_ids = [int(i) for i in chat_ids[0]]
updater = Updater(token=token)
dispatcher = updater.dispatcher

# test 8
@run_async
def startCommand(bot, update):
    if (update.message.chat_id not in chat_ids):
        chat_ids.append(update.message.chat_id)
        f = open(r"{}".format(file_path), "w")
        f.write(str(chat_ids).replace(
            '[', '').replace(']', '').replace('\n', ''))
        f.close()
        print('new user = {}'.format(chat_ids))
        bot.send_message(chat_id=update.message.chat_id, text=confirm_text)
    else:
        bot.send_message(chat_id=update.message.chat_id, text=registred_user)
    schek(bot, update)


@run_async
def stopCommand(bot, update):
    if (update.message.chat_id in chat_ids):
        chat_ids.remove(update.message.chat_id)
        f = open(r"{}".format(file_path), "w")
        f.write(str(chat_ids).replace(
            '[', '').replace(']', '').replace('\n', ''))
        f.close()
        print('dell user = {}'.format(chat_ids))
    bot.send_message(chat_id=update.message.chat_id, text=end_work)


@run_async
def schek(bot, update):
    old_price = round(int(etherium().split('\n')[6].split(' - ')[0]))
    while True:
        new_prise = round(int(etherium().split('\n')[6].split(' - ')[0]))
        if (old_price != new_prise):
            old_price = new_prise
            for id in chat_ids:
                bot.send_message(chat_id=id, text=etherium())
        sleep(60 * 5)


@run_async
def ethCommand(bot, update):
    '''Send ETH price in good view'''
    bot.send_message(chat_id=update.message.chat_id,
                     text=price('ETH_USD', 'Эфира'))


@run_async
def bitcCommand(bot, update):
    '''Send BTC price in good view'''
    bot.send_message(chat_id=update.message.chat_id,
                     text=price('BTC_USD', 'Биткоина'))


@run_async
def nodCommand(bot, update):
    '''Send key for NOD 32'''
    just_key = set()
    key = False
    url = r"http://sovet-v-svet.blogspot.com/2019/01/2019-2020-32-nod32-free-keys-for-nod-32.html"
    nod_keys = req.get(url)
    soup = BeautifulSoup(nod_keys.content, 'html.parser')
    table = soup.find('div', {'dir': 'ltr'})
    for child in table.findChildren('span'):
        if "для всех версий!!!" in str(child).lower():
            key = True
        if "пароль" in str(child).lower():
            break

        if key and child.find('b') is not None and '-' in child.find('b').text:
            just_key.add(child.find('b').text.strip())
    text = ''.join(str(e) + '\n' for e in list(just_key))
    bot.send_message(chat_id=update.message.chat_id, text=text)


@run_async
def textMessage(bot, update):
    request = apiai.ApiAI('1490c47f27114f9bbe4e305754273f22').text_request()
    request.lang = 'ru'
    request.session_id = 'BatlabAIBot'
    request.query = update.message.text
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']
    if 'http' in update.message.text:
        pass
        # yt = YouTube(update.message.text)
        # name = strftime("%Y%m%d")
        # yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        # yt.download(filename=name)
        # bot.send_document(chat_id=update.message.chat_id, document=open(name + '.mp4', 'rb'), timeout=100)
        # os.remove(name + '.mp4')
    else:
        if response:
            bot.send_message(chat_id=update.message.chat_id, text=response)
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text='Я Вас не совсем понял!')


def main():
    '''Create comand'''
    start_command_handler = CommandHandler('start', startCommand)
    stop_command_handler = CommandHandler('stop', stopCommand)
    eth_command_handler = CommandHandler('eth', ethCommand)
    bitc_command_handler = CommandHandler('bitc', bitcCommand)
    nod_command_handler = CommandHandler('nod', nodCommand)
    text_message_handler = MessageHandler(Filters.text, textMessage)
    ''' Add hendlers in dispetcher '''
    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(stop_command_handler)
    dispatcher.add_handler(eth_command_handler)
    dispatcher.add_handler(bitc_command_handler)
    dispatcher.add_handler(nod_command_handler)
    dispatcher.add_handler(text_message_handler)
    ''' Find Update '''
    updater.start_polling(clean=True)
    ''' Close bot if push Ctrl + C '''
    updater.idle()


if __name__ == '__main__':
    main()

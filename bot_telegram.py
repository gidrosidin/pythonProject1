import telebot
from stuff import *  # импортировать все функции из файла stuff.py

import os

bot = telebot.TeleBot(os.environ.get('KEY'))

answers = {
    'git': 'Введи запрос для поиска в формате "GIT Запрос Язык_Программирования" и я дам тебе ссылки на 5 случайных репозиториев',
    'help': 'Я умею искать по гитхабу и повторять слова за тобой. Чтобы узнать, как искать, напиши мне слово git',
}


@bot.message_handler(commands=['start', 'help', 'dog'])
def commands(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, f'Привет, {message.chat.username}!')
    elif message.text == '/help':
        bot.send_message(message.chat.id, answers['help'])
    elif message.text == '/dog':
        img = get_image()
        bot.send_photo(message.chat.id, photo=img)


@bot.message_handler(commands=['button'])
def button_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Поделиться номером телефона', request_contact=True)
    btn2 = telebot.types.KeyboardButton('Поделиться локацией', request_location=True)
    markup.add(btn1)
    markup.add(btn2)
    bot.send_message(message.chat.id, 'Хочешь поделиться телефоном или локацией?', reply_markup=markup)


@bot.message_handler(content_types=['contact', 'location'])
def contact(message):
    if message.contact is not None:  # если в сообщении были отправлены контактные данные пользователя
        print(message.contact)
    elif message.location is not None:
        city = get_city(message.location.latitude, message.location.longitude)
        bot.send_message(message.chat.id, f'Your city is {city}')


@bot.message_handler(content_types=['text'])  # декоратор
def repeat_message(message):
    if message.text.startswith('GIT'):
        msg = message.text.split()
        res = git_search(msg[1], msg[2])
        msg = "Вот, что я смог найти:\n" + res
        bot.send_message(message.chat.id, text=msg, parse_mode='html')

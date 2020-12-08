import telebot
from db import database_sqlite

from telebot import types

bot = telebot.TeleBot("1400204569:AAE41mIqzjsH6JQHmdg2ZWW-EODWgvOUKjI")

name = " "
surname = " "
age = 0
user_id = -1
score = 0


@bot.message_handler(commands=['start'])
def menu(message):
    global user_id
    user_id = message.from_user.id
    print(user_id)
    bot.reply_to(message, "Выбери вариант из меню")
    menu1 = types.InlineKeyboardMarkup()
    key_reg = types.InlineKeyboardButton(text='Регистрация', callback_data='reg')
    menu1.add(key_reg)
    bot.send_message(message.chat.id, text="Меню", reply_markup=menu1)


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


def reg_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "Фамилия?")
    bot.register_next_step_handler(message, reg_surname)


def reg_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, "Сколько лет назад вылупился?")
    bot.register_next_step_handler(message, reg_age)


def reg_age(message):
    global age

    try:
        age = int(message.text)
        bot.send_message(message.from_user.id, "Отлично")
    except Exception:
        bot.send_message(message.from_user.id, "Цифры плиз")
        bot.register_next_step_handler(message, reg_age)

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='YES', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='NO', callback_data='no')
    keyboard.add(key_no)

    bot.send_message(message.from_user.id,
                     text='Информаци верна?\n Имя {name}\n Фамилия {surname}\n Возраст {age}'.format(name=name,
                                                                                                     surname=surname,
                                                                                                     age=age),
                     reply_markup=keyboard)
    return 0


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.from_user.id, 'Привет {name}'.format(name=name))
        search_or_save_users(user_id, name, surname, age, score)
    elif call.data == "no":
        bot.send_message(call.from_user.id, "Давай по новой")
        bot.send_message(call.from_user.id, "Дороу.Как звать это чудо?")
        bot.register_next_step_handler(call.message, reg_name)
    elif call.data == "reg":
        bot.send_message(call.from_user.id, "Поихалы")
        print(bot.ef)
        bot.send_message(call.from_user.id, "Дороу.Как звать это чудо?")
        bot.register_next_step_handler(call.message, reg_name)


bot.polling()

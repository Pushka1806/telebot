import telebot

from db.database_sqlite import *
from config import *
from telebot import types

bot = telebot.TeleBot(TOKEN)
dima_id = 665665811
artem_id = 800987769
artur_id = 580910189

_doc = False
_error = False
error_count = 0


def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None


@bot.message_handler(commands=['start'])
def first_massage(message):
    unique_code = extract_unique_code(message.text)
    print(type(unique_code))
    print(type(message.from_user.id))
    print(unique_code == message.from_user.id)
    if unique_code and int(unique_code) != message.from_user.id:
        value = 200
        multiple_score(user_id=unique_code, value=value)
        add_referral(user_id=unique_code)
        bot.send_message(unique_code, f"Вам было зачислено {value} баллов ")

    bot.send_message(message.from_user.id, "Привет, это тестовый телеграм бот")
    bot.send_message(message.from_user.id, "Начнём")
    bot.send_message(message.from_user.id, "Нажми на /menu")


@bot.message_handler(commands=['menu'])
def menu(message):
    global _doc
    global _error

    _doc = False
    _error = False
    # user_id = message.from_user.id
    print(message.from_user.id)

    init_db()
    print(44444444)
    if cheсk_id(user_id=message.from_user.id) == 0:
        add_user(user_id=message.from_user.id, name=message.from_user.first_name, surname=message.from_user.last_name,
                 score=0)
    menu1 = types.InlineKeyboardMarkup()
    key_score = types.InlineKeyboardButton(text='Ваши баллы', callback_data='score')
    key_document = types.InlineKeyboardButton(text='Прикрепить документ\n или фотографию', callback_data='document')
    key_error = types.InlineKeyboardButton(text='Сообщить об ошибке', callback_data='error')
    key_price = types.InlineKeyboardButton(text='Prices', callback_data='price')
    key_loyalty = types.InlineKeyboardButton(text='Лояльность', callback_data='loyalty')
    menu1.add(key_price)
    menu1.add(key_loyalty)
    menu1.add(key_document)
    menu1.add(key_score)
    menu1.add(key_error)
    bot.send_message(message.chat.id, text="Меню", reply_markup=menu1)


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    global _error
    if _error:
        bot.send_message(message.from_user.id, "Спасибо, ваше сообщение будет отправлено автору")
        bot.forward_message(artur_id, message.chat.id, message.message_id)
        multiple_score(user_id=message.from_user.id, value=100)
        bot.send_message(message.from_user.id, "Вам было зачислено 100 баллов ")
        bot.send_message(message.from_user.id, "Выберите меню /menu")

    else:

        bot.send_message(message.from_user.id, "Выберите меню /menu")


@bot.message_handler(func=lambda _error: True, content_types=['document', 'photo'])
def komp(message):
    global _doc
    if _error == True:
        bot.send_message(message.from_user.id, "Спасибо, ваше сообщение будет отправлено автору")
        bot.forward_message(artur_id, message.chat.id, message.message_id)
        multiple_score(user_id=message.from_user.id, value=100)
        bot.send_message(message.from_user.id, 'Выберите /menu')

    elif _doc:
        bot.forward_message(artem_id, message.chat.id, message.message_id)
        multiple_score(user_id=message.from_user.id, value=100)
        bot.send_message(message.from_user.id, "100 баллов зачислено")
        bot.send_message(message.from_user.id, 'Выберите /menu')
        _doc = False

    else:
        bot.send_message(message.from_user.id, "Чтобы отправить файл, выберите пункт меню /menu")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "score":
        bot.send_message(call.from_user.id, "Количество баллов:")
        bot.send_message(call.from_user.id, check_score(user_id=call.from_user.id))
        bot.send_message(call.from_user.id, "Для продолжения введите /menu")
    elif call.data == "document":
        global _doc
        _doc = True
        bot.send_message(call.from_user.id, "В описании можете добавить информацию к редактированию")
        bot.send_message(call.from_user.id, "Для отмены выберите /menu")
    elif call.data == "price":
        bot.send_message(call.from_user.id,
                         "Печать за страницу:       15к\nC вашими листами: 10к\nВ разделе Лояльность можете ознакомиться со списком скидок")
        bot.send_message(call.from_user.id, "Для продолжения введите /menu")

    elif call.data == "error":
        global _error
        _error = True
        global error_count
        error_count += 1
        bot.send_message(call.from_user.id, 'Номер ошибки {error}'.format(error=error_count))
        bot.send_message(call.from_user.id,
                         "Раскажи мне об возникшей ошибке или прикрепи скриншот,в описании укажи номер ошибки")
        bot.send_message(call.from_user.id, "Для отмены выберите /menu")
    elif call.data == "loyalty":
        loyal_url = types.InlineKeyboardMarkup()
        key_url = types.InlineKeyboardButton(text='Получить ссылку', callback_data='_loyal_url')
        loyal_url.add(key_url)
        bot.send_message(call.from_user.id, text="Ссылка", reply_markup=loyal_url)

        bot.send_message(call.from_user.id, "Для продолжения введите /menu")
    elif call.data == "_loyal_url":
        bot.send_message(call.from_user.id, "Отправьте ссылку другу и при его регистрации получите баллы")
        bot.send_message(call.from_user.id, 't.me/test_shrek_bot?start=580910189')


bot.infinity_polling()

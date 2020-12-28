def reg_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "Фамилия?")
    bot.register_next_step_handler(message, reg_surname)


def reg_surname(message):
    global surname
    surname = message.text

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='YES', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='NO', callback_data='no')
    keyboard.add(key_no)

    bot.send_message(message.from_user.id,
                     text='Информаци верна?\n Имя           {name}\n Фамилия  {surname}'.format(name=name,
                                                                                                surname=surname
                                                                                                ),
                     reply_markup=keyboard)



    elif call.data == "reg":
        name = call.from_user.first_name
        surname = call.from_user.last_name
        bot.send_message(call.from_user.id, "Поихалы")
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='YES', callback_data='yes')
        keyboard.add(key_yes)
        key_no = types.InlineKeyboardButton(text='NO', callback_data='no')
        keyboard.add(key_no)

        bot.send_message(call.from_user.id,
                         text='Информаци верна?\n Имя           {name}\n Фамилия  {surname}'.format(
                             name=name,
                             surname=surname
                         ),
                         reply_markup=keyboard)


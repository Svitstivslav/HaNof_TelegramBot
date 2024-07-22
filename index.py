import telebot
import webbrowser
from telebot import types


bot = telebot.TeleBot("7281571554:AAFGSCBhJqq0ver_I8KnZLBZmJOeC_Rkh7U")


# @bot.message_handler()
# def info(message):
#     if message.text.lower() == 'привет':
#         bot.send_message(
#             message.chat.id,
#             f'Привет, {message.from_user.first_name}'
#         )
#     else:
#         bot.send_message(
#             message.chat.id,
#             'выбирете команду из списка',
#             # reply_markup=keyboard
#         )

# Перенаправляем на сайт
@bot.message_handler(commands=['site'])
def site(message):
    webbrowser.open('https://hanof.pro/')


# Отвечаем на команды
# @bot.message_handler(commands=['start'])
# def start_message(message):
#     bot.send_message(
#         message.chat.id,
#         f'<b>Привет, {message.from_user.first_name}</b>',
#         parse_mode='html'
#     )


# Принемаем файл фото
@bot.message_handler(content_types=['photo'])
def get_photo(message):
    bot.reply_to(message, 'Фото успешно отправлено')


# Создание кнопак
# под сообщением
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на сайт', url='https://hanof.pro/')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('Рассчитать стоимость', callback_data='calculate')
    btn3 = types.InlineKeyboardButton('Сотрудничество', callback_data='cooperation')
    markup.row(btn2, btn3)
    # Отправляем файл пользователю
    btn4 = types.InlineKeyboardButton('отправь мне фото', callback_data='photo')
    markup.row(btn4)
    

    bot.reply_to(message, 'Привет, я бот компании HaNofPro. Чем могу вам помочь?', reply_markup=markup)


# Обработка функции из callback_data
@bot.callback_query_handler(func=lambda callback: True)
def callback_query(callback):
    if callback.data == 'calculate':
        bot.send_message(callback.message.chat.id, 'Выбери валюту')
    elif callback.data == 'cooperation':
        bot.send_message(callback.message.chat.id, 'Связаться со мной')
    elif callback.data == 'photo':
        file = open('photo/photo.jpeg', 'rb')
        bot.send_photo(callback.message.chat.id, file)


bot.polling(none_stop=True)

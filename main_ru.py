import telebot
# from config import TOKEN, SVIT_ID, ANTON_ID
import webbrowser
from telebot import types
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


bot = telebot.TeleBot(os.getenv('TOKEN'))


@bot.message_handler(commands=['site'])
def site_message(message):
    webbrowser.open('https://hanof.pro/')


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(
        'Перейти на сайт',
        url='https://hanof.pro/'
    )
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton(
        'Отправить заявку',
        callback_data='application'
        )
    markup.row(btn2)
    bot.reply_to(
        message,
        'Привет, я бот компании HaNofPro. Чем могу вам помочь?',
        reply_markup=markup
        )


@bot.callback_query_handler(func=lambda callback: True)
def callback_start_query(callback):
    if callback.data == 'application':
        bot.send_message(
            callback.message.chat.id,
            'Отправте фото окна, которое вы хотите изменить.',
        )


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Запрашиваем имя пользователя
    msg = bot.reply_to(
        message,
        'Пожалуйста, введите ваше имя:'
        )
    bot.register_next_step_handler(
        msg,
        process_name_step,
        message.photo[-1].file_id
        )


def process_name_step(message, file_id):
    name = message.text
    # Запрашиваем фамилию пользователя
    msg = bot.reply_to(
        message,
        'Пожалуйста, введите вашу фамилию:'
        )
    bot.register_next_step_handler(
        msg,
        process_surname_step,
        name,
        file_id
        )


def process_surname_step(message, name, file_id):
    surname = message.text
    # Запрашиваем контактную информацию пользователя
    msg = bot.reply_to(
        message,
        'Пожалуйста, введите ваш номер телефона:'
        )
    bot.register_next_step_handler(
        msg,
        process_contact_info_step,
        name,
        surname,
        file_id
        )


def process_contact_info_step(message, name, surname, file_id):
    contact_info = message.text
    # Запрашиваем материал подоконника
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Дерево', 'Пластик', 'Камень')
    msg = bot.reply_to(
        message,
        'Пожалуйста, выберите материал подоконника:',
        reply_markup=markup
        )
    bot.register_next_step_handler(
        msg,
        process_material_step,
        name,
        surname,
        contact_info,
        file_id
        )


def process_material_step(message, name, surname, contact_info, file_id):
    material = message.text
    # Запрашиваем размер подоконника
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(
        'до 1.5м',
        'до 2.5м',
        'более 2.5м'
        )
    msg = bot.reply_to(
        message,
        'Пожалуйста, выберите размер подоконника:',
        reply_markup=markup
        )
    bot.register_next_step_handler(
        msg,
        process_size_step,
        name,
        surname,
        contact_info,
        material,
        file_id
        )


def process_size_step(
        message,
        name,
        surname,
        contact_info,
        material,
        file_id
        ):
    size = message.text
    # Отправляем фото и данные в чат SVIT_ID и ANTON_ID
    bot.send_photo(
        os.getenv('SVIT_ID'),
        file_id,
        caption={f'Имя: {name}'
                 f'\nФaмилия: {surname}'
                 f'\nКонтaктная информация: {contact_info}'
                 f'\nМатериал: {material}'
                 f'\nРазмер: {size}'
                 }
        )
    # bot.send_photo(
    #     os.getenv('ANTON_ID'),
    #     file_id,
    #     caption={f'Имя: {name}'
    #              f'\nФaмилия: {surname}'
    #              f'\nКонтaктная информация: {contact_info}'
    #              f'\nМатериал: {material}'
    #              f'\nРазмер: {size}'
    #              }
    #     )
    bot.send_message(
        message.chat.id,
        'Ваше фото и данные были успешно отправлены.'
        )


bot.polling(none_stop=True)

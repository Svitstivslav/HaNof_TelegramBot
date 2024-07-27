import telebot
import webbrowser
from telebot import types
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


bot = telebot.TeleBot(os.getenv('TOKEN_HW'))


@bot.message_handler(commands=['site'])
def site_message(message):
    webbrowser.open('https://hanof.pro/')


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(
        'עבור אל האתר',
        url='https://hanof.pro/'
    )
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton(
        'שלח בקשה',
        callback_data='application'
        )
    markup.row(btn2)
    bot.reply_to(
        message,
        'היי, אני בוט של חברת HaNofPro. איך אוכל לעזור לך?',
        reply_markup=markup
        )


@bot.callback_query_handler(func=lambda callback: True)
def callback_start_query(callback):
    if callback.data == 'application':
        bot.send_message(
            callback.message.chat.id,
            'שלח תמונה של החלון שברצונך לשנות.',
        )


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Запрашиваем имя пользователя
    msg = bot.reply_to(
        message,
        'שם פרטי:'
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
        'שם משפחה:'
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
        'מספר טלפון:'
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
    markup.add('עץ', 'פלסטיק', 'אבן')
    msg = bot.reply_to(
        message,
        'אנא בחר את חומר אדן החלון:',
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
        'עד 1.5 מטר',
        'עד 2.5 מטר',
        'יותר מ 2.5'
        )
    msg = bot.reply_to(
        message,
        'לבחור את גודל של אדן החלון:',
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
        'תמונות ונתונים נשלחו בהצלחה.'
        )


bot.polling(none_stop=True)

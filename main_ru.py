import telebot
import webbrowser
from telebot import types
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


bot = telebot.TeleBot(os.getenv('TOKEN'))


# Декоратор. При нажатие /start, кидает на старт.
# При нажатие /site кидает на сайт.
def restart_on_start(func):
    def wrapper(message, *args, **kwargs):
        if message.text == '/start':
            return start_message(message)
        elif message.text == '/site':
            return site_message(message)
        else:
            return func(message, *args, **kwargs)
    return wrapper


@bot.message_handler(commands=['site'])
def site_message(message):
    webbrowser.open('https://hanof.pro/')


# Просим пользователя выбрать язык.
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('На русском', 'בעברית')
    msg = bot.send_message(
        message.chat.id,
        'Выберите язык / בחר שפה:',
        reply_markup=markup
        )
    bot.register_next_step_handler(
        msg,
        process_language_choice
        )


# Обрабатываем выбор языка и записываем его
# в ru, где true = ru а false = hw.
def process_language_choice(message):
    ru = None
    if message.text == 'На русском':
        ru = True
    elif message.text == 'בעברית':
        ru = False
    bot.send_message(
        message.chat.id,
        'Это автоматический бот. Мы зададим несколько'
        ' вопросов и свяжемся с Вами в ближайшее время.' if ru else
        'זהו בוט אוטומטי. נשאל מספר שאלות'
        ' וניצור איתך קשר בקרוב.',
    )
    name_question(message, ru)


# Выесняем имя пользователя.
def name_question(message, ru):
    msg = bot.send_message(
        message.chat.id,
        'Как вас зовут?' if ru else 'איך קוראים לך?',
    )
    bot.register_next_step_handler(
        msg,
        process_name_step,
        ru,
    )


# Собираем данные имени. Спрашиваем о городе.
@restart_on_start
def process_name_step(message, ru):
    user_data = {'name': message.text}
    msg = bot.send_message(
        message.chat.id,
        'Город?' if ru else 'עיר?'
    )
    bot.register_next_step_handler(
        msg,
        process_city_step,
        user_data,
        ru,
        )


# Собираем данные города. Спрашиваем о номере телефона.
@restart_on_start
def process_city_step(message, user_data, ru):
    user_data['city'] = message.text
    msg = bot.send_message(
        message.chat.id,
        'Номер телефона?' if ru else 'מספר טלפון?'
    )
    bot.register_next_step_handler(
        msg,
        process_phone_step,
        user_data,
        ru,
        )


# Собираем данные телефона. Спрашиваем о цвете.
@restart_on_start
def process_phone_step(message, user_data, ru):
    user_data['phone'] = message.text
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(
        'Под дерево' if ru else 'עץ',
        'Под камень' if ru else 'אבן',
        'Однотонный цвет (выбор при заказе)' if ru else
        'מוצק צבע (בחירה בעת הזמנה)',
        )
    msg = bot.send_message(
        message.chat.id,
        'Цвет подоконника:' if ru else 'צבע אדן החלון:',
        reply_markup=markup,
        )
    bot.register_next_step_handler(
        msg,
        process_color_step,
        user_data,
        ru,
        )


# Собираем данные разцветки. Спрашиваем о количестве ПД.
@restart_on_start
def process_color_step(message, user_data, ru):
    user_data['color'] = message.text
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(
        '1 подоконник' if ru else '1 אדן החלון',
        '2 - 3 подоконника' if ru else '2-3 אדני חלונות',
        'Более 3-х подоконников' if ru else 'יותר מ -3 אדני חלונות',
        )
    msg = bot.send_message(
        message.chat.id,
        'Количество:' if ru else 'כמות:',
        reply_markup=markup,
        )
    bot.register_next_step_handler(
        msg,
        process_quantity_step,
        user_data,
        ru,
        )


# Собираем данные количества ПД. Спрашиваем о длине.
@restart_on_start
def process_quantity_step(message, user_data, ru):
    user_data['quantity'] = message.text
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(
        '1 - 1.5 метра' if ru else '1-1.5 מטר',
        '1.5 - 2.5 метра' if ru else '1.5-2.5 מטר',
        'Более 2.5 метров' if ru else 'יותר מ 2.5 מטרים',
        'Разные размеры подоконников' if ru else 'גדלים שונים של אדני חלונות',
        )
    msg = bot.send_message(
        message.chat.id,
        'Длина подоконника:' if ru else 'אורך אדן החלון:',
        reply_markup=markup
        )
    bot.register_next_step_handler(
        msg,
        process_length_step,
        user_data,
        ru,
        )


# Собираем данные длины. Спрашиваем о способе связи.
@restart_on_start
def process_length_step(message, user_data, ru):
    user_data['length'] = message.text
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(
        'Телефонный звонок' if ru else 'שיחת טלפון',
        'Сообщение в телеграм' if ru else 'הודעה בטלגרם',
        )
    msg = bot.send_message(
        message.chat.id,
        'Выберите удобный способ получения ответа:' if ru else
        'בחר דרך נוחה לקבל תשובה:',
        reply_markup=markup)
    bot.register_next_step_handler(
        msg,
        process_contact_method_step,
        user_data,
        ru,
        )


# Собираем данные о способе связи. Двигаем данные в send_application.
def process_contact_method_step(message, user_data, ru):
    user_data['contact_method'] = message.text
    send_application(message, user_data, ru)


# Отправляем все данные менеджеру, и сообщение заказчику.
def send_application(message, user_data, ru):
    user_info = f"<b>Имя:</b> {user_data['name']}\n" \
                f"<b>Город:</b> {user_data['city']}\n" \
                f"<b>Телефон:</b> {user_data['phone']}\n" \
                f"<b>Цвет подоконника:</b> {user_data['color']}\n" \
                f"<b>Количество:</b> {user_data['quantity']}\n" \
                f"<b>Длина:</b> {user_data['length']}\n" \
                f"<b>Способ связи:</b> {user_data['contact_method']}\n" \
                f"<b>Ссылка на пользователя:</b>\n" \
                f"https://t.me/{message.from_user.username}",

    bot.send_message(os.getenv('SVIT_ID'), user_info, parse_mode='html')
    bot.send_message(os.getenv('ANTON_ID'), user_info, parse_mode='html')

    bot.send_message(
        message.chat.id,
        f"Спасибо, {user_data['name']}. "
        f"Ваша заявка принята в работу."
        f"В ближайшее время с вами свяжется "
        f"менеджер для уточнения деталей.\n" if ru else
        f"תודה, {user_data['name']}. "
        f"הבקשה שלך התקבלה לעבודה."
        f"בקרוב תיצור איתך קשר עם המנהל לקבלת פרטים נוספים.\n",
        )
    last_message(message, ru)


def last_message(message, ru):
    bot.send_message(
        message.chat.id,
        "Хорошего дня! Ваш ХаНофПро." if ru else
        "שיהיה לך יום טוב! הנוף-פרו שלך!",
    )


bot.polling(none_stop=True)

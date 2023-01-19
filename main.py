import telebot
from config import TOKEN
import random
import requests
import logging
from config import weather_token
from telebot import types
from bs4 import BeautifulSoup

from pyowm import OWM



bot = telebot.TeleBot(TOKEN)

logging.basicConfig(format='%(asctime)s - %(levelname)s -%(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )





@bot.message_handler(commands=['start'])
def welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton('Рандомное число')
    item2 = telebot.types.KeyboardButton('Погода')
    item3 = telebot.types.KeyboardButton('Гороскоп')
    item4 = telebot.types.KeyboardButton('Анекдоты')
    item5 = telebot.types.KeyboardButton('НЕ НАЖИМАЙ СЮДА')
    item6 = telebot.types.KeyboardButton('Игра в слова')

    markup.add(item1, item2, item3, item4, item5)

    bot.send_message(message.chat.id, 'Добро пожаловать! Выберите нужный пункт меню' , reply_markup=markup)





@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    logging.info('Start bot')
    # Если написали «Привет»
    if message.text == "Гороскоп":
        # Пишем приветствие
        bot.send_message(message.from_user.id, "Привет, сейчас я расскажу тебе гороскоп на сегодня.")
        # Готовим кнопки
        keyboard = types.InlineKeyboardMarkup()
        # По очереди готовим текст и обработчик для каждого знака зодиака
        key_oven = types.InlineKeyboardButton(text='Овен', callback_data='zodiac')
        # И добавляем кнопку на экран
        keyboard.add(key_oven)
        key_telec = types.InlineKeyboardButton(text='Телец', callback_data='zodiac')
        keyboard.add(key_telec)
        key_bliznecy = types.InlineKeyboardButton(text='Близнецы', callback_data='zodiac')
        keyboard.add(key_bliznecy)
        key_rak = types.InlineKeyboardButton(text='Рак', callback_data='zodiac')
        keyboard.add(key_rak)
        key_lev = types.InlineKeyboardButton(text='Лев', callback_data='zodiac')
        keyboard.add(key_lev)
        key_deva = types.InlineKeyboardButton(text='Дева', callback_data='zodiac')
        keyboard.add(key_deva)
        key_vesy = types.InlineKeyboardButton(text='Весы', callback_data='zodiac')
        keyboard.add(key_vesy)
        key_scorpion = types.InlineKeyboardButton(text='Скорпион', callback_data='zodiac')
        keyboard.add(key_scorpion)
        key_strelec = types.InlineKeyboardButton(text='Стрелец', callback_data='zodiac')
        keyboard.add(key_strelec)
        key_kozerog = types.InlineKeyboardButton(text='Козерог', callback_data='zodiac')
        keyboard.add(key_kozerog)
        key_vodoley = types.InlineKeyboardButton(text='Водолей', callback_data='zodiac')
        keyboard.add(key_vodoley)
        key_ryby = types.InlineKeyboardButton(text='Рыбы', callback_data='zodiac')
        keyboard.add(key_ryby)
        # Показываем все кнопки сразу и пишем сообщение о выборе
        bot.send_message(message.from_user.id, text='Выбери свой знак зодиака', reply_markup=keyboard)
    elif message.text == 'Рандомное число':
        bot.send_message(message.chat.id, str(random.randint(1, 100)))

    elif message.text == 'Погода':

        bot.send_message(message.from_user.id, "Введите название города")
        bot.register_next_step_handler(message, get_weather)

    elif message.text == 'Анекдоты':
        markup = types.InlineKeyboardMarkup()
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.52'
        }
        url = 'https://www.anekdot.ru/random/anekdot/'
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        anecdot = soup.find('div', class_="text")
        for article in anecdot:
            article_title = article.text.strip()
        bot.send_message(message.chat.id, anecdot.text, reply_markup=markup)
    elif message.text == 'НЕ НАЖИМАЙ СЮДА':
        bot.send_message(message.chat.id, f'С вашей карты списано {random.randint(1000, 2500)} рублей. Спасибо за поддержку бота)'), bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAEHWStjyZ7KlyFasA6uuZWkaBS1jg0SyAACCgADTDbWBDafo3IkQrt9LQQ')
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Выбери пункт меню")
    else:
        bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAEHWSdjyZ1D-iri1DiHWazCDUo0hUeK_AACWwADaJpdDFlcIw0tTK-1LQQ')
        bot.send_message(message.from_user.id, "Нажми /start или /help")

def weather(city: str):
    owm = OWM(weather_token)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    weather = observation.weather
    location = get_location(observation.location.lat, observation.location.lon)
    temperature = weather.temperature("celsius")
    return temperature, location

def get_weather(message):
    city = message.text
    try:
        w = weather(city)
        bot.send_message(message.from_user.id, f'В городе {city} сейчас {round(w[0]["temp"])} градусов,'
                                                       f' чувствуется как {round(w[0]["feels_like"])} градусов')
        bot.send_message(message.from_user.id, w[1])
    except Exception as e:
        bot.send_message(message.from_user.id, 'Такого города нет в базе, попробуй еще раз')
        bot.send_message(message.from_user.id, "Введите название города")
        bot.register_next_step_handler(message, get_weather)
        print(e)
def get_location(lat, lon):
    url = f"https://yandex.ru/pogoda/maps/nowcast?lat={lat}&lon={lon}&via=hnav&le_Lightning=1"
    return url




# Обработчик нажатий на кнопки гороскопа
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # Если нажали на одну из 12 кнопок — выводим гороскоп
    if call.data == "zodiac":
        # Формируем гороскоп
        msg = random.choice(first) + ' ' + random.choice(second) + ' ' + random.choice(second_add) + ' ' + random.choice(third)
        # Отправляем текст в Телеграм
        bot.send_message(call.message.chat.id, msg)
# Запускаем постоянный опрос бота в Телеграме

# Заготовки для трёх предложений
first = ["Сегодня — идеальный день для новых начинаний.","Оптимальный день для того, чтобы решиться на смелый поступок!","Будьте осторожны, сегодня звёзды могут повлиять на ваше финансовое состояние.","Лучшее время для того, чтобы начать новые отношения или разобраться со старыми.","Плодотворный день для того, чтобы разобраться с накопившимися делами."]
second = ["Но помните, что даже в этом случае нужно не забывать про","Если поедете за город, заранее подумайте про","Те, кто сегодня нацелен выполнить множество дел, должны помнить про","Если у вас упадок сил, обратите внимание на","Помните, что мысли материальны, а значит вам в течение дня нужно постоянно думать про"]
second_add = ["отношения с друзьями и близкими.","работу и деловые вопросы, которые могут так некстати помешать планам.","себя и своё здоровье, иначе к вечеру возможен полный раздрай.","бытовые вопросы — особенно те, которые вы не доделали вчера.","отдых, чтобы не превратить себя в загнанную лошадь в конце месяца."]
third = ["Злые языки могут говорить вам обратное, но сегодня их слушать не нужно.","Знайте, что успех благоволит только настойчивым, поэтому посвятите этот день воспитанию духа.","Даже если вы не сможете уменьшить влияние ретроградного Меркурия, то хотя бы доведите дела до конца.","Не нужно бояться одиноких встреч — сегодня то самое время, когда они значат многое.","Если встретите незнакомца на пути — проявите участие, и тогда эта встреча посулит вам приятные хлопоты."]
# Метод, который получает сообщения и обрабатывает их

bot.polling(none_stop=True, interval=0)
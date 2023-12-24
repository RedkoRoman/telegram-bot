import requests
import telebot
from telebot import types

BOT_TOKEN = 'YOUR TOKEN'
WEATHER_KEY = 'b5e1fd804c0ccf40704b95f7757b6881'

bot = telebot.TeleBot(BOT_TOKEN)


def create_start_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Привет')
    markup.add(btn1)
    return markup


def create_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Факт о кошках')
    btn2 = types.KeyboardButton('Случайное действие')
    btn3 = types.KeyboardButton('Случайное изображение собаки')
    btn4 = types.KeyboardButton('Получить свой IP-адрес')
    btn5 = types.KeyboardButton('Погода')
    btn6 = types.KeyboardButton('Расскажи шутку')
    btn7 = types.KeyboardButton('Сколько сейчас стоит биткоин')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    return markup


def parse_api(url):
    result = requests.get(url)
    return result.json()


def get_weather(message):
    city = message.text
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={WEATHER_KEY}'
    result = parse_api(weather_url)

    if 'main' in result:
        temperature = result['main']['temp']
        description = result['weather'][0]['description']
        response_text = f'Погода в городе {city}: \nТемпература: {temperature}°C \nОписание: {description}'
    else:
        response_text = f'Не удалось найти информацию о погоде для города {city}'

    bot.send_message(message.from_user.id, response_text)


@bot.message_handler(commands=['start'])
def start(message):
    markup = create_start_markup()
    bot.send_message(message.from_user.id, 'Привет', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Привет':
        markup = create_main_markup()
        bot.send_message(message.from_user.id, 'Задавай вопрос', reply_markup=markup)
    elif message.text == 'Факт о кошках':
        result = parse_api(url='https://catfact.ninja/fact')
        bot.send_message(message.from_user.id, result['fact'], parse_mode='Markdown')
    elif message.text == 'Случайное действие':
        result = parse_api(url='https://www.boredapi.com/api/activity')
        bot.send_message(message.from_user.id, result['activity'], parse_mode='Markdown')
    elif message.text == 'Случайное изображение собаки':
        result = parse_api(url='https://dog.ceo/api/breeds/image/random')
        bot.send_photo(message.from_user.id, result['message'])
    elif message.text == 'Получить свой IP-адрес':
        result = parse_api(url='https://api.ipify.org?format=json')
        bot.send_message(message.from_user.id, result['ip'], parse_mode='Markdown')
    elif message.text == 'Погода':
        bot.send_message(message.from_user.id, 'Введи название города: ', parse_mode='Markdown')
        bot.register_next_step_handler(message, get_weather)
    elif message.text == 'Расскажи шутку':
        result = parse_api(url='https://official-joke-api.appspot.com/random_joke')
        bot.send_message(message.from_user.id, result['setup'], parse_mode='Markdown')
        bot.send_message(message.from_user.id, result['punchline'], parse_mode='Markdown')
    elif message.text == 'Сколько сейчас стоит биткоин':
        result = parse_api(url='https://api.coindesk.com/v1/bpi/currentprice.json')
        price = result['bpi']['USD']['rate']
        bot.send_message(message.from_user.id, f"Текущая цена биткоина: {price} USD", parse_mode='Markdown')
if __name__ == '__main__':
    bot.polling(none_stop=True)
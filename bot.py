import telebot
import requests
import datetime
#API сайта и его ссылка
APPID = "c64006911caba9ee0382b859b7488c98"
URL_BASE = "http://api.openweathermap.org/data/2.5/"

#токен бота
bot = telebot.TeleBot('1688600309:AAEtiU4sLm4uWWPTu9BB34hxP-81oj7BxUE')

@bot.message_handler(content_types=['text'])
#получение и отправка сообщения в боте
def start(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Привет,я бот который тебе поможет узнать прогноз погодо на сегодня, отправь мне название города!")
    else:
        sms(message)
def sms(message):
    bot.send_message(message.from_user.id, current_weather(message.text))
#получения данных с сайта,и их распределение
def current_weather(q: str = "Moscow", appid: str = APPID, lang: str="ru", units: str="metric"):
    try:
        data =  requests.get(URL_BASE + "weather", params=locals()).json()
        city = data["name"]
        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])
        return (f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                  f"Погода в городе: {city}\nТемпература: {cur_weather}C°\n"
                  f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                  f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                  f"***Хорошего дня!***"
                  )
    except Exception as ex:
        return ('Проверьте название города')
#run
bot.polling(none_stop=True, interval=0)
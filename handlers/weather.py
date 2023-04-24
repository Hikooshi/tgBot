import requests
from math import floor
from tgBot.bot import dp
from aiogram.types import Message
from tgBot.config import WEATHER_API

appid = WEATHER_API


# pyOWM не захотел принимать API_KEY, пришлось создавать свою функцию по сбору информации о погоде
async def get_weather(city, country):
    weather = [False]
    directions = ('С', 'СВ', 'В', 'ЮВ', 'Ю', 'ЮЗ', 'З', 'СЗ') # Кортеж для указания направления ветра
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': ','.join([city, country]), 'type': 'like', 'units': 'metric', 'APPID': appid, 'lang': 'ru'}) # Составляем URL-запрос
        data = res.json()
        if len(data['list']) > 0: # Только если удается найти город
            weather[0] = True
            # Можно было добавить как словарь, но здесь не много данных, поэтому можно и списком
            main_weather = data['list'][0]['main']
            weather.append(str(main_weather['feels_like']))
            weather.append(str(main_weather['humidity']))
            weather.append(str(main_weather['grnd_level'] * 0.75)) # Конвертация из гигаПаскалей в мм рт ст
            weather.append(data['list'][0]['weather'][0]['description'])
            weather.append(str(data['list'][0]['wind']['speed']))
            deg = data['list'][0]['wind']['deg']
            wind_name = directions[floor(deg / 45) % 8] # Расчет направления ветра
            weather.append(wind_name)
    except Exception as e:
        print(e)
        pass

    return weather


@dp.message_handler(commands=["weather"])
async def send_weather(message: Message):
    data = message.text.split() # Разбиваем строку, чтобы получить название города и страны
    # Проверка на то, чтоб были указаны и город и страна
    if len(data) < 3:
        return await message.reply("Не указаны название города или страны")
    # Получаем данные о погоде
    weather = await get_weather(data[1], data[2])
    # Защита от ввода неправильного названия города или страны
    if not weather[0]:
        return await message.reply("Неверно введены название города или страны")
    # Собираем строку, форматируем в HTML
    city_weather = f'Погода в городе <b>{data[1].capitalize()}:</b>\n\n'\
                    f'<b>Температура:</b> {weather[1]} C\n'\
                    f'<b>Влажность:</b> {weather[2]}%\n'\
                    f'<b>Давление:</b> {weather[3]} мм рт ст\n'\
                    f'<b>Облачность:</b> {weather[4]}\n'\
                    f'<b>Ветер:</b> {weather[6]}, скорость: {weather[5]} м/с\n'
    await message.reply(city_weather, parse_mode="HTML")
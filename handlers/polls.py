from tgBot.bot import dp, bot
from random import choice
from aiogram.types import Message, PollAnswer

# Можно добавлять сколько угодно опросов
polls = [
    {'title': 'Кто нравится больше?',
     'options': ['Кошки', 'Собаки']}
]


@dp.message_handler(commands=["poll"])
async def send_poll(message: Message):
    poll = choice(polls) # Всегда выбирается случайный опрос
    await bot.send_poll(chat_id=message.chat.id, question=poll['title'], options=poll['options'], is_anonymous=False)

# Результаты опроса пропадут после перезапуска бота. В ТЗ не было указано сохранение куда-либо

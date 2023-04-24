from tgBot.bot import dp
from aiogram.types import Message
from random import choice

# Кортеж ссылок на фото милых животных
animals = ("https://mobimg.b-cdn.net/v3/fetch/a8/a825274c3f23c6dc799fb1f1a713a44e.jpeg",
           "https://mobimg.b-cdn.net/v3/fetch/c3/c3f3c42b3913598bb495d8f1ba046476.jpeg",
           "https://a.d-cd.net/d9e8d6es-1920.jpg",
           "http://mobimg.b-cdn.net/v3/fetch/46/46a08abec97078ca82d51cb884190d3f.jpeg")


@dp.message_handler(commands=["cute"])
async def send_cute_animal(message: Message):
    try:
        await message.answer_photo(photo=choice(animals), caption="Милое животное") # Выбираем случайную ссылку из кортежа
    except: # Защита от битой ссылки
        await message.answer("Ссылка с фото милого животного недоступна")
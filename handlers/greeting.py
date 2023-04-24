from tgBot.bot import dp, bot
from aiogram.types import Message, ContentType


INFO = """
<b>/weather</b> - Узнать погоду в городе.
<em>Пример: /weather Москва RU</em> (регистр не важен)

<b>/exc</b> - Конвертировать сумму из одной валюты в другую.

<b>/poll</b> - Вызвать случайный опрос.

<b>/cute</b> - Отправить изображение милого животного."""


@dp.message_handler(commands=["start"]) # При знакомстве с ботом в личном сообщении
async def start_cmd(message: Message):
    await bot.send_message(chat_id=message.from_user.id, text=f'Здравствуй, {message.from_user.full_name}. Команды нашего бота:\n{INFO}', parse_mode="HTML")


@dp.message_handler(content_types=[ContentType.NEW_CHAT_MEMBERS]) # При вступлении в группу нового пользователя
async def new_members_handler(message: Message):
    new_member = message.new_chat_members[0]
    await bot.send_message(new_member.id, f'Добро пожаловать, {new_member.full_name}. Команды нашего бота:\n{INFO}', parse_mode="HTML")
from aiogram import Bot, Dispatcher, executor
from tgBot.config import TOKEN
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(TOKEN)
storage = MemoryStorage() # Хранилище нужно для работы с машиной состояний
dp = Dispatcher(bot, storage=storage)


async def on_startup(_) -> None: # Для удобства. В данном боте нет смысла указывать функцию on_shutdown, потому что хранилище и так очистится, когда бот будет выключен
    print("Бот запущен")


if __name__ == "__main__":
    from tgBot.handlers import dp
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
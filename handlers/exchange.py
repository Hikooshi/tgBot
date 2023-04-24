import requests
from tgBot.keyboards.keyboards import currency_kb, currency_list # Импортируем клавиатуру
from tgBot.keyboards.keyboards import currency_names as cn # Импортируем словарь {"Валюта": "Трехбуквенное значение"}. Для удобства дадим другое имя. Задействован в функции set_amount
from tgBot.bot import dp
from aiogram.dispatcher.filters import Text, Command
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from tgBot.config import EXC_API_KEY

headers= {"apikey": EXC_API_KEY} # В хэдере должен содержаться токен

class CurrencyState(StatesGroup): # Машина состояний на валюты и сумму денег
    c1 = State()
    c2 = State()
    amount = State()


async def get_exchange(c1, c2, amount): # Делаем запрос по двум валютам и сумме, возращаем результат конвертации
    response = requests.get(f"https://api.apilayer.com/exchangerates_data/convert?to={c2}&from={c1}&amount={amount}", headers=headers).json()
    return response['result']


@dp.message_handler(Command("exc")) # Начало работы скрипта по конвертации валют. Устанавливаем состояние машины на прием первой валюты
async def start_exchange(message: Message, state: FSMContext):
    await message.answer("Выберите валюту, из которой хотите конвертировать", reply_markup=currency_kb)
    await CurrencyState.c1.set()


@dp.message_handler(Text("Отмена", ignore_case=True), state="*") # Отмена всех действий, сделанных или нет
async def cancel_exchange(message: Message, state: FSMContext):
    await message.answer("Отмена операции", reply_markup=ReplyKeyboardRemove())
    if await state.get_state() == None:
        return
    await state.finish()
    await state.reset_data()


@dp.message_handler(state=CurrencyState.c1) # Устанавливаем состояние машины на прием второй валюты
async def set_c1(message: Message, state: FSMContext):
    if message.text not in currency_list:
        return await message.answer("Неверное название валюты")
    await message.answer("Выберите валюту, в которую хотите конвертировать", reply_markup=currency_kb)
    await state.update_data(c1=message.text)
    await CurrencyState.c2.set()


@dp.message_handler(state=CurrencyState.c2) # Устанавливаем состояние машины на прием значения суммы
async def set_c2(message: Message, state: FSMContext):
    if message.text not in currency_list:
        return await message.answer("Неверное название валюты")
    await message.answer("Укажите сумму", reply_markup=ReplyKeyboardRemove())
    await state.update_data(c2=message.text)
    await CurrencyState.amount.set()


@dp.message_handler(state=CurrencyState.amount)
async def set_amount(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Сумма должна быть указана цифрами")
    data = await state.get_data()
    result = await get_exchange(cn[data['c1']], cn[data['c2']], message.text)
    await message.reply(f'{message.text} {data["c1"]} = {result} {data["c2"]}') # Вызываем конвертацию
    await state.finish()
    await state.reset_data()
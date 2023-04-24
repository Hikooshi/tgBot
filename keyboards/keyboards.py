from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

currency_names = {
    'Российский рубль': 'RUB',
    'Белорусский рубль': 'BYN',
    'Гривна': 'UAH',
    'Теньге': 'KZT',
    'Доллар США': 'USD',
    'Евро': 'EUR'
}

# Кнопки для клавиатуры
currency_buttons = [
    [KeyboardButton(text='Российский рубль'), KeyboardButton(text='Белорусский рубль')],
    [KeyboardButton(text='Гривна'), KeyboardButton(text='Теньге')],
    [KeyboardButton(text='Доллар США'), KeyboardButton(text='Евро')],
    [KeyboardButton(text='Отмена')],
]

# Создаем клавиатуру
currency_kb = ReplyKeyboardMarkup(currency_buttons)

# Этот список нужен для фильтрации, чтоб пользователь не ввел неправильную валюту
currency_list = currency_names.keys()
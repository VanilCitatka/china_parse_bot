from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types

kb = [
    [
        types.KeyboardButton(text='Обувь'),
        types.KeyboardButton(text='Кроссовки'),
        types.KeyboardButton(text='Одежда'),
        types.KeyboardButton(text='Сумки')
    ]
]


def create_main_keyboard():
    builder = ReplyKeyboardBuilder(kb)
    builder.adjust(2)
    return builder.as_markup()

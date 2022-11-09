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


def create_year_kb():
    year_kb = [[types.KeyboardButton(text=str(year)) for year in range(2020, 2026)]]
    builder = ReplyKeyboardBuilder(year_kb)
    builder.adjust(3)
    return builder.as_markup()


def create_month_kb():
    month_kb = [[types.KeyboardButton(text=str(month)) for month in range(1, 13)]]
    builder = ReplyKeyboardBuilder(month_kb)
    builder.adjust(4)
    return builder.as_markup()


def create_day_kb():
    day_kb = [[types.KeyboardButton(text=str(day)) for day in range(1, 32)]]
    builder = ReplyKeyboardBuilder(day_kb)
    builder.adjust(8)
    return builder.as_markup()


def create_main_keyboard():
    builder = ReplyKeyboardBuilder(kb)
    builder.adjust(2)
    return builder.as_markup()

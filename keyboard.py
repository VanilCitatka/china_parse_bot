#!/usr/bin/python3.9
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types

main_kb = [
    [
        types.KeyboardButton(text='Часы'),
        types.KeyboardButton(text='Кроссовки'),
        types.KeyboardButton(text='Одежда'),
        types.KeyboardButton(text='Сумки')
    ]
]

back_kb = [
    [
        types.KeyboardButton(text='Назад'),
    ]
]


def create_main_keyboard():
    builder = ReplyKeyboardBuilder(main_kb).adjust(2)
    return builder.as_markup(resize_keyboard=True)


def create_back_keyboard():
    builder = ReplyKeyboardBuilder(back_kb).adjust(1)
    return builder.as_markup(resize_keyboard=True)

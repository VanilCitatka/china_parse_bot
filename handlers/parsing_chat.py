from aiogram import Router, types
from aiogram.filters import Command, Text

from keyboard import create_main_keyboard

parse = Router()


@parse.message(Command(commands=["start"]))
async def bot_start(msg: types.Message):
    await msg.answer('Привет пошёл нахуй', reply_markup=create_main_keyboard())


# Работа с текстом
@parse.message(Text(text=['Обувь', 'Кроссовки', 'Одежда', 'Сумки']))
async def text_test(msg: types.Message):
    await msg.answer('Пошёл нахуй со своими ' + msg.text, reply_markup=create_main_keyboard())

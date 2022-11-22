from aiogram import Router, types, F
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from keyboard import create_main_keyboard

parse = Router()

categories = ['Часы', 'Кроссовки', 'Cумки', 'Одежда']


class WhatToParse(StatesGroup):
    category = State()
    date = State()


@parse.message(Command(commands=["start"]))
async def bot_start(msg: types.Message, state: FSMContext):
    await msg.answer('Привет! Что парсим?', reply_markup=create_main_keyboard())
    await state.set_state(WhatToParse.category)


# Работа с текстом
@parse.message(WhatToParse.category, F.text.in_(categories))
async def data_choose(msg: types.Message, state: FSMContext):
    await state.update_data(category_type=msg.text.lower())
    await msg.answer('Введите дату в формате гггг-мм-дд', reply_markup=ReplyKeyboardRemove())
    await state.set_state(WhatToParse.date)


@parse.message(WhatToParse.date)
async def fin(msg: types.Message, state: FSMContext):
    hui = await state.get_data()
    await msg.answer(f'Дата: {msg.text}, Категория: {hui["category_type"]}')
    await msg.answer('И ДАЛЬШЕ Я ПОДКЛЮЧАЮ СКРИПТ ЗАРАНЕЕ ИДИ НАХУЙ ПЕСОК Я ПРОГРАММИСТ Я ТАК ВИЖУ')
    await state.clear()






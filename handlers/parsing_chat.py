#!/usr/bin/python3.9
from aiogram import Router, types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove
from keyboard import create_main_keyboard, create_back_keyboard
from aiogram.types import FSInputFile
from datetime import date


import os
from shop_parser.parser import collect_data

parse = Router()

categories = {
    'Часы': 'A2017122802434822429',
    'Кроссовки': 'A2017120822295108026', 
    'Сумки': 'A201803280031209720038067', 
    'Одежда': 'A2018031702370069766'
}


class WhatToParse(StatesGroup):
    set_date = State()


@parse.message(Command(commands=['start']))
async def bot_start(msg: types.Message):
    await msg.answer('Что парсим?', reply_markup=create_main_keyboard())


@parse.message(Text(text=list(categories.keys())))
async def choose_category(msg: types.Message, state: FSMContext):
    await msg.answer('Отлично!', reply_markup=ReplyKeyboardRemove())
    await state.set_state(WhatToParse.set_date)
    await state.update_data(album=categories[msg.text])
    await msg.answer(
        'Введите дату начала парсинга в формате гггг-мм-дд. Пример: 2022-12-31.',
        reply_markup=create_back_keyboard()
    )


@parse.message()
async def wrong_category(msg: types.Message):
    await msg.reply(f'Категория {msg.text} не найдена!\nПопробуйте ещё раз.', reply_markup=create_main_keyboard())


@parse.message(Text(text=['Назад']))
async def back(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.answer('Что парсим?', reply_markup=create_main_keyboard())


@parse.message(WhatToParse.set_date)
async def type_date(msg: types.Message, state: FSMContext):
    try:
        enter_date = date.fromisoformat(msg.text)
        to_day = date.today()
        if enter_date > to_day or to_day.year - enter_date.year > 1:
            raise ValueError
    except ValueError:
        await msg.answer('Неправильно введённая дата. Попробуйте ещё раз',)
    else:
        await state.update_data(start_date=msg.text)
        await download_files(msg, state)


async def download_files(msg: types.Message, state: FSMContext):
    hui = await state.get_data()
    message = await msg.answer('Начинается загрузка.')
    await collect_data(hui['album'], hui['start_date'], message)
    await message.edit_text('Загрузка окончена.')
    if len(os.listdir('tables')) != 0:
        for table in os.listdir('tables'):
            file = FSInputFile(f'tables\\{table}')
            await msg.answer_document(file)
            os.remove(f'tables\\{table}')
    else:
        await msg.answer('Подходящих товаров не нашлось.')
    await msg.answer('Повторим?', reply_markup=create_main_keyboard())
    await state.clear()

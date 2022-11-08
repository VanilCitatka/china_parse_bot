import logging
import asyncio
from keyboard import *
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, Text

from configs.config_reader import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


@dp.message(Command(commands=["start"]))
async def bot_start(msg: types.Message):
    await msg.answer('Привет пошёл нахуй', reply_markup=create_main_keyboard())


# Работа с текстом
@dp.message(Text(text=['Обувь', 'Кроссовки', 'Одежда', 'Сумки']))
async def text_test(msg: types.Message):
    await msg.answer('Пошёл нахуй со своими ' + msg.text, reply_markup=create_main_keyboard())


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

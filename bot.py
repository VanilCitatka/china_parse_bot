import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from configs.config_reader import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


@dp.message(Command(commands=["start"]))
async def bot_start(msg: types.Message):
    await msg.answer('Привет пошёл нахуй')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

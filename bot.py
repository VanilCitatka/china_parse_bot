import logging
import asyncio
from handlers import parsing_chat
from keyboard import *
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, Text

from configs.config_reader import config

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.include_router(parsing_chat.parse)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from config import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value())

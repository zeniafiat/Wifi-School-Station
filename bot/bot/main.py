# main.py

import logging
from aiogram import Bot, Dispatcher

from bot.handlers import create_router  # Теперь это функция

TOKEN = "7282246929:AAEBtMCpibWIL9GmTNh6AZfdkJy06eH0vX0"
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def start_bot():
    router = create_router()  # Создаем новый роутер при каждом запуске
    dp.include_router(router)

    logging.basicConfig(level=logging.INFO)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
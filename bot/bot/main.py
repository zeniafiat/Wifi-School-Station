import logging
from .handlers import rot
from aiogram import Bot,Dispatcher



TOKEN = "7282246929:AAEBtMCpibWIL9GmTNh6AZfdkJy06eH0vX0"
dp = Dispatcher()
bot = Bot(token=TOKEN)


async def start_bot():
    dp.include_router(rot)
    logging.basicConfig(level=logging.INFO)
    try: 
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
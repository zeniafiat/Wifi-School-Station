import asyncio
import logging
from handlers import rot
from aiogram import Bot,Dispatcher,html


TOKEN = "8090502380:AAHJkS4rd6uSxStvFR-YIQzZi9gJu_ibYlY"
dp = Dispatcher()
bot = Bot(token=TOKEN)

async def main() -> None:
    dp.include_router(rot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit") 
import threading
import asyncio
from .main import start_bot


def run_aiogram_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_bot())


def start_bot_thread():
    bot_thread = threading.Thread(target=run_aiogram_bot, daemon=True)
    bot_thread.start()
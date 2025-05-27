import threading
import asyncio
from .main import start_bot


def run_aiogram_bot():
    asyncio.run(start_bot())


def start_bot_thread():
    bot_thread = threading.Thread(target=run_aiogram_bot, daemon=True)
    bot_thread.start()
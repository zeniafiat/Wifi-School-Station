"""
WSGI config for SchoolStation project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SchoolStation.settings")

application = get_wsgi_application()

import threading
from bot.bot.runner import run_aiogram_bot

# Запуск бота в фоне
bot_thread = threading.Thread(target=run_aiogram_bot)
bot_thread.daemon = True
bot_thread.start()

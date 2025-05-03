from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import html, Router

import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from cach_mess import get_data
from sqlite1 import getDATA

from  bot.keyboard import keyboard



rot = Router()
@rot.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(f"""Hello, {message.from_user.full_name}!
я могу следить за воздухом и влажность в классе.
нажми на клаватуре 'пришли данные' для того чтобы получить информацию""", reply_markup=keyboard)


@rot.message(lambda message: message.text.lower() == "пришли данные")
async def echo_handler(message: Message):
    try:
        data = get_data()
        print(data)
        await message.answer(data)
    except:
        await message.answer("не удалось получить информацию!", reply_markup=keyboard)

@rot.message(lambda message: message.text.lower() == "посмотреть прошлые данные")
async def echo_handler(message: Message):
    try:
        data = getDATA()
        print(data)
        await message.answer(data)
    except:
        await message.answer("не удалось получить информацию!", reply_markup=keyboard)
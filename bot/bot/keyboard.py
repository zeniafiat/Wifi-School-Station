
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Пришли данные')],[KeyboardButton(text='посмотреть прошлые данные')],[KeyboardButton(text='/set_id (здесь укажите айди)')]], resize_keyboard=True)

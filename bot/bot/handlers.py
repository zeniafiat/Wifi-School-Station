from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import html, Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import django
from main.models import DATT
from django.contrib.auth import authenticate
from users.models import UserProfile

from asgiref.sync import sync_to_async

from  bot.keyboard import keyboard


import os


# Инициализируем Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

def create_router():
    rot = Router()
    class AuthStates(StatesGroup):
        waiting_for_login = State()
        waiting_for_password = State()
        waiting_for_sensor_id = State() 





    @rot.message(F.text == "/start")
    async def cmd_start(message: Message, state: FSMContext):
        telegram_id = message.from_user.id

        profile = await sync_to_async(UserProfile.objects.filter(telegram_id=telegram_id).first)()

        if profile:
            username = await sync_to_async(lambda: profile.user.username)()
            await message.answer(f"👋 Привет, {username}!", reply_markup=keyboard)
            await state.clear()
            return

        await message.answer("🔐 Вход в систему\nВведите ваш логин:")
        await state.set_state(AuthStates.waiting_for_login)

    @rot.message(AuthStates.waiting_for_login)
    async def ask_password(message: Message, state: FSMContext):
        await state.update_data(login=message.text)
        await message.answer("🔑 Введите пароль:")
        await state.set_state(AuthStates.waiting_for_password)

    @rot.message(AuthStates.waiting_for_password)
    async def process_login(message: Message, state: FSMContext):
        data = await state.get_data()
        login = data['login']
        password = message.text
        telegram_id = message.from_user.id

        user = await sync_to_async(authenticate)(username=login, password=password)

        if user:
            profile, created = await sync_to_async(UserProfile.objects.get_or_create)(
            user=user,
            defaults={'sensor_id': None}  
            )
            profile.telegram_id = telegram_id
            await sync_to_async(profile.save)()
            await message.answer("✅ Вы успешно авторизованы и привязаны к аккаунту.")
            await message.answer("🔢 Введите ID вашего датчика:")
            await state.set_state(AuthStates.waiting_for_sensor_id)
        else:
            await message.answer("❌ Неверный логин или пароль. Попробуйте снова.")
            await state.set_state(AuthStates.waiting_for_login)

    @rot.message(AuthStates.waiting_for_sensor_id)
    async def save_sensor_id(message: Message, state: FSMContext):
        try:
            sensor_id = int(message.text.strip())
            telegram_id = message.from_user.id

            profile = await sync_to_async(UserProfile.objects.get)(telegram_id=telegram_id)

            profile.sensor_id = sensor_id
            await sync_to_async(profile.save)()

            await message.answer(f"📡 Вы привязаны к датчику `{sensor_id}`", parse_mode="Markdown", reply_markup=keyboard)
            await state.clear()

        except ValueError:
            await message.answer("⚠️ Введите число, например: `12345`", parse_mode="Markdown")










    @rot.message(lambda message: message.text.lower() == "пришли данные")
    async def echo_handler(message: Message):
        telegram_id = message.from_user.id

        try:
            profile = await sync_to_async(UserProfile.objects.get)(telegram_id=telegram_id)
            sensor_id = profile.sensor_id

            if sensor_id is None:
                await message.answer("⚠️ Вы не привязаны к датчику. Напишите: `id:12345`", parse_mode="Markdown")
                return

            data = await sync_to_async(DATT.objects.filter)(addr=sensor_id)
            latest_data = await sync_to_async(data.latest)("id")


            await message.answer(
                f"📡 Последние данные с датчика `{sensor_id}`:\n"
                f"Угарный газ: {latest_data.CO}\n"
                f"Комната: {latest_data.room}\n"
                f"Влажность: {latest_data.HUM}\n"
                f"Температура: {latest_data.TEMP}",
                parse_mode="Markdown",
                reply_markup=keyboard
            )

        except UserProfile.DoesNotExist:
            await message.answer("❌ Профиль не найден. Авторизуйтесь через сайт или бота.")
        except DATT.DoesNotExist:
            await message.answer("⚠️ Данные для вашего датчика пока отсутствуют.")
        except Exception as e:
            await message.answer("❌ Не удалось получить данные.")
            print(f"Ошибка: {e}")


    @rot.message(lambda message: message.text.lower() == "посмотреть прошлые данные")
    async def show_past_data_handler(message: Message):
        telegram_id = message.from_user.id

        try:

            profile = await sync_to_async(UserProfile.objects.get)(telegram_id=telegram_id)
            sensor_id = profile.sensor_id

            if sensor_id is None:
                await message.answer("⚠️ Вы не привязаны к датчику. Напишите: `id:12345`", parse_mode="Markdown")
                return

        
            data = await sync_to_async(list)(
                DATT.objects.filter(addr=sensor_id).order_by('-id')[:10]
            )

            if not data:
                await message.answer("📂 У вас пока нет данных в базе.")
                return

            answer = "📊 Последние 10 записей:\n\n"
            for i in data:
                answer += (
                    f"Угарный газ: {i.CO}\n"
                    f"Комната: {i.room}\n"
                    f"Влажность: {i.HUM}\n"
                    f"Температура: {i.TEMP}\n"
                    f"время: {i.time}\n"
                    "----------------------------\n"
                )

            await message.answer(
                answer,
                reply_markup=keyboard
                )

        except UserProfile.DoesNotExist:
            await message.answer("❌ Профиль не найден. Авторизуйтесь через бота или сайт.")
        except Exception as e:
            await message.answer("❌ Не удалось получить информацию.", reply_markup=keyboard)
            print(f"Ошибка: {e}")


    @rot.message(F.text.startswith("/set_id"))
    async def change_sensor_handler(message: Message):
        telegram_id = message.from_user.id
        text = message.text.strip()
        
        try:
            
            parts = text.split()
            if len(parts) < 2:
                await message.answer("⚠️ Укажите новое ID датчика. Пример: `/set_id 12345`", parse_mode="Markdown")
                return

            new_sensor_id = int(parts[1])

            
            profile = await sync_to_async(UserProfile.objects.get)(telegram_id=telegram_id)

            
            profile.sensor_id = new_sensor_id
            await sync_to_async(profile.save)()

            await message.answer(f"🔢 Вы успешно привязаны к датчику `{new_sensor_id}`", parse_mode="Markdown")

        except UserProfile.DoesNotExist:
            await message.answer("❌ Профиль не найден. Напишите `/start`, чтобы авторизоваться.")
        except ValueError:
            await message.answer("❌ Неверный формат ID. Ожидается число, например: `/set_id 12345`", parse_mode="Markdown")
        except Exception as e:
            await message.answer("❌ Не удалось обновить ID датчика.")
            print(f"[ERROR] {e}")
    return rot

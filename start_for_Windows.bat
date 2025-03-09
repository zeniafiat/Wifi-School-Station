@echo off

:: Открытие первого терминала и активация первого виртуального окружения
start cmd /k "venv\Scripts\activate.bat && python SchoolStation\manage.py runserver"

:: Открытие второго терминала и активация второго виртуального окружения
start cmd /k "Wifi-School-Station\venv\Scripts\activate.bat && python Wifi-School-Station\server_code\bot\main.py"
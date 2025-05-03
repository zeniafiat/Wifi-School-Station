#!/bin/bash
gnome-terminal -- bash -c "source venv/Scripts/activate; python SchoolStation/manage.py; exec bash"

gnome-terminal -- bash -c "source Wifi-School-Station/venv/Scripts/activate; python3 Wifi-School-Station/server_code/bot/main.py; exec bash"
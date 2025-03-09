import sqlite3
import re
import os

def writeDATA(data):
    match = re.search(r"!CO:(?P<co>[\d.]+)!TEMP:(?P<temp>[\d.]+)!HUMI:(?P<humi>[\d.]+)", data)
    if match:
        co = float(match.group("co"))
        temp = float(match.group("temp"))
        humi = float(match.group("humi"))
    else:
        raise ValueError("Неверный формат строки data")
    conn = sqlite3.connect("Wifi-School-Station\\sqlitePART.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO COinAIR (CO, TEMP, HUMI) VALUES (?, ?, ?)", (co, temp, humi))
    conn.commit()
    conn.close()

def getDATA():
    conn = sqlite3.connect('Wifi-School-Station\\sqlitePART.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT CO, TEMP, HUMI FROM COinAIR
    ORDER BY id DESC
    LIMIT 10
    ''')
    last_records = cursor.fetchall()
    print(last_records)
    result = """"""
    for row in last_records:
        rowwi = "CO:" + row[0] +' '+ "Temperature" + row[1]+ ' ' + "Humidity:" + row[2] + '\n'
        result += rowwi
    conn.close()
    print(result)
    return result

def UpdateData(data):
    # Поиск значений CO, TEMP и HUMI в строке
    match = re.search(r"!CO:(?P<co>[\d.]+)!TEMP:(?P<temp>[\d.]+)!HUMI:(?P<humi>[\d.]+)", data)
    if match:
        co = float(match.group("co"))
        temp = float(match.group("temp"))
        humi = float(match.group("humi"))
    else:
        raise ValueError("Неверный формат строки data")

    # Подключение к базе данных
    
    conn = sqlite3.connect("SchoolStation\\db.sqlite3")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    cursor = conn.cursor()

    # Получение ID последней записи
    cursor.execute("SELECT id FROM main_datt ORDER BY id DESC LIMIT 1")
    last_record = cursor.fetchone()

    if last_record:
        last_id = last_record[0]
        
        # Обновление последней записи
        cursor.execute("UPDATE main_datt SET CO = ?, TEMP = ?, HUM = ? WHERE id = ?", (co, temp, humi, last_id))
        conn.commit()
        print(f"Запись с ID {last_id} обновлена.")
    else:
        print("Записей в таблице нет.")

    # Закрытие соединения
    conn.close()

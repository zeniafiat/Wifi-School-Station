import sqlite3
import re

def writeDATA(data):
    match = re.search(r"!CO:(?P<co>[\d.]+)!TEMP:(?P<temp>[\d.]+)!HUMI:(?P<humi>[\d.]+)", data)
    if match:
        co = float(match.group("co"))
        temp = float(match.group("temp"))
        humi = float(match.group("humi"))
    else:
        raise ValueError("Неверный формат строки data")
    conn = sqlite3.connect("sqlitePART.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO COinAIR (CO, TEMP, HUMI) VALUES (?, ?, ?)", (co, temp, humi))
    conn.commit()
    conn.close()

def getDATA():
    conn = sqlite3.connect('sqlitePART.db')
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
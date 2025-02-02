import sqlite3

def writeDATA(data):
    conn = sqlite3.connect("sqlitePART.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO COinAIR (CO) VALUES (?)", (data,))
    conn.commit()
    conn.close()

def getDATA():
    conn = sqlite3.connect('sqlitePART.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT CO FROM COinAIR
    ORDER BY id DESC
    LIMIT 10
    ''')
    last_records = cursor.fetchall()
    print(last_records)
    result = ''
    for i in last_records:
        result += i[0]
    conn.close()
    print(result)
    return result
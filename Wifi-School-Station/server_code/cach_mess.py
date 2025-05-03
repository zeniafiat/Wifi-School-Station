import socket
from get_ip import Ip
from sqlite1 import writeDATA, UpdateData

def get_data():
    ip = Ip()
    HOST = ip
    PORT = 8080

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Сервер запущен и слушает на {HOST}:{PORT}")
        conn, addr = s.accept()
        with conn:
            print('Подключено от', addr)
            data = None
            while data == None:
                data = conn.recv(4096)
                data = data.decode()
                print('Получено:', data)
    d = data.split("!")
    resultat = ""
    for i in d:
        resultat += i + " "
    writeDATA(data)
    UpdateData(data)
    print(f"отправлено в хендлер: {resultat}")
    return resultat
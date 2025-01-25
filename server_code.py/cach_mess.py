import socket

HOST = "192.168.1.212"  # Замените на ваш публичный IP-адрес
PORT = 8080                 # Порт

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Сервер запущен и слушает на {HOST}:{PORT}")
    conn, addr = s.accept()
    with conn:
        print('Подключено от', addr)
        while True:
            data = conn.recv(4096)
            print('Получено:', data.decode())
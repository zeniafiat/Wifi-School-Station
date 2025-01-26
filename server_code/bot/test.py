import socket



ip = "192.168.1.212"
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
        while True:
            data = conn.recv(4096)
            data = data.decode()
            print('Получено:', data)
            d = data.split("!")
            resultat = ""
            for i in d:
                resultat += i + " "
    
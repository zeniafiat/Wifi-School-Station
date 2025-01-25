import requests

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_info = response.json()
        return ip_info['ip']
    except Exception as e:
        print(f"Ошибка при получении IP: {e}")
        return None

public_ip = get_public_ip()
if public_ip:
    print(f"Ваш публичный IP-адрес: {public_ip}")
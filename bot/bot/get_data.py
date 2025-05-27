from main.models import DATT

def get_last():
    try:
        last_message = DATT.objects.first()
        if last_message:
            print(f"Последнее сообщение: {last_message}")
        else:
            print("В базе нет записей")
        return last_message
    except:
        return "ошибка дб"

def history():
    history = DATT.objects.order_by('-id')[:10]
    return history
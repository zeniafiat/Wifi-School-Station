data = "!temp:nan!hum:nan!CO2:0.10"
d = data.split("!")

resultat = ""
for i in d:
    resultat += i + " "
print(f"отправлено в хендлер: {resultat}")
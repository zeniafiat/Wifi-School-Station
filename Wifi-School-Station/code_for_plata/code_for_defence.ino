#include <SPI.h>
#include <MFRC522.h>

// Пины подключения RFID RC522
#define RST_PIN 9
#define SS_PIN 10

MFRC522 rfid(SS_PIN, RST_PIN);

// Переменная для хранения состояния метки
bool isCardPresent = false;

// Массив для хранения допустимого ключа (UID)
byte allowedKey[] = {0xDF, 0x0D, 0x81, 0x1C}; // Ключ в шестнадцатеричном формате

// Пины для работы с сигналами
#define INPUT_PIN 4
#define OUTPUT_PIN 2

void setup() {
  Serial.begin(9600);
  SPI.begin(); // Инициализация SPI
  rfid.PCD_Init(); // Инициализация RFID RC522
  Serial.println("Система готова!");

  // Настройка пинов
  pinMode(3, OUTPUT);
  pinMode(INPUT_PIN, INPUT);  // Пин 4 как вход
  pinMode(OUTPUT_PIN, OUTPUT); // Пин 2 как выход
  digitalWrite(OUTPUT_PIN, HIGH); // Устанавливаем низкий сигнал на пине 2
}

void loop() {
  // Постоянное чтение данных с датчиков
  readSensors();

  // Проверка наличия метки
  checkRFID();
}

void readSensors() {
  // Здесь ваш код для чтения данных с датчиков
  Serial.println("Чтение данных с датчиков...");
  delay(500); // Имитация работы с датчиками
}

void checkRFID() {
  // Проверяем, есть ли новая метка
  if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) {
    isCardPresent = false; // Метка отсутствует
    return;
  }

  // Если метка найдена
  if (!isCardPresent) {
    isCardPresent = true; // Устанавливаем флаг, что метка найдена
    Serial.println("Метка найдена!");

    // Сравниваем ключ метки с допустимым ключом
    if (isKeyAllowed(rfid.uid.uidByte)) {
      Serial.println("Доступ разрешен!");
      // Здесь можно запустить каскад функций
      executeCascade();
    } else {
      Serial.println("Доступ запрещен!");
    }
  }

  // Завершаем работу с меткой
  rfid.PICC_HaltA();
  isCardPresent = false; // Сбрасываем состояние метки после обработки
}

bool isKeyAllowed(byte *uid) {
  // Сравниваем UID метки с допустимым ключом
  return memcmp(uid, allowedKey, 4) == 0; // Сравнение 4 байтов
}

void executeCascade() {
  Serial.println("Запуск каскада функций...");
  delay(1000);
  digitalWrite(3, HIGH);
  while (true) {
    // Чтение сигнала с пина 4
    float signal = digitalRead(INPUT_PIN); // Преобразуем значение в диапазон 0.0 - 1.0
    Serial.print("Сигнал с пина 4: ");
    Serial.println(signal);

    // Если сигнал выше 0.01, подаем  сигнал на пин 2
    if (signal > 0.01) {
      Serial.println("Сигнал выше 0.01, подаем  сигнал на пин 2");
      digitalWrite(OUTPUT_PIN, LOW);
    } else {
      digitalWrite(OUTPUT_PIN, HIGH);
    }

    // Проверяем наличие новой метки
    if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
      // Если метка найдена и она подходит, выходим из цикла
      if (isKeyAllowed(rfid.uid.uidByte)) {
        Serial.println("Подходящая метка найдена, прерываем цикл.");
        digitalWrite(3, LOW);
        digitalWrite(OUTPUT_PIN, HIGH); // Сбрасываем сигнал на пине 2
        break;
      }
    }

    delay(100); // Небольшая задержка для стабильности
  }
}
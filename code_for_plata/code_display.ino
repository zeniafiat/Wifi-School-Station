#include <ESP8266WiFi.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Константы для OLED дисплея (могут меняться)
#define SCREEN_WIDTH 128 // Ширина OLED дисплея
#define SCREEN_HEIGHT 64 // Высота OLED дисплея
#define OLED_RESET     -1 // Пин сброса (часто не используется, поэтому -1)

// Создаем объект дисплея
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
  Serial.begin(115200);

  // Инициализация дисплея
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Адрес дисплея (обычно 0x3C или 0x3D)
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Если не удалось проинициализировать дисплей - останавливаем программу
  }
  
  display.clearDisplay();
  display.setTextColor(WHITE);
  display.setTextSize(1);
  display.setCursor(0,0);
  display.println("Hello, OLED!");
  display.display(); 

  delay(2000); // Задержка в 2 секунды
  display.clearDisplay();

  // Тестовый вывод с разным размером текста
  display.setTextSize(1);
  display.setCursor(0,0);
  display.println("Size 1");
  
  display.setTextSize(2);
  display.setCursor(0, 10);
  display.println("Size 2");

  display.setTextSize(3);
  display.setCursor(0, 30);
  display.println("Size 3");
  
  display.display();
}


void loop() {
  // Здесь может быть ваш основной код, например, вывод данных на дисплей.
  // Для примера - вывод времени в цикле.
    display.clearDisplay();
    display.setTextSize(1);
    display.setCursor(0,0);
    display.print("Time: ");
    display.print(millis() / 1000); // Выводим время в секундах
    display.print("s");

    display.display();

    delay(1000); // Задержка 1 сек
}
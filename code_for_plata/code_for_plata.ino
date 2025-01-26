#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <MQUnifiedsensor.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>


//************WIFI**************
const char* ssid = "Yura1";
const char* password = "271183271183";
const char* serverAddress = "192.168.1.212";
const int serverPort = 8080;
WiFiClient client;
//***********************

//*********MQ5**************
#define         Board                   "ESP8266"
#define         Pin                    A0  //Analog input 3 of your arduino
/***********************Software Related Macros************************************/
#define         Type                    "MQ-5" //MQ3
#define         Voltage_Resolution      3.3 // 3V3 <- IMPORTANT
#define         ADC_Bit_Resolution      10 // For ESP8266
#define         RatioMQ5CleanAir        60
/*****************************Globals***********************************************/
MQUnifiedsensor MQ5(Board, Voltage_Resolution, ADC_Bit_Resolution, Pin, Type);
//***********************************


// Константы для OLED дисплея (могут меняться)
#define SCREEN_WIDTH 128 // Ширина OLED дисплея
#define SCREEN_HEIGHT 64 // Высота OLED дисплея
#define OLED_RESET     -1 // Пин сброса (часто не используется, поэтому -1)

// Создаем объект дисплея
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
  //********************
  Serial.begin(115200);


  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Адрес дисплея (обычно 0x3C или 0x3D)
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Если не удалось проинициализировать дисплей - останавливаем программу
  }
  
  display.clearDisplay();
  display.setTextColor(WHITE);
  display.setTextSize(3);
  display.setCursor(0,0);
  display.println("Hello");
  display.println("Class!");
  display.display(); 

  delay(2000); // Задержка в 2 секунды
  display.clearDisplay();





  //**********WIFI**********
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

//***************************MQ5******************************************
      MQ5.setRegressionMethod(1); 
      MQ5.setA(491204); MQ5.setB(-5.826);
      /*
        Exponential regression:
      Gas    | a      | b
      LPG    | 44771  | -3.245
      CH4    | 2*10^31| 19.01
      CO     | 521853 | -3.821
      Alcohol| 0.3934 | -1.504
      Benzene| 4.8387 | -2.68
      Hexane | 7585.3 | -2.849
      */
      MQ5.init(); 
      Serial.print("Calibrating please wait.");
      float calcR0 = 0;
      for(int i = 1; i<=10; i ++)
      {
        MQ5.update(); // Update data, the arduino will read the voltage from the analog pin
        calcR0 += MQ5.calibrate(RatioMQ5CleanAir);
        Serial.print(".");
      }
      MQ5.setR0(calcR0/10);
      Serial.println("  done!.");
      
      if(isinf(calcR0)) {Serial.println("Warning: Conection issue, R0 is infinite (Open circuit detected) please check your wiring and supply"); while(1);}
      if(calcR0 == 0){Serial.println("Warning: Conection issue found, R0 is zero (Analog pin shorts to ground) please check your wiring and supply"); while(1);}
      /*****************************  MQ CAlibration ********************************************/ 
      MQ5.serialDebug(true);
  //*****************************************************************************************


}
void loop() {
  //*********************MQ5**********************
    MQ5.update(); // Update data, the arduino will read the voltage from the analog pin
    float gas = MQ5.readSensor();
    
  //**********************************************
 
  //********************DHT**************************
      //!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  //*************************************************

    //*****************CONST**********************************
  String message = String("!temp:none") + String("!hum:none") + String("!CO:") + String(gas);


    display.clearDisplay();
    display.setTextSize(2);
    display.setCursor(0,0);
    display.println("temp:none"); // Выводим время в секундах
    display.println("humd:none");
    display.println("CO :"+String(gas));
    display.display();



    //************MESEGE SENDER***********************
    if (!client.connected()) {
    if (client.connect(serverAddress, serverPort)) {
        Serial.println("Подключено к серверу");
    } else {
      Serial.println("Не удалось подключиться к серверу. Повторяю попытку...");
      return; // Прекращаем этот цикл и ждём следующей итерации
    }
  }

    if (client.print(message)) {
        Serial.println("Сообщение отправлено: " + message);
    } else {
        Serial.println("Не удалось отправить сообщение.");
    }
    delay(0.5); // Повторяем попытку через 5 секунд (только если нужно)
  
}
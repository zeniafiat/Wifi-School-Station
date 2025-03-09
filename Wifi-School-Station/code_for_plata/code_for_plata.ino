#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <MQUnifiedsensor.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "DHT.h"



//************WIFI**************
const char* ssid = "Yura1";
const char* password = "271183271183";
const char* serverAddress = "192.168.1.212";
const int serverPort = 8080;
WiFiClient client;
//***********************

//*********MQ5**************
#define         Board                   "ESP8266"
#define         Pin                    A0  
/***********************Software Related Macros************************************/
#define         Type                    "MQ-5" 
#define         Voltage_Resolution      3.3 
#define         ADC_Bit_Resolution      10 
#define         RatioMQ5CleanAir        60
/*****************************Globals***********************************************/
MQUnifiedsensor MQ5(Board, Voltage_Resolution, ADC_Bit_Resolution, Pin, Type);
//***********************************


// Константы для OLED дисплея 
#define SCREEN_WIDTH 128 
#define SCREEN_HEIGHT 64 
#define OLED_RESET     -1 

// Создаем объект дисплея
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

//создаём всё для dht-11
#define DHTPIN 12
#define DHTTYPE DHT22 
DHT dht(DHTPIN, DHTTYPE);



void setup() {
  //********************
  Serial.begin(115200);

  //dht-11
  dht.begin();


  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { 
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); 
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
      MQ5.init(); 
      Serial.print("Calibrating please wait.");
      float calcR0 = 0;
      for(int i = 1; i<=10; i ++)
      {
        MQ5.update(); 
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
    MQ5.update();
  float gas = MQ5.readSensor();
    
  //*********************DHT*************************
  float h = dht.readHumidity();
  
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

    //*****************CONST**********************************
  String message = String("!CO:") + String(gas) + String("!TEMP:") + String(t) + String("!HUMI:") + String(h);


    display.clearDisplay();
    display.setTextSize(1);
    display.setCursor(0,0);
    display.println("CO :"+String(gas));
    display.println("Temperature :"+String(t));
    display.println("Humidity :"+String(h));
    display.display();



    //************MESEGE SENDER***********************
    if (!client.connected()) {
    if (client.connect(serverAddress, serverPort)) {
        Serial.println("Подключено к серверу");
    } else {
      Serial.println("Не удалось подключиться к серверу. Повторяю попытку...");
      return; 
    }
  }

    if (client.print(message)) {
        Serial.println("Сообщение отправлено: " + message);
    } else {
        Serial.println("Не удалось отправить сообщение.");
    }
    delay(500); 
  
}
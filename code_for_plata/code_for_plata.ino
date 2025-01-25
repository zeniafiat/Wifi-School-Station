#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include "DHT.h"
#include <MQUnifiedsensor.h>

#define DHTPIN 4
#define DHTTYPE DHT11
//*****
#define         Board                   "ESP8266"
#define         Pin                     A0  //Analog input 3 of your arduino
/***********************Software Related Macros************************************/
#define         Type                    "MQ-5" //MQ3
#define         Voltage_Resolution      3.3 // 3V3 <- IMPORTANT
#define         ADC_Bit_Resolution      10 // For ESP8266
#define         RatioMQ5CleanAir        60

const char* ssid = "Yura1";
const char* password = "271183271183";
const char* serverAddress = "192.168.1.212";
const int serverPort = 8080;

MQUnifiedsensor MQ5(Board, Voltage_Resolution, ADC_Bit_Resolution, Pin, Type);
WiFiClient client;
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  dht.begin();
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

//*********************************************************************
   MQ5.setRegressionMethod(1); //_PPM =  a*ratio^b
  MQ5.setA(521853); MQ5.setB(-3.821); // Configure the equation to to calculate Benzene concentration
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
}

void loop() {
  //*************************************
  if (!client.connected()) {
    if (client.connect(serverAddress, serverPort)) {
        Serial.println("Подключено к серверу");
    } else {
      Serial.println("Не удалось подключиться к серверу. Повторяю попытку...");
      return; // Прекращаем этот цикл и ждём следующей итерации
    }
  }
    //***************************************************
    MQ5.update();
    float t = dht.readTemperature();
    float h = dht.readHumidity();
    float gas = MQ5.readSensor();
    //*******
    String message = "!temp:" + String(t) + "!hum:" + String(h) + "!CO:" + String(gas); // Добавляем время
    //***********************************
    if (client.print(message)) {
        Serial.println("Сообщение отправлено: " + message);
    } else {
        Serial.println("Не удалось отправить сообщение.");
    }
    delay(500); // Повторяем попытку через 5 секунд (только если нужно)
  
}
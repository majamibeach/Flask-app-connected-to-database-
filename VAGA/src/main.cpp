#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include "weight_scale.h"
#include "OledDisplay.h"
#include <WiFi.h>
#include <PubSubClient.h>

weight_scale scale_(2, 13);
OledDisplay oled;

String mass="";

const char* ssid = "OMEN";
const char* password = "ajdespojise";

// Change the variable to your Raspberry Pi IP address, so it connects to your MQTT broker
const char* mqtt_server = "192.168.137.15";

// Initializes the espClient
WiFiClient espClient;
PubSubClient client(espClient);


void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected - ESP IP address: ");
  Serial.println(WiFi.localIP());
}


void callback(String topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  //Serial.println();

  
  //Serial.println();
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    
    if (client.connect("ESP32Client")) {
      Serial.println("connected");  
      //client.subscribe("esp8266/4");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}


void setup() {
    
  Serial.begin(115200);
  oled.initDisplay();
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  //client.setCallback(callback);
  oled.drawBmp();

}

void loop() {

  oled.clear();
  
  mass = "88";
  mass = scale_.get_mass();
  oled.updateText(mass);
  oled.drawBmp();
  

  
  if(WiFi.status() != WL_CONNECTED){
    setup_wifi();
  }

  

  // Length (with one extra character for the null terminator)
  int str_len = mass.length() + 1; 

  // Prepare the character array (the buffer) 
  char char_array[str_len];

  // Copy it over 
  mass.toCharArray(char_array, str_len );

  //client.connect("ESP32Client");
  client.publish("/esp32/mass", char_array);

  if (!client.connected()) {
    reconnect();
  }
  if(!client.loop())

    client.connect("ESP32Client");

    //static char temperatureTemp[7]="poslan";

    // Publishes Temperature and Humidity values
    client.publish("/esp32/mass", char_array);
}



#include "OledDisplay.h"
#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "weight_scale.h"


Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);


OledDisplay::OledDisplay()
{
  
}

void OledDisplay::initDisplay()
{
  Wire.begin(15, 14);
  display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS);
  display.display();
  display.clearDisplay(); 
  display.setTextColor(SSD1306_WHITE);
  display.clearDisplay();
  display.display();
}

void OledDisplay::updateText(String mass)
{ 
  mass = mass +"g";
  display.setTextSize(2);             // Normal 1:1 pixel scale
  display.setCursor(0,0);
  display.print(mass);
  display.display();
  
}

void OledDisplay::drawBmp()
{
  const unsigned char wifi_bmp [] PROGMEM = {
	// 'wifi, 12x12px
	0x00, 0x00, 0x1f, 0x80, 0x30, 0xe0, 0x60, 0x30, 0x1f, 0x90, 0x30, 0xc0, 0x20, 0x40, 0x0f, 0x00, 
	0x00, 0x80, 0x00, 0x00, 0x06, 0x00, 0x06, 0x00
};

  //Wire.begin(15, 14);

  display.drawBitmap(0, 20, wifi_bmp, 12, 12, 1);
  display.display();
  
  //Wire.end();
  
}

void OledDisplay::clear()
{
  display.clearDisplay();
}

void OledDisplay::MQTT_connecting()
{
  display.clearDisplay();
  display.setTextSize(2);             // Normal 1:1 pixel scale
  display.setCursor(0,0);
  display.print("MQTT connecting...");
  display.display();
}

void OledDisplay::WIFI_connecting()
{
  display.clearDisplay();
  display.setTextSize(2);             // Normal 1:1 pixel scale
  display.setCursor(0,0);
  display.print("WIFI connecting...");
  display.display();
}
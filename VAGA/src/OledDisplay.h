#ifndef OLEDDISPLAY_H
#define OLEDDISPLAY_H
#include<Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "weight_scale.h"
#pragma once

class OledDisplay
{
public:
    OledDisplay();
    void initDisplay();
    void drawBmp();
    void updateText(String mass);
    void clear();
    void MQTT_connecting();
    void WIFI_connecting();

    

private:

    #define SCREEN_WIDTH 128 // OLED display width, in pixels
    #define SCREEN_HEIGHT 32 // OLED display height, in pixels
    #define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
    #define SCREEN_ADDRESS 0x3C ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32

};

#endif
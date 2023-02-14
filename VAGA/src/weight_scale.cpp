#include "weight_scale.h"

#include<HX711.h>
#include <Arduino.h>

HX711 scale;


weight_scale::weight_scale(int pin_sda_, int pin_scl_)
{
    pin_sda = pin_sda_;
    pin_scl = pin_scl_;
    
    scale.begin(pin_sda, pin_scl);
    scale.set_scale(1704.3f);
    scale.tare();

}
weight_scale::~weight_scale()
{
    
}

String weight_scale::get_mass()
{   
    //scale.begin(pin_sda, pin_scl);
    //delay(1000);
    mass = String(scale.get_units(10));
    return mass;
    //Serial.println(mass);
    
}
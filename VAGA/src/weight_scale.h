#ifndef WEIGHT_SCALE_H
#define WEIGHT_SCALE_H
#include <Arduino.h>

#pragma once



class weight_scale
{
public:

    String mass;

    weight_scale(int pin_sda_, int pin_scl_);
    ~weight_scale();

    String get_mass();    

private:

    int pin_sda;
    int pin_scl;
    

};

#endif
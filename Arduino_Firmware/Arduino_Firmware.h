
#ifndef Arduino_Firmware_h
#define Arduino_Firmware_h

#include <Arduino.h>
#include <stdio.h>
#include <math.h>


// defines pins numbers of direction and PWM for stepper motors
const int M1_XSTEP = 2; 
const int M1_XDIR = 3;  // 1 = CW, 0 = CCW

const int M2_XSTEP = 4; 
const int M2_XDIR = 5;  // 1 = CW, 0 = CCW

const int M3_XSTEP = 6; 
const int M3_XDIR = 7;  // 1 = CW, 0 = CCW

const int M4_XSTEP = 8; 
const int M4_XDIR = 9;  // 1 = CW, 0 = CCW

const int M5_YSTEP = 10; 
const int M5_YDIR = 11;  // 1 = CW, 0 = CCW

const int M6_ZSTEP = 12; 
const int M6_ZDIR = 13;  // 1 = CW, 0 = CCW

// defines pins numbers of enable pin for stepper motors
const int EX = 19;
const int EY = 18;
const int EZ = 17;

// defines pins numbers of microstepping resolution
const int S1 = 14;
const int S2 = 15;
const int S3 = 16;

// define controls constants
const int resolution_multiplier = 16;
const int speed_time = 100;
const int low_speed_time = 700;
const int ramp_start_time = 800;

//Declare Functions
void initGPIO();
long rampSelector(long dist);
void setupEnable(void);
void enableMotor(char axis, int enable);
void setupResolution(int resolution);
char convertAxis(int int_axis);

void goToCoordonate_X(long steps_to_perform, long dir);
void goToCoordonate_Y(long steps_to_perform, long dir);
void goToCoordonate_Z(long steps_to_perform, long dir);

long rampSelector(long dist);
long rampUp_X(long ramp_direction, long min_time, long steps_to_perform);
long rampDown_X(long ramp_direction, long min_time, long steps_to_perform);
long rampUp_Y(long ramp_direction, long min_time, long steps_to_perform);
long rampDown_Y(long ramp_direction, long min_time, long steps_to_perform);
long rampUp_Z(long ramp_direction, long min_time, long steps_to_perform);
long rampDown_Z(long ramp_direction, long min_time, long steps_to_perform);
void goToWithRamp(long steps_to_perform, long dir, char axis);



#endif

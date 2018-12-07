
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

// define slowest PWM
const int low_speed_time = 700;

//Global variables
extern String resolution;
extern long initial_position[3];
extern long final_position[3];
extern long speed_time;
extern long ramp_start_time;

//Structures
struct Robot {
  long robot_position[];
  char resolution;
  long resolution_multiplier;
};

//Declare Functions
void initGPIO();
long rampSelector(long dist);
void setupEnable(void);
long setupResolution(char *resolution);
long goToCoordonate(long initial_position, long final_position, char axis, long speed_time, long resolution_multiplier);
long xAxis_goToCoordonate(long initial_position, long final_position, long speed_time, long resolution_multiplier);
//long goToCoordonate(long initial_position, long final_position, char axis, long speed_time, long resolution_multiplier);
//long goToCoordonate(long initial_position, long final_position, char axis, long speed_time, long resolution_multiplier);
long rampUp(long ramp_direction, long min_time, long steps_to_perform, long resolution_multiplier);
long rampDown(long ramp_direction, long min_time, long steps_to_perform, long resolution_multiplier);
void goTo(long *initial_position, long *final_position, long speed_time, long resolution_multiplier);
void goToWithRamp(long *initial_position, long *final_position, long speed_time, long resolution_multiplier);
long rampSelector(long dist);

#endif


#ifndef Arduino_Firmware_h
#define Arduino_Firmware_h

#include <Arduino.h>
#include <stdio.h>
#include <math.h>


// defines pins numbers
const int X_STEP = 3; 
const int X_DIR = 2;  // 1 = CW, 0 = CCW
const int Y_STEP = 3; 
const int Y_DIR = 2;  // 1 = CW, 0 = CCW
const int Z_STEP = 7; 
const int Z_DIR = 6;  // 1 = CW, 0 = CCW
const int S1 = 8;
const int S2 = 9;
const int S3 = 10;
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
long setupResolution(char *resolution);
long goToCoordanate(long initial_position, long final_position, char axis, long speed_time, long resolution_multiplier);
long rampUp(long ramp_direction, long min_time, long steps_to_perform, char axis, long resolution_multiplier);
long rampDown(long ramp_direction, long min_time, long steps_to_perform, char axis, long resolution_multiplier);
void goTo(long *initial_position, long *final_position, long speed_time, long resolution_multiplier);
void goToWithRamp(long *initial_position, long *final_position, long speed_time, long resolution_multiplier);
long rampSelector(long dist);

#endif

#include "Arduino_Firmware.h"

void initGPIO()
{
  pinMode(X_STEP,OUTPUT); 
  pinMode(X_DIR,OUTPUT);
  pinMode(Y_STEP,OUTPUT); 
  pinMode(Y_DIR,OUTPUT);
  pinMode(Z_STEP,OUTPUT); 
  pinMode(Z_DIR,OUTPUT);

  pinMode(S1,OUTPUT); 
  pinMode(S2,OUTPUT);
  pinMode(S3,OUTPUT);
}

long setupResolution(char *resolution)
{
  long resolution_multiplier = 0;
  if(resolution == "Full")
  {
    digitalWrite(S1,LOW);
    digitalWrite(S2,LOW);
    digitalWrite(S3,LOW);
    resolution_multiplier = 1;
  }
  else if(resolution == "Half")
  {
    digitalWrite(S1,HIGH);
    digitalWrite(S2,LOW);
    digitalWrite(S3,LOW);
    resolution_multiplier = 2;
  }
  else if(resolution == "1/4")
  {
    digitalWrite(S1,LOW);
    digitalWrite(S2,HIGH);
    digitalWrite(S3,LOW);
    resolution_multiplier = 4;
  }
  else if(resolution == "1/8")
  {
    digitalWrite(S1,HIGH);
    digitalWrite(S2,HIGH);
    digitalWrite(S3,LOW);
    resolution_multiplier = 8;
  }
  else 
  {
    digitalWrite(S1,HIGH);
    digitalWrite(S2,HIGH);
    digitalWrite(S3,HIGH);
    resolution_multiplier = 16;
  }
  return resolution_multiplier;
}

long goToCoordanate(long initial_position, long final_position, char axis, long speed_time, long resolution_multiplier)
{
  int step_pin = 0;
  int dir_pin = 0;
  if(axis == 'x')
  {
    step_pin = X_STEP;
    dir_pin = X_DIR;
  }
  else if(axis == 'y')
  {
    step_pin = Y_STEP;
    dir_pin = Y_DIR;
  }
  else if(axis == 'z')
  {
    step_pin = Z_STEP;
    dir_pin = Z_DIR;
  }
  else
  {
    return 1;
  }
  
  long steps_to_perform;
  steps_to_perform = abs(final_position - initial_position);
  if(final_position >= initial_position)
  {
   digitalWrite(dir_pin,HIGH); // Enables the motor to move in a particular direction
  }
  else
  {
    digitalWrite(dir_pin,LOW); // Enables the motor to move in a particular direction
  }

  if(steps_to_perform < 500)
  {
    speed_time = low_speed_time;
  }
  for(long x = 0; x < steps_to_perform*resolution_multiplier; x++)
  {
    digitalWrite(step_pin,HIGH); 
    delayMicroseconds(speed_time/resolution_multiplier); 
    digitalWrite(step_pin,LOW); 
    delayMicroseconds(speed_time/resolution_multiplier);
   }
   return final_position;
}

void goTo(long *initial_position, long *final_position, long speed_time, long resolution_multiplier)
{
  // initial_position[] is a matrix of the initial position [x, y, z]
  // final_position[] is a matrix of the final position [x, y, z]
  initial_position[0] = goToCoordanate(initial_position[0], final_position[0], 'x', speed_time, resolution_multiplier);
  //initial_position[1] = goToCoordanate(initial_position[1], final_position[1], 'y', speed_time, resolution_multiplier);
  //final_position[2] = goToCoordanate(initial_position[2], final_position[2], 'z', speed_time, resolution_multiplier);
}





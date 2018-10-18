#include "Arduino_Firmware.h"


long rampUp(long ramp_direction, long min_time, long steps_to_perform, char axis, long resolution_multiplier)
{
  //ramp_direction: 1 for ramp up and 0 for ramp down
  //ramp_time: ramp time in ms
  //steps_to_perform: number of steps to perform
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
  
  if(ramp_direction == 1)
  {
   digitalWrite(dir_pin,HIGH); // Enables the motor to move in a particular direction
  }
  else if(ramp_direction == 0)
  {
    digitalWrite(dir_pin,LOW); // Enables the motor to move in a particular direction
  }

  long total_time = ramp_start_time/resolution_multiplier;
  double dt_dx = (double(ramp_start_time)/double(resolution_multiplier) - double(min_time)/double(resolution_multiplier))/(double(steps_to_perform)*double(resolution_multiplier));
  for(long x=0; x < steps_to_perform*resolution_multiplier; x = x + 1)
  {
    digitalWrite(step_pin,HIGH); 
    delayMicroseconds(total_time); 
    digitalWrite(step_pin,LOW); 
    delayMicroseconds(total_time); 
    total_time = ramp_start_time/resolution_multiplier - long(x*dt_dx);  
  }
  //Serial.println(500*dt_dx);
}

long rampDown(long ramp_direction, long min_time, long steps_to_perform, char axis, long resolution_multiplier)
{
  //ramp_direction: 1 for ramp up and 0 for ramp down
  //ramp_time: ramp time in ms
  //steps_to_perform: number of steps to perform
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
  
  if(ramp_direction == 1)
  {
   digitalWrite(dir_pin,HIGH); // Enables the motor to move in a particular direction
  }
  else if(ramp_direction == 0)
  {
    digitalWrite(dir_pin,LOW); // Enables the motor to move in a particular direction
  }

  long total_time = ramp_start_time/resolution_multiplier;
  double dt_dx = (double(ramp_start_time)/double(resolution_multiplier) - double(min_time)/double(resolution_multiplier))/(double(steps_to_perform)*double(resolution_multiplier));
  for(long x=0; x < steps_to_perform*resolution_multiplier; x = x + 1)
  {
    digitalWrite(step_pin,HIGH); 
    delayMicroseconds(total_time); 
    digitalWrite(step_pin,LOW); 
    delayMicroseconds(total_time); 
    total_time = min_time/resolution_multiplier + long(x*dt_dx);  
  }
}

void goToWithRamp(long *initial_position, long *final_position, long speed_time, long resolution_multiplier)
{
  // initial_position is a matrix of the initial position [x, y, z]
  // final_position is a matrix of the final position [x, y, z]
  int x_dir;
  int y_dir;
  int z_dir;
  if(final_position[0] >= initial_position[0])
  {
   x_dir = 1; // Enables the motor to move in a particular direction
  }
  else
  {
    x_dir = 0; // Enables the motor to move in a particular direction
  }
  if(final_position[1] >= initial_position[1])
  {
   y_dir = 1; // Enables the motor to move in a particular direction
  }
  else
  {
    y_dir = 0; // Enables the motor to move in a particular direction
  }
  if(final_position[2] >= initial_position[2])
  {
   z_dir = 1; // Enables the motor to move in a particular direction
  }
  else
  {
    z_dir = 0; // Enables the motor to move in a particular direction
  }
  
  long x_dist = abs(final_position[0] - initial_position[0]);
  long y_dist = abs(final_position[1] - initial_position[1]);
  long z_dist = abs(final_position[2] - initial_position[2]);

  long ramp_dist= 0;
  // x axis
  ramp_dist = rampSelector(x_dist);
  rampUp(x_dir, speed_time, ramp_dist, 'x', resolution_multiplier);
  if(final_position[0] >= initial_position[0])
  {
    initial_position[0] = goToCoordanate(initial_position[0]+ramp_dist, final_position[0]-ramp_dist, 'x', speed_time, resolution_multiplier);
  }
  else
  {
    initial_position[0] = goToCoordanate(initial_position[0]-ramp_dist, final_position[0]+ramp_dist, 'x', speed_time, resolution_multiplier);
  }
  rampDown(x_dir, speed_time, ramp_dist, 'x', resolution_multiplier);
  initial_position[0] = final_position[0];

  /*
  // y axis
  ramp_dist = rampSelector(y_dist);
  rampUp(y_dir, speed_time, ramp_dist, 'y', resolution_multiplier);
  initial_position[1] = goToCoordanate(initial_position[1]+ramp_dist, final_position[1]-ramp_dist, 'y', speed_time, resolution_multiplier);
  rampDown(y_dir, speed_time, ramp_dist, 'y', resolution_multiplier);
  initial_position[1] = final_position[1];

  // z axis
  ramp_dist = rampSelector(z_dist);
  rampUp(z_dir, speed_time, ramp_dist, 'z', resolution_multiplier);
  initial_position[2] = goToCoordanate(initial_position[2]+ramp_dist, final_position[2]-ramp_dist, 'z', speed_time, resolution_multiplier);
  rampDown(z_dir, speed_time, ramp_dist, 'z', resolution_multiplier);
  initial_position[2] = final_position[2];
  */
}

long rampSelector(long dist)
{
  if(dist >= 3000)
  {
    return 1000;
  }
  else if(dist < 3000 && dist >= 1000)
  {
    return 100;
  }
  else if (dist < 1000 && dist >= 500)
  {
    return 50;
  }
  else
  {
    return 0;
  }
}
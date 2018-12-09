#include "Arduino_Firmware.h"


long rampUp_X(long ramp_direction, long min_time, long steps_to_perform)
{
  //ramp_direction: 1 for ramp up and 0 for ramp down
  //ramp_time: ramp time in ms
  //steps_to_perform: number of steps to perform

  //Direction
  if(ramp_direction == 0)
  {
   digitalWrite(M1_XDIR,HIGH); // Enables the motor to move in a particular direction
   digitalWrite(M2_XDIR,HIGH);
   digitalWrite(M3_XDIR,LOW);
   digitalWrite(M4_XDIR,LOW);
  }
  else if(ramp_direction == 1)
  {
    digitalWrite(M1_XDIR,LOW); // Enables the motor to move in a particular direction
    digitalWrite(M2_XDIR,LOW);
    digitalWrite(M3_XDIR,HIGH);
    digitalWrite(M4_XDIR,HIGH);
  }

  long total_time = ramp_start_time/resolution_multiplier;
  double dt_dx = (double(ramp_start_time)/double(resolution_multiplier) - double(min_time)/double(resolution_multiplier))/(double(steps_to_perform)*double(resolution_multiplier));

  //PWM
  for(long x=0; x < steps_to_perform*resolution_multiplier; x = x + 1)
  {
    digitalWrite(M1_XSTEP,HIGH); 
    digitalWrite(M2_XSTEP,HIGH); 
    digitalWrite(M3_XSTEP,HIGH); 
    digitalWrite(M4_XSTEP,HIGH); 
    delayMicroseconds(total_time); 
    digitalWrite(M1_XSTEP,LOW); 
    digitalWrite(M2_XSTEP,LOW);
    digitalWrite(M3_XSTEP,LOW);
    digitalWrite(M4_XSTEP,LOW);
    delayMicroseconds(total_time); 
    total_time = ramp_start_time/resolution_multiplier - long(x*dt_dx);  
  }
  
}

long rampDown_X(long ramp_direction, long min_time, long steps_to_perform)
{
  //ramp_direction: 1 for ramp up and 0 for ramp down
  //ramp_time: ramp time in ms
  //steps_to_perform: number of steps to perform

  // Direction
   if(ramp_direction == 0)
  {
   digitalWrite(M1_XDIR,HIGH); // Enables the motor to move in a particular direction
   digitalWrite(M2_XDIR,HIGH);
   digitalWrite(M3_XDIR,LOW);
   digitalWrite(M4_XDIR,LOW);
  }
  else if(ramp_direction == 1)
  {
    digitalWrite(M1_XDIR,LOW); // Enables the motor to move in a particular direction
    digitalWrite(M2_XDIR,LOW);
    digitalWrite(M3_XDIR,HIGH);
    digitalWrite(M4_XDIR,HIGH);
  }

  long total_time = ramp_start_time/resolution_multiplier;
  double dt_dx = (double(ramp_start_time)/double(resolution_multiplier) - double(min_time)/double(resolution_multiplier))/(double(steps_to_perform)*double(resolution_multiplier));
  
  // PWM
  for(long x=0; x < steps_to_perform*resolution_multiplier; x = x + 1)
  {
    digitalWrite(M1_XSTEP,HIGH); 
    digitalWrite(M2_XSTEP,HIGH); 
    digitalWrite(M3_XSTEP,HIGH); 
    digitalWrite(M4_XSTEP,HIGH); 
    delayMicroseconds(total_time); 
    digitalWrite(M1_XSTEP,LOW); 
    digitalWrite(M2_XSTEP,LOW); 
    digitalWrite(M3_XSTEP,LOW); 
    digitalWrite(M4_XSTEP,LOW); 
    delayMicroseconds(total_time); 
    total_time = min_time/resolution_multiplier + long(x*dt_dx);  
  }
}

long rampUp_Y(long ramp_direction, long min_time, long steps_to_perform)
{
  //ramp_direction: 1 for ramp up and 0 for ramp down
  //ramp_time: ramp time in ms
  //steps_to_perform: number of steps to perform

  //Direction
  if(ramp_direction == 0)
  {
   digitalWrite(M5_YDIR,HIGH); // Enables the motor to move in a particular direction
  }
  else if(ramp_direction == 1)
  {
    digitalWrite(M5_YDIR,LOW); // Enables the motor to move in a particular direction
  }

  long total_time = ramp_start_time/resolution_multiplier;
  double dt_dx = (double(ramp_start_time)/double(resolution_multiplier) - double(min_time)/double(resolution_multiplier))/(double(steps_to_perform)*double(resolution_multiplier));

  //PWM
  for(long x=0; x < steps_to_perform*resolution_multiplier; x = x + 1)
  {
    digitalWrite(M5_YSTEP,HIGH); 
    delayMicroseconds(total_time); 
    digitalWrite(M5_YSTEP,LOW); 
    delayMicroseconds(total_time); 
    total_time = ramp_start_time/resolution_multiplier - long(x*dt_dx);  
  }
  
}

long rampDown_Y(long ramp_direction, long min_time, long steps_to_perform)
{
  //ramp_direction: 1 for ramp up and 0 for ramp down
  //ramp_time: ramp time in ms
  //steps_to_perform: number of steps to perform

  // Direction
   if(ramp_direction == 0)
  {
   digitalWrite(M5_YDIR,HIGH); // Enables the motor to move in a particular direction
  }
  else if(ramp_direction == 1)
  {
    digitalWrite(M5_YDIR,LOW); // Enables the motor to move in a particular direction
  }

  long total_time = ramp_start_time/resolution_multiplier;
  double dt_dx = (double(ramp_start_time)/double(resolution_multiplier) - double(min_time)/double(resolution_multiplier))/(double(steps_to_perform)*double(resolution_multiplier));
  
  // PWM
  for(long x=0; x < steps_to_perform*resolution_multiplier; x = x + 1)
  {
    digitalWrite(M5_YSTEP,HIGH);  
    delayMicroseconds(total_time); 
    digitalWrite(M5_YSTEP,LOW); 
    delayMicroseconds(total_time); 
    total_time = min_time/resolution_multiplier + long(x*dt_dx);  
  }
}

long rampUp_Z(long ramp_direction, long min_time, long steps_to_perform)
{
  //ramp_direction: 1 for ramp up and 0 for ramp down
  //ramp_time: ramp time in ms
  //steps_to_perform: number of steps to perform

  //Direction
  if(ramp_direction == 0)
  {
   digitalWrite(M6_ZDIR,HIGH); // Enables the motor to move in a particular direction
  }
  else if(ramp_direction == 1)
  {
    digitalWrite(M6_ZDIR,LOW); // Enables the motor to move in a particular direction
  }

  long total_time = ramp_start_time/resolution_multiplier;
  double dt_dx = (double(ramp_start_time)/double(resolution_multiplier) - double(min_time)/double(resolution_multiplier))/(double(steps_to_perform)*double(resolution_multiplier));

  //PWM
  for(long x=0; x < steps_to_perform*resolution_multiplier; x = x + 1)
  {
    digitalWrite(M6_ZSTEP,HIGH); 
    delayMicroseconds(total_time); 
    digitalWrite(M6_ZSTEP,LOW); 
    delayMicroseconds(total_time); 
    total_time = ramp_start_time/resolution_multiplier - long(x*dt_dx);  
  }
  
}

long rampDown_Z(long ramp_direction, long min_time, long steps_to_perform)
{
  //ramp_direction: 1 for ramp up and 0 for ramp down
  //ramp_time: ramp time in ms
  //steps_to_perform: number of steps to perform

  // Direction
   if(ramp_direction == 0)
  {
   digitalWrite(M6_ZDIR,HIGH); // Enables the motor to move in a particular direction
  }
  else if(ramp_direction == 1)
  {
    digitalWrite(M6_ZDIR,LOW); // Enables the motor to move in a particular direction
  }

  long total_time = ramp_start_time/resolution_multiplier;
  double dt_dx = (double(ramp_start_time)/double(resolution_multiplier) - double(min_time)/double(resolution_multiplier))/(double(steps_to_perform)*double(resolution_multiplier));
  
  // PWM
  for(long x=0; x < steps_to_perform*resolution_multiplier; x = x + 1)
  {
    digitalWrite(M6_ZSTEP,HIGH);  
    delayMicroseconds(total_time); 
    digitalWrite(M6_ZSTEP,LOW); 
    delayMicroseconds(total_time); 
    total_time = min_time/resolution_multiplier + long(x*dt_dx);  
  }
}

void goToWithRamp(long steps_to_perform, long dir, char axis)
{
  // direction is a matrix of the ...

  long ramp_dist= 0;

  if (axis == 'x')
  {
    ramp_dist = rampSelector(steps_to_perform);
    rampUp_X(dir, speed_time, ramp_dist);
    
    goToCoordonate_X(steps_to_perform-2*ramp_dist, dir);
  
    rampDown_X(dir, speed_time, ramp_dist);
  }
  else if (axis == 'y')
  {
    ramp_dist = rampSelector(steps_to_perform);
    rampUp_Y(dir, speed_time, ramp_dist);
    
    goToCoordonate_Y(steps_to_perform-2*ramp_dist, dir);
  
    rampDown_Y(dir, speed_time, ramp_dist);
  }
  else if (axis == 'z')
  {
    ramp_dist = rampSelector(steps_to_perform);
    rampUp_Z(dir, speed_time, ramp_dist);
    
    goToCoordonate_Z(steps_to_perform-2*ramp_dist, dir);
  
    rampDown_Z(dir, speed_time, ramp_dist);
  }
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

#include "Arduino_Firmware.h"

//Thoses functions will move the robot at a constant PWM

void goToCoordonate_X(long steps_to_perform,long dir)
{ 
  long current_speed_time = 0;
  
  // Set direction
  if(dir == 0)
  {
   digitalWrite(M1_XDIR,HIGH); // Enables the motor to move in a particular direction
   digitalWrite(M2_XDIR,HIGH);
   digitalWrite(M3_XDIR,LOW);
   digitalWrite(M4_XDIR,LOW);
  }
  else if (dir == 1)
  {
    digitalWrite(M1_XDIR,LOW); // Enables the motor to move in a particular direction
    digitalWrite(M2_XDIR,LOW);
    digitalWrite(M3_XDIR,HIGH);
    digitalWrite(M4_XDIR,HIGH);
  }

  if(steps_to_perform < 500)
  {
    current_speed_time = low_speed_time;
  }
  else
  {
    current_speed_time = speed_time;
  }
  for(long x = 0; x < steps_to_perform*resolution_multiplier; x++)
  {
    digitalWrite(M1_XSTEP,HIGH); 
    digitalWrite(M2_XSTEP,HIGH); 
    digitalWrite(M3_XSTEP,HIGH); 
    digitalWrite(M4_XSTEP,HIGH); 
    delayMicroseconds(current_speed_time/resolution_multiplier); 
    digitalWrite(M1_XSTEP,LOW); 
    digitalWrite(M2_XSTEP,LOW); 
    digitalWrite(M3_XSTEP,LOW); 
    digitalWrite(M4_XSTEP,LOW); 
    delayMicroseconds(current_speed_time/resolution_multiplier);
   }
}


void goToCoordonate_Y(long steps_to_perform,long dir)
{ 
  long current_speed_time = 0;
  
  // Set direction
  if(dir == 0)
  {
   digitalWrite(M5_YDIR,HIGH); // Enables the motor to move in a particular direction
  }
  else if (dir == 1)
  {
    digitalWrite(M5_YDIR,LOW); // Enables the motor to move in a particular direction
  }

  if(steps_to_perform < 500)
  {
    current_speed_time = low_speed_time;
  }
  else
  {
    current_speed_time = speed_time;
  }
  //digitalWrite(EX,HIGH);
  for(long x = 0; x < steps_to_perform*resolution_multiplier; x++)
  {

    digitalWrite(M5_YSTEP,HIGH);  
    delayMicroseconds(current_speed_time/resolution_multiplier); 

    digitalWrite(M5_YSTEP,LOW); 
    delayMicroseconds(current_speed_time/resolution_multiplier);
   }
   //digitalWrite(EX,LOW);
}

void goToCoordonate_Z(long steps_to_perform,long dir)
{ 
  long current_speed_time = 0;
  
  // Set direction
  if(dir == 0)
  {
   digitalWrite(M6_ZSTEP,HIGH); // Enables the motor to move in a particular direction
  }
  else if (dir == 1)
  {
    digitalWrite(M6_ZSTEP,LOW); // Enables the motor to move in a particular direction
  }

  if(steps_to_perform < 500)
  {
    current_speed_time = low_speed_time;
  }
  else
  {
    current_speed_time = speed_time;
  }
  for(long x = 0; x < steps_to_perform*resolution_multiplier; x++)
  {

    digitalWrite(M6_ZSTEP,HIGH);  
    delayMicroseconds(current_speed_time/resolution_multiplier); 

    digitalWrite(M6_ZSTEP,LOW); 
    delayMicroseconds(current_speed_time/resolution_multiplier);
   }
}



#include "Arduino_Firmware.h"


long goToCoordonate(long initial_position, long final_position, char axis, long speed_time, long resolution_multiplier)
{
  if(axis == 'x')
  {
    xAxis_goToCoordonate(initial_position, final_position, speed_time, resolution_multiplier);
  }
  else if(axis == 'y')
  {
    //goToCoordanate_Y(initial_position, final_position, speed_time, resolution_multiplier);
  }
  else if(axis == 'z')
  {
    //goToCoordanate_Z(initial_position, final_position, speed_time, resolution_multiplier);
  }
  else
  {
    return 1;
  }
}

long xAxis_goToCoordonate(long initial_position, long final_position, long speed_time, long resolution_multiplier)
{ 
  long steps_to_perform;
  steps_to_perform = abs(final_position - initial_position);

  // Set direction
  if(final_position >= initial_position)
  {
   digitalWrite(M1_XDIR,HIGH); // Enables the motor to move in a particular direction
   digitalWrite(M2_XDIR,HIGH);
   digitalWrite(M3_XDIR,LOW);
   digitalWrite(M4_XDIR,LOW);
  }
  else
  {
    digitalWrite(M1_XDIR,LOW); // Enables the motor to move in a particular direction
    digitalWrite(M2_XDIR,LOW);
    digitalWrite(M3_XDIR,HIGH);
    digitalWrite(M4_XDIR,HIGH);
  }

  if(steps_to_perform < 500)
  {
    speed_time = low_speed_time;
  }
  for(long x = 0; x < steps_to_perform*resolution_multiplier; x++)
  {
    digitalWrite(M1_XSTEP,HIGH); 
    digitalWrite(M2_XSTEP,HIGH); 
    digitalWrite(M3_XSTEP,HIGH); 
    digitalWrite(M4_XSTEP,HIGH); 
    delayMicroseconds(speed_time/resolution_multiplier); 
    digitalWrite(M1_XSTEP,LOW); 
    digitalWrite(M2_XSTEP,LOW); 
    digitalWrite(M3_XSTEP,LOW); 
    digitalWrite(M4_XSTEP,LOW); 
    delayMicroseconds(speed_time/resolution_multiplier);
   }
   return final_position;
}
/*
long goToCoordonate_Y(long initial_position, long final_position, long speed_time, long resolution_multiplier)
{
  int step_pin = 0;
  int dir_pin = 0;

  
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

long goToCoordonate_Z(long initial_position, long final_position, long speed_time, long resolution_multiplier)
{
  int step_pin = 0;
  int dir_pin = 0;

  
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
*/
void goTo(long *initial_position, long *final_position, long speed_time, long resolution_multiplier)
{
  // initial_position[] is a matrix of the initial position [x, y, z]
  // final_position[] is a matrix of the final position [x, y, z]
  initial_position[0] = goToCoordonate(initial_position[0], final_position[0], 'x', speed_time, resolution_multiplier);
  //initial_position[1] = goToCoordonate(initial_position[1], final_position[1], 'y', speed_time, resolution_multiplier);
  //final_position[2] = goToCoordonate(initial_position[2], final_position[2], 'z', speed_time, resolution_multiplier);
}





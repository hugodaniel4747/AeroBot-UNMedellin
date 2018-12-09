#include "Arduino_Firmware.h"

void initGPIO()
{
  pinMode(M1_XSTEP,OUTPUT); 
  pinMode(M1_XDIR,OUTPUT);
  pinMode(M2_XSTEP,OUTPUT); 
  pinMode(M2_XDIR,OUTPUT);
  pinMode(M3_XSTEP,OUTPUT); 
  pinMode(M3_XDIR,OUTPUT);
  pinMode(M4_XSTEP,OUTPUT); 
  pinMode(M4_XDIR,OUTPUT);
  
  pinMode(M5_YSTEP,OUTPUT); 
  pinMode(M5_YDIR,OUTPUT);
  
  pinMode(M6_ZSTEP,OUTPUT); 
  pinMode(M6_ZDIR,OUTPUT);

  pinMode(EX,OUTPUT); 
  pinMode(EY,OUTPUT);
  pinMode(EZ,OUTPUT);

  pinMode(S1,OUTPUT); 
  pinMode(S2,OUTPUT);
  pinMode(S3,OUTPUT);
}

void setupEnable(void)
{
  digitalWrite(EX,LOW);
  digitalWrite(EY,LOW);
  digitalWrite(EZ,LOW);
}

void setupResolution(int resolution)
{
  if(resolution == 1)
  {
    digitalWrite(S1,LOW);
    digitalWrite(S2,LOW);
    digitalWrite(S3,LOW);
  }
  else if(resolution == 2)
  {
    digitalWrite(S1,HIGH);
    digitalWrite(S2,LOW);
    digitalWrite(S3,LOW);
  }
  else if(resolution == 4)
  {
    digitalWrite(S1,LOW);
    digitalWrite(S2,HIGH);
    digitalWrite(S3,LOW);
  }
  else if(resolution == 8)
  {
    digitalWrite(S1,HIGH);
    digitalWrite(S2,HIGH);
    digitalWrite(S3,LOW);
  }
  else 
  {
    digitalWrite(S1,HIGH);
    digitalWrite(S2,HIGH);
    digitalWrite(S3,HIGH);
  }
}

void enableMotor(char axis,int enable)
{
  //Enable LOW (0) enables the motors, HIGH (1) disables thems
  if (enable = 1)
  {
    if (axis == 'x')
    {
      digitalWrite(EX,HIGH);
    }
    if (axis == 'y')
    {
      digitalWrite(EY,HIGH);
    }
    if (axis == 'z')
    {
      digitalWrite(EZ,HIGH);
    }
  }
}

char convertAxis(int int_axis)
{
  char axis = "";
  if (int_axis == 0)
  {
    axis = 'x';
  }
  else if (int_axis == 1)
  {
    axis = 'y';
  }
  else if (int_axis == 2)
  {
    axis = 'z';
  }
  return axis;
}


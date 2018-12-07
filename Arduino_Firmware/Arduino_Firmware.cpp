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


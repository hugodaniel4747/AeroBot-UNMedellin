
#include "Arduino_Firmware.h"

long steps_to_perform = 0;
int dir = 0;
int int_axis = 0;
int axis = 0;
int enable = 0;

String inString = "";    // string to hold input

void setup()
{
  
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  delay(3000);
  while (!Serial)
  {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  Serial.print("Program Starts\n");
  
  // Sets pins as Outputs
  initGPIO();
  setupEnable();
  setupResolution(resolution_multiplier);
}

long val = 0;

int counter = 0;
int tableau[4] = {0,0,0,0};

void loop()
{
  //SECTION INTERFACE UTILISATEUR
  // Read serial input:
  
  while (Serial.available() > 0)
  {
    char inChar = Serial.read();
    if (isDigit(inChar))
    {
      // convert the incoming byte to a char and add it to the string:
      inString += (char)inChar;
    }
            
    // if you  a newline, get the instruction
    if (inChar == '\n')
    {
      val = inString.toInt();
     
      inString = "";
      tableau[counter] = val;
      counter++;
    }
  }
  if(counter > 3)
  {
    counter = 0;
    Serial.print('[');
    Serial.print(tableau[0]);
    Serial.print(',');
    Serial.print(tableau[1]);
    Serial.print(',');
    Serial.print(tableau[2]);
    Serial.print(',');
    Serial.print(tableau[3]);
    Serial.print("]\n");

    //Execute command
    axis = convertAxis(tableau[0]);
    steps_to_perform = tableau[1];
    dir = tableau[2];
    enable = tableau[3];
    enableMotor(axis, enable);
    goToWithRamp(steps_to_perform, dir, axis);
  }
}
  



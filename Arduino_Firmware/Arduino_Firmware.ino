
#include "Arduino_Firmware.h"

String resolution = "1/16";
long initial_position[3] = {0, 0, 0};
long final_position[3] = {0, 0, 0};
long speed_time = 100;
long ramp_start_time = 800;
long resolution_multiplier = 1000000;
String str = "";
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
  Serial.print("Enter new destination\n");
  
  // Sets pins as Outputs
  initGPIO();
  resolution_multiplier = setupResolution("1/16");
}
void loop()
{
  //SECTION INTERFACE UTILISATEUR
  // Read serial input:
  while (Serial.available() > 0)
  {
    
    int inChar = Serial.read();
    if (isDigit(inChar))
    {
      // convert the incoming byte to a char and add it to the string:
      inString += (char)inChar;
    }
    // if you get a newline, print the string, then the string's value:
    if (inChar == '\n')
    {
      final_position[0] = inString.toInt();
      inString = "";
      //Serial.print("Going to position: ");
      //Serial.print(final_position[0]);
      //Serial.print("\n");
      goToWithRamp(initial_position, final_position, speed_time, resolution_multiplier);
      //Serial.print("Arrived at position: ");
      //Serial.print(initial_position[0]);
      //Serial.print("\n");
      Serial.print("Enter new destination\n");
      delay(1000);
    }
  }
  //if (Serial.available()) //Lecture du buffer Serial
  //{
    /*str = Serial.readString();
    if (str == "end")
    {
      Serial.print("Going to: End...\n");
      final_position[0] = 3000;
      Serial.print("Enter new destination\n");
    }
    else if (str == "start")
    {
      Serial.print("Going to: Start...\n");
      final_position[0] = 0;
      Serial.print("Enter new destination\n");
    }*/
    //str = Serial.readString();
    //Serial.println(toInt(str));
    //goToWithRamp(initial_position, final_position, speed_time, resolution_multiplier);
    //delay(1000);
  //}
  /*
  final_position[0] = 3000;
  
  goToWithRamp(initial_position, final_position, speed_time, resolution_multiplier);
  //goTo(initial_position, final_position, speed_time, resolution_multiplier);
  delay(1000);
  final_position[0] = 0;
  goToWithRamp(initial_position, final_position, speed_time, resolution_multiplier);
  //goTo(initial_position, final_position, speed_time, resolution_multiplier);
  delay(1000);
  */
}



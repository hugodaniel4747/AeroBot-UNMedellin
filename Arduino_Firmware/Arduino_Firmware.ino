// defines pins numbers
const int X_STEP = 3; 
const int X_DIR = 2;  // 1 = CW, 0 = CCW
const int Y_STEP = 5; 
const int Y_DIR = 4;  // 1 = CW, 0 = CCW
const int Z_STEP = 7; 
const int Z_DIR = 6;  // 1 = CW, 0 = CCW
const int S1 = 8;
const int S2 = 9;
const int S3 = 10;

//Global variables
char resolution[] = "Full";
int initial_position[3] = {0, 0, 0};
int final_position[3] = {500, 0, 0};
int speed_time = 1500;
int ramp_start_time = 1000/16;

//Declare Functions
int rampSelector(int dist);
void setupResolution(char *resolution);
int goToCoordanate(int initial_position, int final_position, char axis, int speed_time);
int rampUp(int ramp_direction, int min_time, int steps_to_perform, char axis);
int rampDown(int ramp_direction, int min_time, int steps_to_perform, char axis);
void goTo(int *initial_position, int *final_position, int speed_time);
void goToWithRamp(int *initial_position, int *final_position, int speed_time);
int rampSelector(int dist);


void setup()
{
  // Sets the two pins as Outputs
  pinMode(X_STEP,OUTPUT); 
  pinMode(X_DIR,OUTPUT);
  pinMode(Y_STEP,OUTPUT); 
  pinMode(Y_DIR,OUTPUT);
  pinMode(Z_STEP,OUTPUT); 
  pinMode(Z_DIR,OUTPUT);
  pinMode(S1,OUTPUT); 
  pinMode(S2,OUTPUT);
  pinMode(S3,OUTPUT);
  digitalWrite(S1,HIGH);
  digitalWrite(S2,HIGH);
  digitalWrite(S3,HIGH);
  final_position[0] = 500;
  rampUp(1, 500/16, 500*16, 'x');
  goToCoordanate(0, 1000*16, 'x', 500/16);
  rampDown(1, 500/16, 500*16, 'x');
  delay(1000);
}
void loop()
{
  final_position[0] = 3000;
  
  /*goToWithRamp(initial_position, final_position, speed_time);
  delay(1000);
  final_position[0] = 0;
  goToWithRamp(initial_position, final_position, speed_time);
  delay(1000);
  */
}

void setupResolution(char *resolution)
{
  if(resolution == "Full")
  {
    digitalWrite(S1,LOW);
    digitalWrite(S2,LOW);
    digitalWrite(S3,LOW);
  }
  else if(resolution == "Half")
  {
    digitalWrite(S1,HIGH);
    digitalWrite(S2,LOW);
    digitalWrite(S3,LOW);
  }
  else if(resolution == "1/4")
  {
    digitalWrite(S1,LOW);
    digitalWrite(S2,HIGH);
    digitalWrite(S3,LOW);
  }
  else if(resolution == "1/8")
  {
    digitalWrite(S1,HIGH);
    digitalWrite(S2,HIGH);
    digitalWrite(S3,LOW);
  }
  else 
  {
    digitalWrite(S1,LOW);
    digitalWrite(S2,LOW);
    digitalWrite(S3,HIGH);
  }
}

int goToCoordanate(int initial_position, int final_position, char axis, int speed_time)
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
  
  int steps_to_perform = abs(final_position - initial_position);
  if(final_position >= initial_position)
  {
   digitalWrite(dir_pin,HIGH); // Enables the motor to move in a particular direction
  }
  else
  {
    digitalWrite(dir_pin,LOW); // Enables the motor to move in a particular direction
  }

  for(int x = 0; x < steps_to_perform; x++) {
    digitalWrite(step_pin,HIGH); 
    delayMicroseconds(speed_time); 
    digitalWrite(step_pin,LOW); 
    delayMicroseconds(speed_time);
   }
   return final_position;
}

int rampUp(int ramp_direction, int min_time, int steps_to_perform, char axis)
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

  int total_time = ramp_start_time/1000;
  float dt_dx = (float(ramp_start_time) - float(min_time))/float(steps_to_perform)/1000;
  for(int x=0; x < steps_to_perform; x = x + 1)
  {
    digitalWrite(step_pin,HIGH); 
    delayMicroseconds(total_time); 
    digitalWrite(step_pin,LOW); 
    delayMicroseconds(total_time); 
    total_time = (ramp_start_time/1000 - x*dt_dx)*1000;
  }  
}

int rampDown(int ramp_direction, int min_time, int steps_to_perform, char axis)
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

  int total_time = ramp_start_time;
  float dt_dx = (ramp_start_time - min_time)/steps_to_perform;
  for(int x=0; x < steps_to_perform; x = x + 1)
  {
    digitalWrite(step_pin,HIGH); 
    delayMicroseconds(total_time); 
    digitalWrite(step_pin,LOW); 
    delayMicroseconds(total_time); 
    total_time = ramp_start_time + x*dt_dx;
  }
}

void goTo(int *initial_position, int *final_position, int speed_time)
{
  // initial_position[] is a matrix of the initial position [x, y, z]
  // final_position[] is a matrix of the final position [x, y, z]
  initial_position[0] = goToCoordanate(initial_position[0], final_position[0], 'x', speed_time);
  initial_position[1] = goToCoordanate(initial_position[1], final_position[1], 'y', speed_time);
  //final_position[2] = goToCoordanate(initial_position[2], final_position[2], 'z', speed_time);
}

void goToWithRamp(int *initial_position, int *final_position, int speed_time)
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
  
  int x_dist = abs(final_position[0] - initial_position[0]);
  int y_dist = abs(final_position[1] - initial_position[1]);
  int z_dist = abs(final_position[2] - initial_position[2]);

  int ramp_dist= 0;
  // x axis
  ramp_dist = rampSelector(x_dist);
  rampUp(x_dir, speed_time, ramp_dist, 'x');
  initial_position[0] = goToCoordanate(initial_position[0]+ramp_dist, final_position[0]-ramp_dist, 'x', speed_time);
  rampDown(x_dir, speed_time, ramp_dist, 'x');
  initial_position[0] = final_position[0];

  // y axis
  ramp_dist = rampSelector(y_dist);
  rampUp(y_dir, speed_time, ramp_dist, 'y');
  initial_position[1] = goToCoordanate(initial_position[1]+ramp_dist, final_position[1]-ramp_dist, 'y', speed_time);
  rampDown(y_dir, speed_time, ramp_dist, 'y');
  initial_position[1] = final_position[1];

  // z axis
  ramp_dist = rampSelector(z_dist);
  rampUp(z_dir, speed_time, ramp_dist, 'z');
  initial_position[2] = goToCoordanate(initial_position[2]+ramp_dist, final_position[2]-ramp_dist, 'z', speed_time);
  rampDown(z_dir, speed_time, ramp_dist, 'z');
  initial_position[2] = final_position[2];
}

int rampSelector(int dist)
{
  if(dist >= 3000)
  {
    return 300;
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




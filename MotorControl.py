"""

    Editor: Hugo Daniel
    Project name: AreoponicBot U.N.
    Date: September 2018
    Location: Universidad National de Colombia sede Medellin
    File name: MotorControl.py

    Description: Motor algorythmes
    
    
"""

from time import sleep
import pigpio
import RPi.GPIO as GPIO
# Connect to pigpiod daemon
""" Need to creat shell script to give access to pigpio"""
pi = pigpio.pi()

#Global variables
DIR = 23     # Direction GPIO Pin
STEP = 24    # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation

X_POSITION = 0 # Current position in x axis

def initMotorGPIO(resolution="Full"): 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.output(DIR, CW)
    
    GPIO.setwarnings(False)
    
    setResolution(resolution)
    
def setResolution(resolution):
    MODE = (14, 15, 18)   # Microstep Resolution GPIO Pins
    GPIO.setup(MODE, GPIO.OUT)
    resolutionTableMode = {'Full': (0, 0, 0),
                           'Half': (1, 0, 0),
                           '1/4': (0, 1, 0),
                           '1/8': (1, 1, 0),
                           '1/16': (1, 1, 1)}
    GPIO.output(MODE, resolutionTableMode[resolution])
    
def clearMotorGPIO():
    pi.set_PWM_dutycycle(STEP, 0)  # PWM off
    pi.stop()
    GPIO.cleanup()
    

def goTo(y_position):
    
    # Set duty cycle and frequency
    pi.set_PWM_dutycycle(STEP, 128)  # 50% On 50% Off
    pi.set_PWM_frequency(STEP, 500)  # 500 pulses per second
    
    # Set duty cycle and frequency
    #pi.set_PWM_dutycycle(STEP, 128)  # 50% On 50% Off
    #pi.set_PWM_frequency(STEP, 2000)  # 500 pulses per second
    

def ramp():   
    # Ramp up
    generate_ramp([[6, 6],
                   [13, 13],
                   [25, 25],
                   [31, 31],
                   [50, 50],
                   [63, 63],
                   [100, 100],
                   [125, 125],
                   [156, 156],
                   [200, 200],
                   [250, 250],
                   [313, 313],
                   [500, 500],
                   [625, 625],
                   [1000, 1000],
                   [1250, 10000]])                   
    

        
def generate_ramp(ramp):
        """Generate ramp wave forms.
    
        ramp:  List of [Frequency, Steps]
        """
        pi.wave_clear()     # clear existing waves
        length = len(ramp)  # number of ramp levels
        wid = [-1] * length
    
        # Generate a wave per ramp level
        for i in range(length):
            frequency = ramp[i][0]
            micros = int(500000 / frequency)
            wf = []
            wf.append(pigpio.pulse(1 << STEP, 0, micros))  # pulse on
            wf.append(pigpio.pulse(0, 1 << STEP, micros))  # pulse off
            pi.wave_add_generic(wf)
            wid[i] = pi.wave_create()
    
        # Generate a chain of waves
        chain = []
        for i in range(length):
            steps = ramp[i][1]
            x = steps & 255
            y = steps >> 8
            chain += [255, 0, wid[i], 255, 1, x, y]
    
        pi.wave_chain(chain)  # Transmit chain.

def easyGoTo(resolution, x_destination):
    
    resolutionTableSize = {'Full':  1,
                           'Half':  2,
                           '1/4' :  4,
                           '1/8' :  8,
                           '1/16':  16}
    
    # Determine number of steps to perform
    """For the moment, position is in steps"""
    step_to_perform = abs(X_POSITION - x_destination)
    
    # Determine sens of rotation
    if X_POSITION - x_destination > 0:
        rotation = CCW
    else:
        rotation = CW
        
    step_count = step_to_perform*resolutionTableSize[resolution]
    delay = .005/resolutionTableSize[resolution]
    
    #print("Motor starting...")
    
    GPIO.output(DIR, rotation)
    for x in range(step_count):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
    
    sleep(.5)
        
    X_POSITION = x_destination
    
    #print("End of sequence")
    
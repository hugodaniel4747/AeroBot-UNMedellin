"""

    Editor: Hugo Daniel
    Project name: AreoponicBot U.N.
    Date: September 2018
    Location: Universidad National de Colombia sede Medellin
    File name: Gripper.py

    Description: Gripper control algorythmes
    
    
"""

import RPi.GPIO as GPIO
from time import sleep
import time
import pigpio

Raspberry_Analog_I = 24
Raspberry_Digital_I = 23
Raspberry_Digital_O = 18

pi = pigpio.pi()
 
class ToolChanger:    
    def __init__(self, tool):
        #init GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Raspberry_Digital_O, GPIO.OUT)
        GPIO.setup(Raspberry_Digital_I, GPIO.IN)
        GPIO.setup(Raspberry_Analog_I, GPIO.IN)
        sleep(2)
        
        if tool == "Gripper":
            self.Gripper = Gripper(500)
        elif tool == "Ultrasonic sensor":
            self.UntrasonicSensor = UltrasonicSensor()
        
    def cleanToolChanger():
        pi.stop()
        GPIO.cleanup() 
        
        
 


class Gripper:
    def __init__(self, position=500):
        self.position = position
        self.setGripperPosition(position)
        sleep(1)
    def setGripperPosition(self, position):
        self.position = position
        pi.set_servo_pulsewidth(Raspberry_Digital_O, position)
        sleep(1)
    def getGripperPosition(self):
        return self.position
    
class UltrasonicSensor:
    def __init__(self):
        self.distance = self.getDistance()  
        self.TRIG = Raspberry_Digital_O 
        self.ECHO = Raspberry_Digital_I          
    def getDistance(self):
        distance_to_average = 0
        average_devider = 20
        for x in range(0,average_devider):
            GPIO.output(self.TRIG, True)
            sleep(0.00001)
            GPIO.output(self.TRIG, False)    
            while GPIO.input(self.ECHO)==0:
                pulse_start = time.time()   
            while GPIO.input(self.ECHO)==1:
                pulse_end = time.time()    
            pulse_duration = pulse_end - pulse_start    
            raw_distance = pulse_duration * 17150  
            raw_distance = round(raw_distance, 2)
            distance_to_average = distance_to_average + raw_distance
        self.distance = distance_to_average/average_devider
    def getLastDistance(self):
        return self.distance

        
        
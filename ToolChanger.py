"""

    Editor: Hugo Daniel
    Project name: AreoponicBot U.N.
    Date: September 2018
    Location: Universidad National de Colombia sede Medellin
    File name: ToolChanger.py

    Description: Tool changer control algorythmes
    
    
"""

import RPi.GPIO as GPIO
from time import sleep
import time
import pigpio
import Microchip

Raspberry_Digital_I = 23
Raspberry_Digital_O = 18

pi = pigpio.pi()


class Tool:    
    def __init__(self, tool):
        #init GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Raspberry_Digital_O, GPIO.OUT)
        GPIO.setup(Raspberry_Digital_I, GPIO.IN)

        #init SPI for analog input
        self.SPI_bus = 0
        self.CE = 0
        self.MCP3201 = Microchip.MCP3201(self.SPI_bus, self.CE)       
        sleep(2)

        self.setCurrentTool(tool)

    def setCurrentTool(self, tool):
        if tool == "Gripper":
            self.current_tool = Gripper(500)
        elif tool == "Ultrasonic sensor":
            self.current_tool = UltrasonicSensor()
        else
            self.current_too = None
        
    def getAnalogInput(self):
        self.ADC_output_code = self.MCP3201.readADC_MSB()
        self.ADC_voltage_MSB = self.MCP3201.convert_to_voltage(self.ADC_output_code)
        #print("MCP3201 voltage: %0.2f V" % self.ADC_voltage_MSB)
        sleep(0.1)
        self.ADC_output_code = self.MCP3201.readADC_LSB()
        self.ADC_voltage_LSB = self.MCP3201.convert_to_voltage(self.ADC_output_code)
        #print("MCP3201 voltage: %0.2f V" % self.ADC_voltage_LSB)
        self.analog_voltage = (float(self.ADC_voltage_MSB) + float(self.ADC_voltage_LSB))/2       
        return self.analog_voltage
        
    def cleanToolChanger(self):
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
        self.TRIG = Raspberry_Digital_O 
        self.ECHO = Raspberry_Digital_I
        self.distance = self.getDistance()  
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
        return self.distance
    def getLastDistance(self):
        return self.distance

        

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 11:59:30 2018

@author: hugodaniel
"""

 # 
 # Editor     : YouYou from DFRobot
 # Date       : 23.04.2014
 # E-Mail	: youyou.yu@dfrobot.com

 # Product name: Analog EC Meter
 # Product SKU : DFR0300
 # Version     : 1.0

 # Description:
 # Sample code for testing the EC meter and get the data feedback from the Arduino Serial Monitor.

 # Connection:
 #        EC meter output     -> Analog pin 1
 #        DS18B20 digital pin -> Digital pin 2
 #

import time
from time import sleep
import os
import Microchip

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
temp_sensor = "sys/bus/w1/devices/28-000005e2fdc3/w1_slave"

#init SPI for analog input
SPI_bus = 0
CE = 0
MCP3201 = Microchip.MCP3201(SPI_bus, CE)       
sleep(2)


def temp_raw():

    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():

    lines = temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = temp_raw()
    temp_output = lines[1].find('t=')

    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
    
def getAnalogInput():
    ADC_output_code = MCP3201.readADC_MSB()
    ADC_voltage_MSB = MCP3201.convert_to_voltage(ADC_output_code)
    #print("MCP3201 voltage: %0.2f V" % self.ADC_voltage_MSB)
    sleep(0.1)
    ADC_output_code = MCP3201.readADC_LSB()
    ADC_voltage_LSB = MCP3201.convert_to_voltage(ADC_output_code)
    #print("MCP3201 voltage: %0.2f V" % self.ADC_voltage_LSB)
    analog_voltage = (float(ADC_voltage_MSB) + float(ADC_voltage_LSB))/2       
    return analog_voltage


StartConvert = 0
ReadTemperature = 1

numReadings = 20            #the number of sample times
#ECsensorPin = A1            #EC Meter analog output,pin on analog 1
DS18B20_Pin = 2             #DS18B20 signal, pin on digital 2
AnalogSampleInterval = 25
printInterval = 700
tempSampleInterval = 850    #analog sample interval;serial print interval;temperature sample interval
readings = []       #3the readings from the analog input
AnalogAverage = 0
averageVoltage = 0          #the average
AnalogSampleTime = 0
printTime = 0

#float temperature,ECcurrent; 
 
#Temperature chip i/o
#OneWire ds(DS18B20_Pin)     #on digital pin 2

#initialize all the readings to 0:
for thisReading in range(numReadings):
    readings[thisReading] = 0
#TempProcess(StartConvert)   #let the DS18B20 start the convert
tempSampleTime = time.time()


def loop():
  
    #Every once in a while,sample the analog value and calculate the average.
      
    AnalogSampleTime = time.time()
    AnalogValueTotal = 0        #the running total
    index = 0                   #the index of the current reading
    tempSampleTime = 0
    printTime = time.time()
    
    if(time.time() - AnalogSampleTime) >= AnalogSampleInterval:
        AnalogSampleTime = time.time()
         # subtract the last reading:
        AnalogValueTotal = AnalogValueTotal - readings[index]
        # read from the sensor:
        readings[index] = getAnalogInput
        # add the reading to the total:
        AnalogValueTotal = AnalogValueTotal + readings[index]
        # advance to the next position in the array:
        index = index + 1
        # if we're at the end of the array...
        if (index >= numReadings):
            # ...wrap around to the beginning:
            index = 0
        # calculate the average:
        AnalogAverage = AnalogValueTotal / numReadings
        
    """
     Every once in a while,MCU read the temperature from the DS18B20 and then let the DS18B20 start the convert.
     Attention:The interval between start the convert and read the temperature should be greater than 750 millisecond,or the temperature is not accurate!
    """
    if (time.time() - tempSampleTime) >= tempSampleInterval:  
         tempSampleTime = time.time()
         temperature = read_temp()  # read the current temperature from the  DS18B20

        
    """
     Every once in a while,print the information on the serial monitor.
    """
    if (time.time() - printTime) >= printInterval:
        printTime = time.time()
        averageVoltage = AnalogAverage * 5000/1024
        print("Analog value: " + AnalogAverage) #analog average,from 0 to 1023      
        print("Voltage: " + averageVoltage + "mV") #millivolt average,from 0mv to 4995mV
        print("temp: " + temperature + "°C")  #current temperature 
        
        TempCoefficient = 1.0 + 0.0185 * (temperature - 25.0)    #temperature compensation formula: fFinalResult(25^C) = fFinalResult(current)/(1.0+0.0185*(fTP-25.0));
        CoefficientVolatge = averageVoltage/TempCoefficient   
        if CoefficientVolatge < 150:
            print("No solution!")   #25^C 1413us/cm<-->about 216mv  if the voltage(compensate)<150,that is <1ms/cm,out of the range
        elif CoefficientVolatge > 3300:
            print("Out of the range!")  #>20ms/cm,out of the range
        else: 
            if CoefficientVolatge <= 448:
                ECcurrent = 6.84 * CoefficientVolatge - 64.32   #1ms/cm<EC<=3ms/cm
            elif CoefficientVolatge <= 1457:
                ECcurrent = 6.98 * CoefficientVolatge - 127  #3ms/cm<EC<=10ms/cm
            else:
                ECcurrent = 5.3 * CoefficientVolatge + 2278    #10ms/cm<EC<20ms/cm
            ECcurrent = ECcurrent/1000    #convert us/cm to ms/cm
            print("EC: " + ECcurrent + "ms/cm")  #two decimal

"""
ch=0,let the DS18B20 start the convert;ch=1,MCU read the current temperature from the DS18B20.
"""
"""
def TempProcess(ch):

    #returns the temperature from one DS18B20 in DEG Celsius
    #static byte data[12];
    #static byte addr[8];
    #static float TemperatureSum
    if not(ch):
        if not(ds.search(addr)):
            Serial.println("no more sensors on chain, reset search!")
            ds.reset_search()
            return 0
                      
#        if OneWire::crc8( addr, 7) != addr[7]:
#            Serial.println("CRC is not valid!")
#            return 0
            
        if addr[0] != 0x10 and addr[0] != 0x28:
            Serial.print("Device is not recognized!")
            return 0
    
        ds.reset()
        ds.select(addr)
        ds.write(0x44,1) # start conversion, with parasite power on at the end
            
    else:
        present = ds.reset()
        ds.select(addr)    
        ds.write(0xBE)  # Read Scratchpad            
        for i in range(9): # we need 9 bytes
            data[i] = ds.read()
               
        ds.reset_search()          
        MSB = data[1]
        LSB = data[0]       
        tempRead = ((MSB << 8) | LSB)  #using two's compliment
        TemperatureSum = tempRead / 16
        
    return TemperatureSum  
"""    

if __name__=="__main__":
    loop()
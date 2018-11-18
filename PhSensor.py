"""

    Autor: Hugo Daniel
    Project name: AreoponicBot U.N.
    Date: September 2018
    Location: Universidad National de Colombia sede Medellin
    File name: PhSensor.py

    Description: Ph sensor code
    
    STATE: NOT TERMINATED    
    
"""

import time
import Microchip




 # This sample code is used to test the pH meter Pro V1.0.
 # Editor : YouYou
 # Ver    : 1.0
 # Product: analog pH meter Pro
 # SKU    : SEN0169

Offset = 0            #deviation compensate
samplingInterval = 20
printInterval = 800
ArrayLenth  = 40    #times of collection
pHArray = []   #Store the average value of the sensor feedback
 
SPI_bus = 0
CE = 0
MCP3201 = Microchip.MCP3201(SPI_bus, CE)
time.sleep(0.1)
    

def loop():
    pHArrayIndex = 0
    while True:
        samplingTime = time.time()
        printTime = time.time()
        if (time.time() - samplingTime) > samplingInterval:
            
            ADC_output_code = MCP3201.readADC_MSB()
            pHArrayIndex = pHArrayIndex + 1
            pHArray[pHArrayIndex] = MCP3201.convert_to_voltage(ADC_output_code)
            if pHArrayIndex == ArrayLenth:
                pHArrayIndex = 0
            voltage = avergearray(pHArray, ArrayLenth)*5.0/1024
            pHValue = 3.5*voltage+Offset
            samplingTime = time.time()
        
        if(time.time() - printTime) > printInterval:   #Every 800 milliseconds, print a numerical, convert the state of the LED indicator
            print("Voltage:" + voltage + "    pH value: "+ pHValue)
            printTime = time.time()
      
def avergearray(arr, number):

    amount = 0
    if number <=0:
        print("Error number for the array to avraging!/n")
        return 0

    if number<5:  #less than 5, calculated directly statistics
        for i in range(number):
            amount += arr[i]
        avg = amount/number
        return avg;
    else:
        if arr[0] < arr[1]:
            min_ = arr[0]
            max_ = arr[1]
        else:
            min_ = arr[1]
            max_ = arr[0]
      
        for i in range(2,number):
            if arr[i] < min_:
                amount += min_        #arr<min
                min_ = arr[i]
            else:
                if arr[i] > max_:
                    amount += max_    #arr>max
                    max_ = arr[i]
                else:
                    amount += arr[i] #min<=arr<=max
          
    avg = amount/(number-2)
      
    return avg

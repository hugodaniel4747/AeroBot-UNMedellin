#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 15:35:14 2018

@author: hugodaniel
"""


# Libraries
import warnings
import serial
import serial.tools.list_ports

# Global def

# Function that connect the Pi to an Arduino
def setUpArduino():
    arduino_ports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if 'ACM' in p.description or "Arduino" in p.description 
    ]
    #print(arduino_ports)
    if not arduino_ports:
        #raise IOError("No Arduino found")
        return False
    if len(arduino_ports) > 1:
        warnings.warn('Multiple Arduinos found - using the first')
    
    return arduino_ports

# Function that return True if input is a int
def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def main():   
    print("main: ")
    
    # Init comm arduino
    arduino_ports = setUpArduino()
    #init serial comm between arduino and raspberry pi
    if arduino_ports != False:
        ser = serial.Serial(arduino_ports[0], 9600, 8, 'N', 1, timeout=1)
    else:
        print("Arduino Connexion failed")    
    
    while True:
        try:
            data = ser.readline()

            if data.decode() == "Ready for new command":
                command = input('Enter an axis: ')  
                ser.write(command.encode())
                ser.write('\n'.encode())
                command = input('Enter an number of steps: ') 
                ser.write(command.encode())
                ser.write('\n'.encode())
                command = input('Enter a direction: ') 
                ser.write(command.encode())
                ser.write('\n'.encode())
                command = input('Enter a enable: ') 
                ser.write(command.encode())
                ser.write('\n'.encode())
        except (KeyboardInterrupt):
            print('\n', "Exit on Ctrl-C")
        
        except:
            print("Other error or exception occurred!")
            raise
    
        finally:
            print
    
    
if __name__=="__main__":
    main()
    

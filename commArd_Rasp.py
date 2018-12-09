#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 15:35:14 2018

@author: hugodaniel
"""


# Libraries
import cv2
import AeroGarden
import Vision
#import ToolChanger
import warnings
import serial
import serial.tools.list_ports

# Global def
Tresh_Area = 100
Dist_Tresh = 150
# My_Path is used to point to the image directory.
# My_path = "/home/pi/Documents/GitRepo/Image" # For th Raspberry pi
My_Path = "/Users/hugodaniel/Desktop/StageMedellin/GitRepo/Image" # For my computer

# Function that connect the Pi to an Arduino
def setUpArduino():
    arduino_ports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if 'ACM' in p.description or "Arduino" in p.description 
    ]
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

# Function used to set up the garden    
def setUpGarden(GARDEN):
    #Garden initialisation
    
    GARDEN.addRow()
    GARDEN.addBed(0, AeroGarden.IcorporTEST())
    
    GARDEN.displayGardenMap()
    GARDEN.addPlantMapGarden(0,0,0,0,AeroGarden.DictOfPlantes.myPlants[1])
    GARDEN.displayGardenMap()
    GARDEN.addSetOfPlantsMap(AeroGarden.DictOfPlantes.myPlants[2],3)
    GARDEN.displayGardenMap()
    GARDEN.updatePlantsArea()
    GARDEN.displayGardenMapAreas()

def main():   
    print("main: ")
    
    # Global def
    #Image_Directory = "/Users/hugodaniel/MATLAB-Drive/Medellin/Images/bebeplantes.jpg"

    # Init Tool Changer
    #Tool = ToolChanger.Tool("Gripper")
    
    # Init Garden
    G = AeroGarden.Garden()
    #setUpGarden(G)
    #G.updatePlantsArea()
    #G.displayGardenMapAreas()
    
    # Init comm arduino
    arduino_ports = setUpArduino()
    #init serial comm between arduino and raspberry pi
    if arduino_ports != False:
        ser = serial.Serial(arduino_ports[0], 9600, 8, 'N', 1, timeout=1)
    
    
    try:
        while True:
            data = ser.readreadline()    
            if data == "Ready for new command":
                command = input('Enter an axis: ')  
                ser.write(command)
                command = input('Enter an number of steps: ') 
                ser.write(command)
                command = input('Enter a direction: ') 
                ser.write(command)
                command = input('Enter a enable: ') 
                ser.write(command)
                
    except (KeyboardInterrupt):
        Tool.cleanToolChanger()
        print('\n', "Exit on Ctrl-C")
        
    except:
        print("Other error or exception occurred!")
        raise
    
    finally:
        print
    
    Tool.cleanToolChanger()
    
if __name__=="__main__":
    main()
    
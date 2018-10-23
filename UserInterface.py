#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 20:41:27 2018

@author: hugodaniel
"""

from guizero import App, Text, TextBox, PushButton, Slider, Picture, Box, Combo
import cv2
import AeroGarden
import Vision
import warnings
import serial
import serial.tools.list_ports
from time import sleep

# Global def
Tresh_Area = 100
Dist_Tresh = 150

def setUpArduino():
    arduino_ports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if 'ACM' or "Arduino" in p.description
    ]
    if not arduino_ports:
        raise IOError("No Arduino found")
    if len(arduino_ports) > 1:
        warnings.warn('Multiple Arduinos found - using the first')
    
    return arduino_ports


def updateCNCPosition():
    CNC_current_position.value = 3000
    
def updateTool(selected_tool):
    if selected_tool == "Gripper":
        boxUltrasonicSensor.disable()
        boxUltrasonicSensor.hide()
        boxGripper.enable()
        boxGripper.show()
    elif selected_tool == "Ultrasonic sensor":
        boxGripper.disable()
        boxGripper.hide()
        boxUltrasonicSensor.enable()
        boxUltrasonicSensor.show()
    else:
        boxGripper.disable()
        boxGripper.hide()
        boxUltrasonicSensor.disable()
        boxUltrasonicSensor.hide()

def openGripper():
    gripper_state.value = "Open"
def closeGripper():
    gripper_state.value = "Close"
    
def updateUltrasonicSensorDistance():
    distance.value = 40
    
def takePhoto():
    Vision.storeCapture("/Users/hugodaniel/Desktop/imageTest.jpg")
    Vision.resizeImage("/Users/hugodaniel/Desktop/imageTest.jpg", 1000)
    app2 = App()
    Picture(app2, image="/Users/hugodaniel/Desktop/imageTest.jpg")
    
def analysePlants():
    app2 = App()
    
    #Plants detection
    Vision.storeCapture("/Users/hugodaniel/Desktop/imageTest.jpg",1)
    img = Vision.getImageFromComputer("/Users/hugodaniel/Desktop/imageTest.jpg")
    contours = Vision.pipelineGetContours(img)
    listOfAreas = Vision.drawAreasBoundingBox(img, contours, Tresh_Area)
    listCenterAreas = Vision.findCenterPlant(img, listOfAreas, 200)
    
    cv2.imwrite("/Users/hugodaniel/Desktop/imageTest.jpg", img)
    Picture(app2, image="/Users/hugodaniel/Desktop/imageTest.jpg")



# APP  
app = App(title="AeroponicBot Gripper GUI", layout="grid", height=200, width=400)

text_CNC_current_position= Text(app, grid=[0,0], text="Current position", align="left")
CNC_current_position= Text(app, grid=[1,0], text="0")
text_CNC= Text(app, text="X axis", grid=[0,1], align="left")
input_CNC = TextBox(app, command=updateCNCPosition, grid=[1,1]) 

text_tool= Text(app, text="Current tool", grid=[0,3], align="left")
current_tool = Combo(app, options=["None", "Gripper" , "Ultrasonic sensor"], grid=[1,3], command=updateTool, align="left")

capture = PushButton(app, command=takePhoto, grid=[0,2], align="left", text="Take a picture")
capture2 = PushButton(app, command=analysePlants, grid=[1,2], align="left", text="Analyse plant areas")

# Box Gripper
boxGripper = Box(app, layout="grid", grid=[0,4], enabled=False, visible=False)
text_gripper = Text(boxGripper, text="Gripper state: ", grid=[0,4], align="left")
gripper_state = Text(boxGripper, grid=[1,4], text="Open")
button_gripper_open = PushButton(boxGripper, command=openGripper, text="Open", grid=[0,5])
button_gripper_close = PushButton(boxGripper, command=closeGripper, text="Close", grid=[2,5])

# Box Ultrasonic sensor
boxUltrasonicSensor = Box(app, layout="grid", grid=[0,4], enabled=False, visible=False)
text_ultrasonic_sensor = Text(boxUltrasonicSensor, grid=[0,4], text="Distance: ")
distance = Text(boxUltrasonicSensor, grid=[1,3])
distance.repeat(500,updateUltrasonicSensorDistance)

app.display()

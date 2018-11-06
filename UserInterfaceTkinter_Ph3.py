#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 20:41:27 2018

@author: hugodaniel
"""

import tkinter as tk
import tkinter.ttk as ttk
import cv2
import AeroGarden
import Vision
#import ToolChanger
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


class CurrentPosition:
    # Current position
    def __init__(self, frame):
        self.text_CNC_current_position = tk.Label(frame, text="Current position")
        self.text_CNC_current_position.grid(column=0, row=0)

        self.CNC_current_position = tk.Label(frame, text="0")
        self.CNC_current_position.grid(column=1, row=0)

        self.text_CNC = tk.Label(frame, text="X axis")
        self.text_CNC.grid(column=0, row=1)

        self.input_CNC = tk.Entry(frame,width=10)
        self.input_CNC.grid(column=1, row=1)
        self.input_CNC.bind('<Return>',self.updateCNCPosition)

    def updateCNCPosition(self, event):
        self.CNC_current_position.configure(text=3000)

class Capture:
    # Capture
    def __init__(self, frame):
        self.capture = tk.Button(frame, command=self.takePhoto, text="Take a picture")
        self.capture.grid(column=0, row=0)
        self.capture2 = tk.Button(frame, command=self.analysePlants, text="Analyse plant areas")
        self.capture2.grid(column=1, row=0)

    def takePhoto(self):
        Vision.storeCapture("/home/pi/Desktop/imageTest.png")
        Vision.resizeImage("/home/pi/Desktop/imageTest.png", 1000)
        self.top = tk.Toplevel()
        self.top.title("Capture")
        self.canvas = tk.Canvas(self.top, width=1000, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.capture = tk.PhotoImage(file="/home/pi/Desktop/imageTest.png")
        self.canvas.create_image(500,300,image=self.capture)
        self.canvas.image = self.capture
    
    def analysePlants(self):
        #Plants detection
        Vision.storeCapture("/home/pi/Desktop/imageTest.png")
        self.img = Vision.getImageFromComputer("/home/pi/Desktop/imageTest.png")
        self.contours = Vision.pipelineGetContours(self.img)
        self.listOfAreas = Vision.drawAreasBoundingBox(self.img, self.contours, Tresh_Area)
        self.listCenterAreas = Vision.findCenterPlant(self.img, self.listOfAreas, 200)
        
        cv2.imwrite("/home/pi/Desktop/imageTest.png", self.img)

        self.top = tk.Toplevel()
        self.top.title("Analyse capture")
        self.canvas = tk.Canvas(self.top, width=1000, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.capture = tk.PhotoImage(file="/home/pi/Desktop/imageTest.png")
        self.canvas.create_image(500,300,image=self.capture)
        self.canvas.image = self.capture

class CurrentTool:
    # Current tool
    def __init__(self, frame, Gripper, Ultra_Sonic_Sensor):        
        self.text_tool= tk.Label(frame, text="Current tool")
        self.text_tool.grid(column=0, row=0)
        
        self.combo = ttk.Combobox(frame) 
        self.combo['values']= ("None", "Gripper" , "Ultrasonic sensor")
        self.combo.current(0) #set the selected item
        self.combo.grid(column=1, row=0)
        self.gripper = Gripper
        self.ultra_sonic_sensor = Ultra_Sonic_Sensor
        def handler(event, self=self):
                return self.updateTool(event)
        self.combo.bind("<<ComboboxSelected>>", handler)
        

    def updateTool(self, event):
        #init ToolChanger
        #self.Tool = ToolChanger.Tool("None")
        self.selected_tool = self.combo.get()
        self.gripper.button_gripper_open.configure(state=tk.DISABLED)
        self.gripper.button_gripper_close.configure(state=tk.DISABLED)
        self.gripper.gripper_state.configure(text="--")
        self.ultra_sonic_sensor.distance_untrasonic_sensor.grid_remove()
        
        self.gripper.blurGripperImage()
        if self.selected_tool == "Gripper":
            #self.Tool.setCurrentTool("Gripper")
            self.gripper.gripper_state.configure(text="Open")
            self.gripper.openGripperImage()
            self.gripper.button_gripper_open.configure(state=tk.NORMAL)
            self.gripper.button_gripper_close.configure(state=tk.NORMAL)
        elif self.selected_tool == "Ultrasonic sensor":
            #self.Tool.setCurrentTool("Ultrasonic sensor")
            self.ultra_sonic_sensor.distance_untrasonic_sensor.grid()
    
class Gripper:
    # Gripper
    def __init__(self, frame, frame_tool):
        self.frame_tool = frame_tool
        self.text_gripper = tk.Label(frame, text="State: ")
        self.text_gripper.grid(column=0, row =0)
        self.gripper_state = tk.Label(frame, text="--")
        self.gripper_state.grid(column=1, row =0)
        self.button_gripper_open = tk.Button(frame, text="Open", command=self.openGripper, state=tk.DISABLED)
        self.button_gripper_open.grid(column=0, row =1)
        self.button_gripper_close = tk.Button(frame, text="Close", command=self.closeGripper, state=tk.DISABLED)
        self.button_gripper_close.grid(column=1, row =1)
        
        #Init gripper image
        self.canvas = tk.Canvas(self.frame_tool, width=100, height=100, state=tk.DISABLED)
        self.canvas.pack(fill="both", expand=True)
        self.blurGripperImage()

    def openGripper(self):
        self.gripper_state.configure(text="Open")
        self.openGripperImage()
        
    def closeGripper(self):
        self.gripper_state.configure(text="Close")
        self.closeGripperImage()
        
    def openGripperImage(self):
        Vision.resizeImage("/home/pi/Documents/GitRepo/GripperOpen.png", 100)
        self.capture = tk.PhotoImage(file="/home/pi/Documents/GitRepo/GripperOpen.png")
        self.canvas.create_image(50,50,image=self.capture)
        self.canvas.image = self.capture
        
    def closeGripperImage(self):
        Vision.resizeImage("/home/pi/Documents/GitRepo/GripperClose.png", 100)
        self.capture = tk.PhotoImage(file="/home/pi/Documents/GitRepo/GripperClose.png")
        self.canvas.create_image(50,50,image=self.capture)
        self.canvas.image = self.capture
        
    def blurGripperImage(self):
        Vision.resizeImage("/home/pi/Documents/GitRepo/GripperBlur.png", 100)
        self.capture = tk.PhotoImage(file="/home/pi/Documents/GitRepo/GripperBlur.png")
        self.canvas.create_image(50,50,image=self.capture)
        self.canvas.image = self.capture

class UltraSonicSensor:
    # Ultrasonic sensor
    def __init__(self, frame):
        self.text_ultrasonic_sensor = tk.Label(frame, text="Distance: ")
        self.text_ultrasonic_sensor.grid(column=0, row =0)
        self.distance_untrasonic_sensor = tk.Label(frame)
        self.distance_untrasonic_sensor.grid(column=1, row =0)
        frame.after(500, self.updateUltrasonicSensorDistance)
        self.distance_untrasonic_sensor.grid_remove()

    def updateUltrasonicSensorDistance(self):
        self.distance_untrasonic_sensor.configure(text=40)

class MainApplication:
    def __init__(self, master):
        # Window init
        master.title("AeroponicBot GUI")
        master.geometry('600x450')

        # Frames
        frame_current_position = tk.LabelFrame(master, text="Current robot position")
        frame_current_position.grid(column=0, row=0, padx=5, pady=5)
        frame_capture = tk.LabelFrame(master, text="Camera")
        frame_capture.grid(column=0, row=1, padx=2, pady=5)
        frame_current_tool = tk.LabelFrame(master, text="Tool changer")
        frame_current_tool.grid(column=0, row=2, padx=5, pady=0)
        frame_gripper = tk.LabelFrame(frame_current_tool, text="Gripper")
        frame_gripper.grid(column=0, row=3, padx=5, pady=2)
        frame_ultra_sonic_sensor = tk.LabelFrame(frame_current_tool, text="Ultrasonic sensor")
        frame_ultra_sonic_sensor.grid(column=0, row=4, padx=2, pady=2)
        
        frame_photo = tk.Frame(frame_current_tool)
        frame_photo.grid(column=1, row=3, padx=5, pady=5)
        
        # Setup Widgets
        self.current_position = CurrentPosition(frame_current_position)
        self.capture = Capture(frame_capture)
        self.gripper = Gripper(frame_gripper, frame_photo)
        self.ultra_sonic_sensor = UltraSonicSensor(frame_ultra_sonic_sensor)
        self.current_tool = CurrentTool(frame_current_tool, self.gripper, self.ultra_sonic_sensor)
        


#start user interface loop
if __name__ == "__main__":
    #Init comm arduino
    #arduino_ports = setUpArduino()
    #init serial comm between arduino and raspberry pi
    #if arduino_ports != False:
    #    ser = serial.Serial(arduino_ports[0], 9600, 8, 'N', 1, timeout=1)

    #Init Garden
    G = AeroGarden.Garden()
    #setUpGarden(G)
    #G.updatePlantsArea()
    #G.displayGardenMapAreas()
    
    master = tk.Tk()
    MainApplication(master)
    while True:
        try:
            master.mainloop()
            break
        except UnicodeDecodeError:
            pass  


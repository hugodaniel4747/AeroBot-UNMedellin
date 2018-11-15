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
My_Path = "/Users/hugodaniel/Desktop/StageMedellin/GitRepo/Image"


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
        #Tool.current_tool.setGripperPosition(self.input_CNC.get())
        self.CNC_current_position.configure(text=3000)#str(self.input_CNC.get()))

class Capture:
    # Capture
    def __init__(self, frame):
        self.capture = tk.Button(frame, command=self.takePhoto, text="Take a picture")
        self.capture.grid(column=0, row=0)
        self.capture2 = tk.Button(frame, command=self.analysePlants, text="Analyse plant areas")
        self.capture2.grid(column=1, row=0)

    def takePhoto(self):
        Vision.storeCapture(My_Path+"/imageTest.png")
        Vision.resizeImage(My_Path+"/imageTest.png", 1000)
        self.top = tk.Toplevel()
        self.top.title("Capture")
        self.canvas = tk.Canvas(self.top, width=1000, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.capture = tk.PhotoImage(file=(My_Path+"/imageTest.png"))
        self.canvas.create_image(500,300,image=self.capture)
        self.canvas.image = self.capture
    
    def analysePlants(self):
        #Plants detection
        Vision.storeCapture(My_Path+"/imageTest.png")
        self.img = Vision.getImageFromComputer(My_Path+"/imageTest.png")
        self.contours = Vision.pipelineGetContours(self.img)
        self.listOfAreas = Vision.drawAreasBoundingBox(self.img, self.contours, Tresh_Area)
        self.listCenterAreas = Vision.findCenterPlant(self.img, self.listOfAreas, 200)
        
        cv2.imwrite(My_Path+"/imageTest.png", self.img)

        self.top = tk.Toplevel()
        self.top.title("Analyse capture")
        self.canvas = tk.Canvas(self.top, width=1000, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.capture = tk.PhotoImage(file=(My_Path+"/imageTest.png"))
        self.canvas.create_image(500,300,image=self.capture)
        self.canvas.image = self.capture

class CurrentTool:
    # Current tool
    def __init__(self, frame, Gripper, Ultrasonic_Sensor, EC_Sensor, Temperature_Sensor, Ph_Sensor):        
        self.text_tool= tk.Label(frame, text="Current tool")
        self.text_tool.grid(column=0, row=0)
        
        self.combo = ttk.Combobox(frame) 
        self.combo['values']= ("No Tool", "Gripper" , "Ultrasonic sensor", "EC and temperature sensor", "Ph sensor")
        self.combo.current(0) #set the selected item
        self.combo.grid(column=1, row=0)
        self.gripper = Gripper
        self.ultrasonic_sensor = Ultrasonic_Sensor
        self.ec_sensor = EC_Sensor
        self.temperature_sensor = Temperature_Sensor
        self.ph_sensor = Ph_Sensor
        def handler(event, self=self):
                return self.updateTool(event)
        self.combo.bind("<<ComboboxSelected>>", handler)
        

    def updateTool(self, event):
        #update ToolChanger
        #Tool.setCurrentTool("None")
        
        self.selected_tool = self.combo.get()
        self.gripper.button_gripper_open.configure(state=tk.DISABLED)
        self.gripper.button_gripper_close.configure(state=tk.DISABLED)
        self.gripper.gripper_state.configure(text="--")
        self.ultrasonic_sensor.active = False
        self.ultrasonic_sensor.updateUltrasonicSensor()
        self.ec_sensor.active = False
        self.ec_sensor.updateECSensor()
        self.temperature_sensor.active = False
        self.temperature_sensor.updateTemperatureSensor()
        self.ph_sensor.active = False
        self.ph_sensor.updatePhSensor() 
        
        self.gripper.blurGripperImage()
        
        if self.selected_tool == "Gripper":
            #Tool.setCurrentTool("Gripper")
            
            self.gripper.gripper_state.configure(text="Open")
            self.gripper.openGripperImage()
            self.gripper.button_gripper_open.configure(state=tk.NORMAL)
            self.gripper.button_gripper_close.configure(state=tk.NORMAL)
        elif self.selected_tool == "Ultrasonic sensor":
            #Tool.setCurrentTool("Ultrasonic sensor")
            self.ultrasonic_sensor.active = True
            self.ultrasonic_sensor.updateUltrasonicSensor()
            #self.ultrasonic_sensor.distance_untrasonic_sensor.grid()
        elif self.selected_tool == "EC and temperature sensor":
            #Tool.setCurrentTool("ECTempSensor")
            
            self.ec_sensor.active = True
            self.ec_sensor.updateECSensor()
            self.temperature_sensor.active = True
            self.temperature_sensor.updateTemperatureSensor()
        elif self.selected_tool == "Ph sensor":
            #Tool.setCurrentTool("PhSensor")
            
            self.ph_sensor.active = True
            self.ph_sensor.updatePhSensor() 
    
class Gripper:
    # Gripper
    def __init__(self, frame, frame_photo):
        self.frame_photo = frame_photo
        self.text_gripper = tk.Label(frame, text="State: ")
        self.text_gripper.grid(column=0, row =0)
        self.gripper_state = tk.Label(frame, text="--")
        self.gripper_state.grid(column=1, row =0)
        self.button_gripper_open = tk.Button(frame, text="Open", command=self.openGripper, state=tk.DISABLED)
        self.button_gripper_open.grid(column=0, row =1)
        self.button_gripper_close = tk.Button(frame, text="Close", command=self.closeGripper, state=tk.DISABLED)
        self.button_gripper_close.grid(column=1, row =1)
        
        #Init gripper image
        self.canvas = tk.Canvas(self.frame_photo, width=100, height=100, state=tk.DISABLED)
        self.canvas.pack(fill="both", expand=True)
        self.blurGripperImage()

    def openGripper(self):
        #Tool.current_tool.setGripperPosition(1900)
        
        self.gripper_state.configure(text="Open")
        self.openGripperImage()
        
    def closeGripper(self):
        #Tool.current_tool.setGripperPosition(1400)
        
        self.gripper_state.configure(text="Close")
        self.closeGripperImage()
        
    def openGripperImage(self):
        Vision.resizeImage(My_Path+"/GripperOpen.png", 100)
        self.capture = tk.PhotoImage(file=(My_Path+"/GripperOpen.png"))
        self.canvas.create_image(50,50,image=self.capture)
        self.canvas.image = self.capture
        
    def closeGripperImage(self):
        Vision.resizeImage(My_Path+"/GripperClose.png", 100)
        self.capture = tk.PhotoImage(file=(My_Path+"/GripperClose.png"))
        self.canvas.create_image(50,50,image=self.capture)
        self.canvas.image = self.capture
        
    def blurGripperImage(self):
        Vision.resizeImage(My_Path+"/GripperBlur.png", 100)
        self.capture = tk.PhotoImage(file=(My_Path+"/GripperBlur.png"))
        self.canvas.create_image(50,50,image=self.capture)
        self.canvas.image = self.capture

class UltrasonicSensor:
    # Ultrasonic sensor
    def __init__(self, frame, frame_photo):
        self.frame_photo = frame_photo
        self.frame = frame
        self.active = False
        self.text_ultrasonic_sensor = tk.Label(frame, text="Distance: ")
        self.text_ultrasonic_sensor.grid(column=0, row =0)
        self.distance_untrasonic_sensor = tk.Label(frame)
        self.distance_untrasonic_sensor.grid(column=1, row =0)
        self.frame.after(500, self.updateUltrasonicSensor)
        self.distance_untrasonic_sensor.configure(text="--")
        
        #Init ultrasonic sensor image
        self.canvas = tk.Canvas(self.frame_photo, width=100, height=100, state=tk.DISABLED)
        self.canvas.pack(fill="both", expand=True)
        self.blurUltrasonicSensorImage()

    def updateUltrasonicSensor(self):
        if self.active == True:            
            self.distance_untrasonic_sensor.configure(text=40)
            self.frame.after(500, lambda: self.updateUltrasonicSensor())
            self.clearUltrasonicSensorImage()
        else:
            self.distance_untrasonic_sensor.configure(text="--")
            self.blurUltrasonicSensorImage()

    def clearUltrasonicSensorImage(self):
        Vision.resizeImage(My_Path+"/UltrasonicSensorClear.png", 100)
        self.capture = tk.PhotoImage(file=(My_Path+"/UltrasonicSensorClear.png"))
        self.canvas.create_image(50,50,image=self.capture)
        self.canvas.image = self.capture
        
    def blurUltrasonicSensorImage(self):
        Vision.resizeImage(My_Path+"/UltrasonicSensorBlur.png", 100)
        self.capture = tk.PhotoImage(file=(My_Path+"/UltrasonicSensorBlur.png"))
        self.canvas.create_image(50,50,image=self.capture)
        self.canvas.image = self.capture
        
class ECSensor:
    # Ultrasonic sensor
    def __init__(self, frame, frame_photo):
        self.frame_photo = frame_photo
        self.frame = frame
        self.active = False
        self.text_EC_EC_sensor = tk.Label(frame, text="EC (S/cm): ")
        self.text_EC_EC_sensor.grid(column=0, row =0)
        self.EC_EC_sensor = tk.Label(frame)
        self.EC_EC_sensor.grid(column=1, row =0)
        self.frame.after(500, self.updateECSensor)
        self.EC_EC_sensor.configure(text="--")
        
        #Init EC sensor image
        self.canvas = tk.Canvas(self.frame_photo, width=100, height=100, state=tk.DISABLED)
        self.canvas.pack(fill="both", expand=True)
        self.blurECSensorImage()

    def updateECSensor(self):
        if self.active == True:            
            self.EC_EC_sensor.configure(text=40)
            self.frame.after(500, lambda: self.updateECSensor())
            self.clearECSensorImage()
        else:
            self.EC_EC_sensor.configure(text="--")
            self.blurECSensorImage()
        
    def clearECSensorImage(self):
        Vision.resizeImage(My_Path+"/ECSensorClear.png", 100)
        self.capture = tk.PhotoImage(file=(My_Path+"/ECSensorClear.png"))
        self.canvas.create_image(50,50,image=self.capture)
        self.canvas.image = self.capture
        
    def blurECSensorImage(self):
        Vision.resizeImage(My_Path+"/ECSensorBlur.png", 100)
        self.capture = tk.PhotoImage(file=(My_Path+"/ECSensorBlur.png"))
        self.canvas.create_image(50,50,image=self.capture)
        self.canvas.image = self.capture
        
class TemperatureSensor:
    # Ultrasonic sensor
    def __init__(self, frame, frame_photo):
        self.frame_photo = frame_photo
        self.frame = frame
        self.active = False
        self.text_temperature_sensor= tk.Label(frame, text="Temperature (°C): ")
        self.text_temperature_sensor.grid(column=0, row =0)
        self.temp_temperature_sensor = tk.Label(frame)
        self.temp_temperature_sensor.grid(column=1, row =0)
        self.frame.after(500, self.updateTemperatureSensor)
        self.temp_temperature_sensor.configure(text="--")

    def updateTemperatureSensor(self): 
        if self.active == True:            
            self.temp_temperature_sensor.configure(text=40)
            self.frame.after(500, lambda: self.updateTemperatureSensor())
        else:
            self.temp_temperature_sensor.configure(text="--")
        
class PhSensor:
    # Ultrasonic sensor
    def __init__(self, frame, frame_photo):
        self.frame_photo = frame_photo
        self.frame = frame
        self.active = False
        self.text_Ph_sensor = tk.Label(frame, text="Ph: ")
        self.text_Ph_sensor.grid(column=0, row =0)
        self.Ph_Ph_sensor = tk.Label(frame)
        self.Ph_Ph_sensor.grid(column=1, row =0)
        self.frame.after(500, self.updatePhSensor)
        self.Ph_Ph_sensor.configure(text="--")
        
        #Init EC sensor image
        self.canvas = tk.Canvas(self.frame_photo, width=100, height=100, state=tk.DISABLED)
        self.canvas.pack(fill="both", expand=True)
        self.blurPhSensorImage()

    def updatePhSensor(self):
        if self.active == True:            
            self.Ph_Ph_sensor.configure(text=40)
            self.frame.after(500, lambda: self.updatePhSensor())
            self.clearPhSensorImage()
        else:
            self.Ph_Ph_sensor.configure(text="--")
            self.blurPhSensorImage()
        
    def clearPhSensorImage(self):
        Vision.resizeImage(My_Path+"/PhSensorClear.png", 100)
        self.capture = tk.PhotoImage(file=(My_Path+"/PhSensorClear.png"))
        self.canvas.create_image(50,50,image=self.capture)
        self.canvas.image = self.capture
        
    def blurPhSensorImage(self):
        Vision.resizeImage(My_Path+"/PhSensorBlur.png", 100)
        self.capture = tk.PhotoImage(file=(My_Path+"/PhSensorBlur.png"))
        self.canvas.create_image(50,50,image=self.capture)
        self.canvas.image = self.capture

class MainApplication:
    def __init__(self, master):
        # Window init
        master.title("AeroponicBot GUI")
        master.geometry('600x650')

        # Frames
        #Current position
        frame_current_position = tk.LabelFrame(master, text="Current robot position")
        frame_current_position.grid(column=0, row=0, padx=5, pady=5)
        #Camera
        frame_capture = tk.LabelFrame(master, text="Camera")
        frame_capture.grid(column=0, row=1, padx=2, pady=5)
        #Tool changer
        frame_current_tool = tk.LabelFrame(master, text="Tool changer")
        frame_current_tool.grid(column=0, row=2, padx=5, pady=0)
        #Gripper
        frame_gripper = tk.LabelFrame(frame_current_tool, text="Gripper")
        frame_gripper.grid(column=0, row=3, padx=5, pady=2)
        frame_photo_gripper = tk.Frame(frame_current_tool)
        frame_photo_gripper.grid(column=1, row=3, padx=2, pady=2)
        #Ultrasonic sensor
        frame_ultrasonic_sensor = tk.LabelFrame(frame_current_tool, text="Ultrasonic sensor")
        frame_ultrasonic_sensor.grid(column=0, row=4, padx=2, pady=2)
        frame_photo_ultrasonic = tk.Frame(frame_current_tool)
        frame_photo_ultrasonic.grid(column=1, row=4, padx=2, pady=2)        
        #EC and temperature sensor
        frame_EC_Temp_sensor = tk.LabelFrame(frame_current_tool, text="EC and temperature sensor")
        frame_EC_Temp_sensor.grid(column=0, row=5, padx=2, pady=2)
        #EC sensor
        frame_EC_sensor = tk.Frame(frame_EC_Temp_sensor)
        frame_EC_sensor.grid(column=0, row=0, padx=2, pady=2)
        #Temperature sensor
        frame_temperature_sensor = tk.Frame(frame_EC_Temp_sensor)
        frame_temperature_sensor.grid(column=0, row=1, padx=2, pady=2)
        #Photo EC and temperature sensor
        frame_photo_EC_temp = tk.Frame(frame_current_tool)
        frame_photo_EC_temp.grid(column=1, row=5, padx=2, pady=2)
        #Ph sensor
        frame_Ph_sensor = tk.LabelFrame(frame_current_tool, text="Ph sensor")
        frame_Ph_sensor.grid(column=0, row=6, padx=2, pady=2)
        frame_photo_Ph = tk.Frame(frame_current_tool)
        frame_photo_Ph.grid(column=1, row=6, padx=2, pady=2)
        
        
        # Setup Widgets
        self.current_position = CurrentPosition(frame_current_position)
        self.capture = Capture(frame_capture)
        self.gripper = Gripper(frame_gripper, frame_photo_gripper)
        self.ultrasonic_sensor = UltrasonicSensor(frame_ultrasonic_sensor, frame_photo_ultrasonic)
        self.ec_sensor = ECSensor(frame_EC_sensor, frame_photo_EC_temp)
        self.temperature_sensor = TemperatureSensor(frame_temperature_sensor, frame_photo_EC_temp)
        self.ph_sensor = PhSensor(frame_Ph_sensor, frame_photo_Ph)
        self.current_tool = CurrentTool(frame_current_tool, self.gripper, self.ultrasonic_sensor, self.ec_sensor, self.temperature_sensor, self.ph_sensor)
        


#start user interface loop
if __name__ == "__main__":
    #Init comm arduino
    #arduino_ports = setUpArduino()
    #init serial comm between arduino and raspberry pi
    #if arduino_ports != False:
    #    ser = serial.Serial(arduino_ports[0], 9600, 8, 'N', 1, timeout=1)
    
    #Inint tool changer
    #Tool = ToolChanger.Tool("None")
    #Tool.setCurrentTool("Gripper")
    #Init Garden
    G = AeroGarden.Garden()
    #setUpGarden(G)
    #G.updatePlantsArea()
    #G.displayGardenMapAreas()
    
    master = tk.Tk()
    main_window = MainApplication(master)
    while True:
        try:
            master.mainloop()
            break
        except UnicodeDecodeError:
            pass  


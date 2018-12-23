"""

    Autor: Hugo Daniel
    Project name: AreoponicBot U.N.
    Date: September 2018
    Location: Universidad National de Colombia sede Medellin
    File name: GUI.py

    Description: Tool changer control algorythmes
    
    
"""


# Libraries
import tkinter as tk
import tkinter.ttk as ttk
import cv2
import AeroGarden
import Vision
import ToolChanger
import warnings
import serial
import serial.tools.list_ports

# Global def
global Tresh_Area
global Dist_Tresh
global My_path

Tresh_Area = 100
Dist_Tresh = 150
# My_Path is used to point to the image directory.
My_Path = "/home/pi/Documents/GitRepo/Image" # For the Raspberry pi
#My_Path = "/Users/hugodaniel/Desktop/StageMedellin/GitRepo/Image" # For my computer

class RobotControl:
    #Robot control function
    def __init__(self, ser):
        self.axis = 1
        self.steps_to_perform = 0
        self.direction = 0
        self.enable = 0
        self.ser = ser
        self.serial_data = ""
    
    def waitForArduinoReady(self):
        self.serial_data = ""
        while self.serial_data != "Ready for new command":
            self.serial_data = self.ser.readline().decode()

    def sendCommandArduino(self):
        print("axis ", int(self.axis))
        print("steps ", self.steps_to_perform)
        print("direction ", int(self.direction))
        print("enable ", self.enable)
        self.ser.write((str(self.axis)).encode())
        self.ser.write('\n'.encode())
        self.ser.write(self.steps_to_perform.encode())
        self.ser.write('\n'.encode())
        self.ser.write((str(self.direction)).encode())
        self.ser.write('\n'.encode())
        self.ser.write((str(self.enable)).encode())
        self.ser.write('\n'.encode())


class CurrentPosition:
    # Current position
    def __init__(self, ser, frame, RobotControl, master):   
        self.robot_status = tk.Label(frame, text="Robot status")
        self.robot_status.grid(column=0, row=0)
        self.text_CNC_current_enter_position = tk.Label(frame, text="Enter command")
        self.text_CNC_current_enter_position.grid(column=2, row=1, padx=2)
        self.text_CNC_current_position = tk.Label(frame, text="Last command")
        self.text_CNC_current_position.grid(column=3, row=1)

        self.robot_status_flag = tk.Label(frame, text="Ready")
        self.robot_status_flag.grid(column=2, row=0)
        self.CNC_current_position_X = tk.Label(frame, text="0")
        self.CNC_current_position_X.grid(column=3, row=2)
        self.CNC_current_position_Y = tk.Label(frame, text="0")
        self.CNC_current_position_Y.grid(column=3, row=3)
        self.CNC_current_position_Z = tk.Label(frame, text="0")
        self.CNC_current_position_Z.grid(column=3, row=4)

        self.text_CNC_X = tk.Label(frame, text="X axis")
        self.text_CNC_X.grid(column=0, row=2)
        self.text_CNC_Y = tk.Label(frame, text="Y axis")
        self.text_CNC_Y.grid(column=0, row=3)
        self.text_CNC_Z = tk.Label(frame, text="Z axis")
        self.text_CNC_Z.grid(column=0, row=4)

        self.input_CNC_X = tk.Entry(frame,width=10)
        self.input_CNC_X.grid(column=2, row=2)
        self.input_CNC_X.bind('<Return>',self.updateXCNCPosition)
        self.input_CNC_Y = tk.Entry(frame,width=10)
        self.input_CNC_Y.grid(column=2, row=3)
        self.input_CNC_Y.bind('<Return>',self.updateYCNCPosition)
        self.input_CNC_Z = tk.Entry(frame,width=10)
        self.input_CNC_Z.grid(column=2, row=4)
        self.input_CNC_Z.bind('<Return>',self.updateZCNCPosition)

        self.RobotControl = RobotControl
        self.RobotControl.waitForArduinoReady()

        self.master = master
 
        
    def updateXCNCPosition(self, event):
        steps_to_perform = self.input_CNC_X.get() 
        self.robot_status_flag.configure(text="Moving... Whait for motor to stop", foreground="red")

        if int(steps_to_perform) < 0:
            steps_to_perform = str(abs(int(steps_to_perform)))
            self.RobotControl.steps_to_perform = steps_to_perform
            self.RobotControl.direction = 0
        else:
            self.RobotControl.direction = 1
            self.RobotControl.steps_to_perform = steps_to_perform

        self.RobotControl.axis = 0    
        self.RobotControl.enable = 0
        self.master.after(100, self.updateXCNCPositionCallBack)

    def updateYCNCPosition(self, event):
        steps_to_perform = self.input_CNC_Y.get() 
        self.robot_status_flag.configure(text="Moving... Whait for motor to stop", foreground="red")

        if int(steps_to_perform) < 0:
            steps_to_perform = str(abs(int(steps_to_perform)))
            self.RobotControl.steps_to_perform = steps_to_perform
            self.RobotControl.direction = 0
        else:
            self.RobotControl.direction = 1
            self.RobotControl.steps_to_perform = steps_to_perform

        self.RobotControl.axis = 1    
        self.RobotControl.steps_to_perform = steps_to_perform
        self.RobotControl.enable = 0
        self.master.after(100, self.updateYCNCPositionCallBack)

    def updateZCNCPosition(self, event):
        steps_to_perform = self.input_CNC_Z.get() 
        self.robot_status_flag.configure(text="Moving... Whait for motor to stop", foreground="red")

        if int(steps_to_perform) < 0:
            steps_to_perform = str(abs(int(steps_to_perform)))
            self.RobotControl.steps_to_perform = steps_to_perform
            self.RobotControl.direction = 0
        else:
            self.RobotControl.direction = 1
            self.RobotControl.steps_to_perform = steps_to_perform

        self.RobotControl.axis = 2    
        self.RobotControl.steps_to_perform = steps_to_perform
        self.RobotControl.enable = 0
        self.master.after(100, self.updateZCNCPositionCallBack)

    def updateXCNCPositionCallBack(self):
        self.RobotControl.sendCommandArduino()
        self.RobotControl.waitForArduinoReady()
        self.robot_status_flag.configure(text="Ready")
        if self.RobotControl.direction == 0:
            self.CNC_current_position_X.configure(text=("-", self.RobotControl.steps_to_perform))
        else:
            self.CNC_current_position_X.configure(text=self.RobotControl.steps_to_perform)
        self.input_CNC_X.delete(0, 'end')

    def updateYCNCPositionCallBack(self):
        self.RobotControl.sendCommandArduino()
        self.RobotControl.waitForArduinoReady()
        self.robot_status_flag.configure(text="Ready")
        if self.RobotControl.direction == 0:
            self.CNC_current_position_Y.configure(text=("-", self.RobotControl.steps_to_perform))
        else:
            self.CNC_current_position_Y.configure(text=self.RobotControl.steps_to_perform)
        self.input_CNC_Y.delete(0, 'end')

    def updateZCNCPositionCallBack(self):
        self.RobotControl.sendCommandArduino()
        self.RobotControl.waitForArduinoReady()
        self.robot_status_flag.configure(text="Ready")
        if self.RobotControl.direction == 0:
            self.CNC_current_position_Z.configure(text=("-", self.RobotControl.steps_to_perform))
        else:
            self.CNC_current_position_Z.configure(text=self.RobotControl.steps_to_perform)
        self.input_CNC_Z.delete(0, 'end')
        
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
        #!!!Need to add code to save the area!!!
        Vision.analysePlantArea(My_Path, Tresh_Area)

        self.top = tk.Toplevel()
        self.top.title("Analyse capture")
        self.canvas = tk.Canvas(self.top, width=1000, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.capture = tk.PhotoImage(file=(My_Path+"/imageTest.png"))
        self.canvas.create_image(500,300,image=self.capture)
        self.canvas.image = self.capture

class CurrentTool:
    # Current tool: This class controls the current tool on the GUI
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
        # Update ToolChanger
        """
        The goal of this function is to update the current tool.
        When a tool is selected, the updateTool function will disable every 
        other tools and only enable the tool taht is selected in the GUI
        via the selected_tool var.
        
        If a tool is disable, his picture will be blured and his text = to "--".
        This is done by setting the active attribute of the tool to "False" and 
        by callint the update function of the tool
        """
        
        Tool.setCurrentTool("None")
        
        # Get setected_tool var
        self.selected_tool = self.combo.get()
        
        # Disable all tools
        self.gripper.active = False
        self.gripper.updateGripper()
        self.ultrasonic_sensor.active = False
        self.ultrasonic_sensor.updateUltrasonicSensor()
        self.ec_sensor.active = False
        self.ec_sensor.updateECSensor()
        self.temperature_sensor.active = False
        self.temperature_sensor.updateTemperatureSensor()
        self.ph_sensor.active = False
        self.ph_sensor.updatePhSensor() 
        
        # Enable the selected tool
        if self.selected_tool == "Gripper":
            Tool.setCurrentTool("Gripper")
            self.gripper.active = True
            self.gripper.updateGripper()            
        elif self.selected_tool == "Ultrasonic sensor":
            Tool.setCurrentTool("Ultrasonic sensor")
            self.ultrasonic_sensor.active = True
            self.ultrasonic_sensor.updateUltrasonicSensor()
            #self.ultrasonic_sensor.distance_untrasonic_sensor.grid()
        elif self.selected_tool == "EC and temperature sensor":
            Tool.setCurrentTool("ECTempSensor")
            
            self.ec_sensor.active = True
            self.ec_sensor.updateECSensor()
            self.temperature_sensor.active = True
            self.temperature_sensor.updateTemperatureSensor()
        elif self.selected_tool == "Ph sensor":
            Tool.setCurrentTool("PhSensor")
            
            self.ph_sensor.active = True
            self.ph_sensor.updatePhSensor() 
    
class Gripper:
    # Gripper
    def __init__(self, frame, frame_photo):
        self.frame_photo = frame_photo
        self.active = False
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
        
    def updateGripper(self):
        if self.active == True:            
            self.gripper_state.configure(text="Open")
            self.openGripperImage()
            self.button_gripper_open.configure(state=tk.NORMAL)
            self.button_gripper_close.configure(state=tk.NORMAL)
        else:
            self.button_gripper_open.configure(state=tk.DISABLED)
            self.button_gripper_close.configure(state=tk.DISABLED)
            self.gripper_state.configure(text="--")
            self.blurGripperImage()

    def openGripper(self):
        Tool.current_tool.setGripperPosition(1900)
        
        self.gripper_state.configure(text="Open")
        self.openGripperImage()
        
    def closeGripper(self):
        Tool.current_tool.setGripperPosition(1400)
        
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
    def __init__(self, ser, master, RobotControl):
        # Window init
        self.master = master
        self.ser = ser
        self.RobotControl = RobotControl
        
        self.master.title("AeroponicBot GUI")
        self.master.geometry('600x650')

        # Setting the position and the form of the frames
        # Current position
        self.frame_current_position = tk.LabelFrame(self.master, text="Current robot position")
        self.frame_current_position.grid(column=0, row=0, padx=5, pady=5)
        # Camera
        self.frame_capture = tk.LabelFrame(self.master, text="Camera")
        self.frame_capture.grid(column=0, row=1, padx=2, pady=5)
        # Tool changer
        self.frame_current_tool = tk.LabelFrame(self.master, text="Tool changer")
        self.frame_current_tool.grid(column=0, row=2, padx=5, pady=0)
        # Gripper
        self.frame_gripper = tk.LabelFrame(self.frame_current_tool, text="Gripper")
        self.frame_gripper.grid(column=0, row=3, padx=5, pady=2)
        self.frame_photo_gripper = tk.Frame(self.frame_current_tool)
        self.frame_photo_gripper.grid(column=1, row=3, padx=2, pady=2)
        # Ultrasonic sensor
        self.frame_ultrasonic_sensor = tk.LabelFrame(self.frame_current_tool, text="Ultrasonic sensor")
        self.frame_ultrasonic_sensor.grid(column=0, row=4, padx=2, pady=2)
        self.frame_photo_ultrasonic = tk.Frame(self.frame_current_tool)
        self.frame_photo_ultrasonic.grid(column=1, row=4, padx=2, pady=2)        
        # EC and temperature sensor
        self.frame_EC_Temp_sensor = tk.LabelFrame(self.frame_current_tool, text="EC and temperature sensor")
        self.frame_EC_Temp_sensor.grid(column=0, row=5, padx=2, pady=2)
        # EC sensor
        self.frame_EC_sensor = tk.Frame(self.frame_EC_Temp_sensor)
        self.frame_EC_sensor.grid(column=0, row=0, padx=2, pady=2)
        # Temperature sensor
        self.frame_temperature_sensor = tk.Frame(self.frame_EC_Temp_sensor)
        self.frame_temperature_sensor.grid(column=0, row=1, padx=2, pady=2)
        # Photo EC and temperature sensor
        self.frame_photo_EC_temp = tk.Frame(self.frame_current_tool)
        self.frame_photo_EC_temp.grid(column=1, row=5, padx=2, pady=2)
        # Ph sensor
        self.frame_Ph_sensor = tk.LabelFrame(self.frame_current_tool, text="Ph sensor")
        self.frame_Ph_sensor.grid(column=0, row=6, padx=2, pady=2)
        self.frame_photo_Ph = tk.Frame(self.frame_current_tool)
        self.frame_photo_Ph.grid(column=1, row=6, padx=2, pady=2)

        
        # Setup Widgets
        self.current_position = CurrentPosition(self.ser, self.frame_current_position, self.RobotControl, self.master)
        self.capture = Capture(self.frame_capture)
        self.gripper = Gripper(self.frame_gripper, self.frame_photo_gripper)
        self.ultrasonic_sensor = UltrasonicSensor(self.frame_ultrasonic_sensor, self.frame_photo_ultrasonic)
        self.ec_sensor = ECSensor(self.frame_EC_sensor, self.frame_photo_EC_temp)
        self.temperature_sensor = TemperatureSensor(self.frame_temperature_sensor, self.frame_photo_EC_temp)
        self.ph_sensor = PhSensor(self.frame_Ph_sensor, self.frame_photo_Ph)
        self.current_tool = CurrentTool(self.frame_current_tool, self.gripper, self.ultrasonic_sensor, self.ec_sensor, self.temperature_sensor, self.ph_sensor)


# Function that connect the Pi to an Arduino
def setUpArduino():
    arduino_ports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if ('ACM' or "Arduino") in p.description
    ]
    if not arduino_ports:
        raise IOError("No Arduino found")
    if len(arduino_ports) > 1:
        warnings.warn('Multiple Arduinos found - using the first')

    return arduino_ports

#start user interface loop
if __name__ == "__main__":
    # Init comm arduino
    arduino_ports = setUpArduino()
    
    # Init serial comm between arduino and raspberry pi
    if arduino_ports != False:
        ser = serial.Serial(arduino_ports[0], 9600, 8, 'N', 1, timeout=1)
    
    # Inint tool changer
    Tool = ToolChanger.Tool("None")
    
    # Init Garden
    G = AeroGarden.Garden()
    #setUpGarden(G)
    #G.updatePlantsArea()
    #G.displayGardenMapAreas()

    Robot = RobotControl(ser)
    
    master = tk.Tk()
    main_window = MainApplication(ser, master, Robot)

    while True:       
        try:
            master.mainloop()
            break
        except UnicodeDecodeError:
            pass 

        
    # Clean GPIO
    Tool.cleanToolChanger()


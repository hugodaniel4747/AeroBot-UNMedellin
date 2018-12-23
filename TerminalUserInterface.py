"""

    Autor: Hugo Daniel
    Project name: AreoponicBot U.N.
    Date: September 2018
    Location: Universidad National de Colombia sede Medellin
    File name: TerminalUserInterface.py

    Description: User interface accesible from terminal
    
    
"""

"""
!!!!!!!!!!!!!!!
UNCOMMENT ALL ToolChanget AND Tool INSTANCES BEFORE USING ON A RESPBERRY PI
COMMENT WHEN BUILDING FROM A COMPUTER
!!!!!!!!!!!!!!!
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
        if ('ACM' or "Arduino") in p.description 
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
    print("Terminal user interface program starts")
    
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
    
    tool = "None"
    serial_data = ""
    try:
        while True:
            while serial_data != "Ready for new command":
                serial_data = ser.readline().decode()
                print("Waining for arduino...")
            command = input('Enter command: ')
            
            if command == "help":
                print("Try:")
                print("analog")
                print("robot position")
                print("robot position -> exit")
                print("capture")
                print("analyse capture")
                print("tool")
                print("tool -> current tool")
                print("tool -> open (gripper tool)")
                print("tool -> close (gripper tool)")
                print("tool -> go to (gripper tool)")
                print("tool -> get (ultrasonic sensor tool)")
                print("tool -> get (ec and temp tool)")
                print("tool -> get (ph sensor tool)")
                print("tool -> exit")
                print("change tool")
                print()
                
            elif command == "analog":
                #print("Analog value: " + Tool.getAnalogInput())
                print()
                
            elif command == "robot position":
                while True:
                    if serial_data == "Ready for new command":
                        serial_data = ""
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

                        #Wait to receive confirmation before continuing
                        while serial_data != "Ready for new command":
                            serial_data = ser.readline().decode()
                            print("Waining for arduino...")
                        
                        second_command = input('Enter "exit" to quit: ')
                        if second_command == "exit":
                            break
                            
            elif command == "capture":
                Vision.storeCapture(My_Path+"/imageTest.png")
                Vision.resizeImage(My_Path+"/imageTest.png", 1000)
            elif command == "analyse capture": 
                #Plants detection 
                #!!!Need to add code to save the area!!!
                Vision.analysePlantArea(My_Path, Tresh_Area)
                
            elif command == "tool":
                while True:
                    second_command = input('Enter a tool command: ')                    
                    if tool == "gripper":
                        if second_command == "open":
                            #Tool.current_tool.setGripperPosition(1900)
                            print("not activated")
                        elif second_command == "close":
                            #Tool.current_tool.setGripperPosition(1400)
                            print("not activated")
                        elif second_command == "go to":
                            position = input('Enter a position: ')
                            print("not activated")
                            #Tool.current_tool.setGripperPosition(position)
                            print("not activated")
                    elif tool == "ultrasonic sensor":
                        if second_command == "get":
                            print("Code not implemented")
                    elif tool == "ec and temp sensor":
                        if second_command == "get":
                            print("Code not implemented")
                    elif tool == "ph sensor":
                        if second_command == "get":
                            print("Code not implemented")
                    elif second_command == "exit":
                        break
                    if second_command == "current tool":
                        print(tool)
                    else:
                        print("not a valid command")                                                
                        
            elif command == "change tool":
                tool = input('Enter a new tool: ')
                #Tool.setCurrentTool(tool)  
                print("New tool: " + tool + " set")
                
            else:
                print("not a valid command")
                
    except (KeyboardInterrupt):
        #Tool.cleanToolChanger()
        print('\n', "Exit on Ctrl-C")
        
    except:
        print("Other error or exception occurred!")
        raise
    
    finally:
        print
    
    #Tool.cleanToolChanger()
    
if __name__=="__main__":
    main()
    






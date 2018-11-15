"""

    Editor: Hugo Daniel
    Project name: AreoponicBot U.N.
    Date: September 2018
    Location: Universidad National de Colombia sede Medellin
    File name: main.py
    Python Version: 2 -> might have problems with opencv in python 3

    Description: main()
    
    
"""
# Library
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
        if 'ACM' in p.description or "Arduino" in p.description 
    ]
    if not arduino_ports:
        #raise IOError("No Arduino found")
        return False
    if len(arduino_ports) > 1:
        warnings.warn('Multiple Arduinos found - using the first')
    
    return arduino_ports

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
    
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

    #Init Tool Changer
    #Tool = ToolChanger.Tool("Gripper")
    
    G = AeroGarden.Garden()
    #setUpGarden(G)
    #G.updatePlantsArea()
    #G.displayGardenMapAreas()
    
    #arduino_ports = setUpArduino()
    #init serial comm between arduino and raspberry pi
    #if arduino_ports != False:
    #    ser = serial.Serial(arduino_ports[0], 9600, 8, 'N', 1, timeout=1)
    
    #Interact with arduino
    tool = "None"
    try:
        while True:
            command = input('Enter command: ')
            
            if command == "help":
                print("Tap:")
                print("Analog")
                print("Robot position")
                print("Robot position -> exit")
                print("Capture")
                print("Analyse capture")
                print("tool")
                print("tool -> Current tool")
                print("tool -> open (Gripper tool)")
                print("tool -> close (Gripper tool)")
                print("tool -> go to (Gripper tool)")
                print("tool -> get (Ultrasonic sensor tool)")
                print("tool -> get (EC and temp tool)")
                print("tool -> get (Ph sensor tool)")
                print("tool -> exit")
                print("Change tool")
                print()
                
            elif command == "Analog":
                #print("Analog value: " + Tool.getAnalogInput())
                print()
                
            elif command == "Robot position":
                while True:
                    second_command = input('Enter a command or position: ')
                    if second_command == "exit":
                        break
                    elif isInt(second_command):
                        print("Code not implemented")
                    else:
                        print("not a valid command")
            elif command == "Capture":
                Vision.storeCapture(My_Path+"/imageTest.png")
                Vision.resizeImage(My_Path+"/imageTest.png", 1000)
            elif command == "Analyse capture": 
                #Plants detection
                Vision.storeCapture(My_Path+"/imageTest.png")
                img = Vision.getImageFromComputer(My_Path+"/imageTest.png")
                contours = Vision.pipelineGetContours(img)
                listOfAreas = Vision.drawAreasBoundingBox(img, contours, Tresh_Area)
                listCenterAreas = Vision.findCenterPlant(img, listOfAreas, 200)        
                cv2.imwrite(My_Path+"/imageTest.png", img)
                
            elif command == "tool":
                while True:
                    second_command = input('Enter a tool command: ')                    
                    if tool == "Gripper":
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
                    elif tool == "Ultrasonic sensor":
                        if second_command == "get":
                            print("Code not implemented")
                    elif tool == "EC and temp sensor":
                        if second_command == "get":
                            print("Code not implemented")
                    elif tool == "PH sensor":
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
    
if __name__=="__main__":
    main()
    






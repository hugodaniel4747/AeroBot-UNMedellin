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



def main():   
    print("main: ")
    
    # Global def
    #Image_Directory = "/Users/hugodaniel/MATLAB-Drive/Medellin/Images/bebeplantes.jpg"
    
    G = AeroGarden.Garden()
    #setUpGarden(G)
    #G.updatePlantsArea()
    #G.displayGardenMapAreas()
    
    arduino_ports = setUpArduino()
    #init serial comm between arduino and raspberry pi
    ser = serial.Serial(arduino_ports[0], 9600, 8, 'N', 1, timeout=1)
    
    #Interact with arduino
    output = " "
    while True:
        print("----" )
        output = ser.readline()
        while output != "":
            print(output)
            if output == "Enter new destination\n":
                destination = raw_input('New destination: ')
                ser.write(destination + '\r\n')
                sleep(4)
                
                #Vision
                #img = Vision.getCapture()
                #img = Vision.getImageFromComputer("/Users/hugodaniel/Desktop/StageMedellin/Working_Images/bebePlantesCentre.jpg")
                img = Vision.getImageFromComputer("/home/pi/Desktop/imageTest.jpg")
                contours = Vision.pipelineGetContours(img)
                listOfAreas = Vision.drawAreasBoundingBox(img, contours, Tresh_Area)
                listCenterAreas = Vision.findCenterPlant(img, listOfAreas, 200)
                cv2.namedWindow("image")
                cv2.imshow("image",img)
                cv2.waitKey(0)
                
            output = ""
    
    """
    #Plants detection
    #Vision.storeCapture("imageTest.jpg", "/Users/hugodaniel/Desktop", 0)
    img = Vision.getImageFromComputer("/Users/hugodaniel/Desktop/StageMedellin/Working_Images/bebePlantesCentre.jpg")
    #img = Vision.getCapture()
    contours = Vision.pipelineGetContours(img)
    listOfAreas = Vision.drawAreasBoundingBox(img, contours, Tresh_Area)
    #listOfAreasInsideTresh = Vision.analyseAreasProximity(listOfAreas, Dist_Tresh)
    #listAreaGroup = Vision.findDuplicatesAreas(listOfAreasInsideTresh)
    #Vision.drawListOfAreas(img, listAreaGroup)
    
    listCenterAreas = Vision.findCenterPlant(img, listOfAreas, 200)
    print(Vision.getTotalArea(listCenterAreas))
    
    cv2.namedWindow("image")
    cv2.imshow("image",img)

    cv2.waitKey(0)
    """
    
    
if __name__=="__main__":
    main()
    
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




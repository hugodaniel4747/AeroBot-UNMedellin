"""

    Editor: Hugo Daniel
    Project name: AreoBot U.N.
    Date: September 2018
    Location: Universidad National de Colombia sede Medellin

    Description: main()
    
    
"""
# Library
import cv2
import AeroGarden
import Vision



def main():   
    print("main: ")
    
    # Global def
    Tresh_Area = 0
    Dist_Tresh = 150
    Image_Directory = "/Users/hugodaniel/MATLAB-Drive/Medellin/Images/bebeplantes.jpg"
    
    #Garden initialisation
    G = AeroGarden.Garden()
    G.addRow()
    G.addBed(0)
    
    G.addPlantMapGarden(0,0,0,0,AeroGarden.DictOfPlantes.myList[1])
    G.addSetOfPlants(AeroGarden.DictOfPlantes.myList[2],3)
    G.displayGardenMapAreas()
    G.updatePlantsArea()
    G.displayGardenMapAreas()
    
    
    #Plants detection
    img = Vision.getImage(Image_Directory)
    contours = Vision.pipelineGetContours(img)
    listOfAreas = Vision.drawAreasBoundingBox(img, contours, Tresh_Area)
    listOfAreasInsideTresh = Vision.analyseAreasProximity(listOfAreas, Dist_Tresh)
    listAreaGroup = Vision.findDuplicatesAreas(listOfAreasInsideTresh)
    Vision.drawAreas(img, listAreaGroup)
    
    cv2.namedWindow("image")
    cv2.imshow("image",img)

    cv2.waitKey(0)

    
    
if __name__=="__main__":
    main()
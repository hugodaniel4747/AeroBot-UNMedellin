"""

    Editor: Hugo Daniel
    Project name: AreoponicBot U.N.
    Date: September 2018
    Location: Universidad National de Colombia sede Medellin
    File name: main.py

    Description: main()
    
    
"""
# Library
import cv2
import AeroGarden
import Vision



def main():   
    print("main: ")
    
    # Global def
    #Image_Directory = "/Users/hugodaniel/MATLAB-Drive/Medellin/Images/bebeplantes.jpg"
    
    #Garden initialisation
    G = AeroGarden.Garden()
    G.addRow()
    G.addBed(0, AeroGarden.IcorporTEST())
    
    G.displayGardenMap()
    G.addPlantMapGarden(0,0,0,0,AeroGarden.DictOfPlantes.myPlants[1])
    G.displayGardenMap()
    G.addSetOfPlantsMap(AeroGarden.DictOfPlantes.myPlants[2],3)
    G.displayGardenMap()
    G.updatePlantsArea()
    G.displayGardenMapAreas()
    
    #G.updatePlantsArea()
    #G.displayGardenMapAreas()
    
    """
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
    """
    
    
if __name__=="__main__":
    main()
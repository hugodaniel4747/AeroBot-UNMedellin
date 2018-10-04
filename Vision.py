"""

    Editor: Hugo Daniel
    Project name: AreoponicBot U.N.
    Date: September 2018
    Location: Universidad National de Colombia sede Medellin
    File name: Vision.py

    Description: Vision algorythme to detect plants and deternimate proprieties
    
    
"""
# Library
import cv2
import numpy as np

# Global def
Tresh_Area = 100
Dist_Tresh = 150

def getImage(imageDirectory):
    """
        Arguments:  Image directory
        Return:     Image
    """  
    
    ### Load a color image
    img = cv2.imread(imageDirectory,-1)
    
    ### Resize image
    r = 1000.0 / img.shape[1]
    dim = (1000, int(img.shape[0] * r))    
    # perform the actual resizing of the image
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return img

def pipelineGetContours(colorImage):
    """
        Arguments:  Image in color
        Return:     Contours
        Strategie:  Use of a HSV mask
    """  
    
    ### Color to HSV
    imgHSV = cv2.cvtColor(colorImage, cv2.COLOR_BGR2HSV)
    
    # Define range of blue color in HSV
    lower_green = np.array([30,40,0])
    upper_green = np.array([125,255,250])
    
    ### Make binarised image
    maskHSV = cv2.inRange(imgHSV, lower_green, upper_green)
    
    ### Find contours
    _, contours, _ = cv2.findContours(maskHSV, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours
   

def drawAreasBoundingBox(image, contours, tresh_area):
    """
        Arguments:  Image to print the bounding boxes,
                    Contours of the areas
                    Treshold area to filter areas
        Return:     List of areas with proprieties
    """
    
    ### Draw Box contours
    listOfAreas = []
    for c in contours:    
        if cv2.contourArea(c) > tresh_area: # Treshold value to eliminate little areas
            # rectangle: get the bounding rect
            x, y, w, h = cv2.boundingRect(c)
            # draw a red rectangle to visualize the bounding rect
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 1)         
            """
            # Rectangle in angle
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            # convert all coordinates floating point values to int
            box = np.int0(box)
            # draw a red 'nghien' rectangle
            cv2.drawContours(image, [box], 0, (0, 0, 255))
            """
            # Print the center of the square on image
            # get the center of mass of the area
            M = cv2.moments(c)
            # calculate x,y coordinate of center
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(image, (cX, cY), 3, (0, 255, 0), -1)
            #cv2.circle(image, (np.uint8(np.ceil(x/kpCnt)), np.uint8(np.ceil(y/kpCnt))), 1, (0, 0, 255), 3)
            
            # save data
            listOfAreas.append([cv2.contourArea(c), cX, cY, x, y, x+w, y+h]) # list of areas with their center of mass
    return listOfAreas


def analyseAreasProximity(listOfAreas, dist_tresh):
    """
        Argument:   List of areas with centers of mass 
        Return:     List of areas with the center of mass within the treshold
                    distance for every areas
    """
    listOfAreasInsideTresh = []
    for area_a in listOfAreas:
        list1Area = []
        list1Area.append(area_a)
        for area_b in listOfAreas:
            dist = pow(pow(max(area_a[1],area_b[1])-min(area_a[1],area_b[1]),2) + pow(max(area_a[2],area_b[2])-min(area_a[2],area_b[2]),2),0.5)
            if dist < dist_tresh and area_b != area_a:
                list1Area.append(area_b)  
        listOfAreasInsideTresh.append(list1Area)
    return listOfAreasInsideTresh

def findDuplicatesAreas(listOfAreasInsideTresh): 
    """
        Argument:   List of areas inside treshold distance for every areas
        Return:     List of areas inside the same treshold distance
        Strategy:   Find identical areas and delete duplicates
    """
    listFinal = []
    for listArea_a in listOfAreasInsideTresh: 
        counter = 0
        listFinal.append(listArea_a)
        for listArea_b in listFinal:
            if listComp(listArea_a,listArea_b):
                counter = counter + 1
        if counter > 1:
            listFinal.remove(listArea_a)    
    return listFinal

def listComp(listOfArea1, listArea2):   
    """
        Arguments:  Fisrt list and second list to compare with first list
        Return:     Bool value
    """
    for area1 in listOfArea1:   
        flag = False
        for area2 in listArea2:
            if area1 == area2:
                flag = True                 
        if flag:
            continue
        else:
            return False
    return True 

def drawAreas(image, listOfAreas):
    """
        Arguments:  List of areas and the picture on witch you wanna print the
                    areas
        Fonction:   Draw visual landmarks for user on the picture
    """
    for listOfArea in listOfAreas:
        """
        #Print a circle around the area using the extremums center of mass of the areas
        xPt1 = max(listOfArea, key=lambda x: x[1])[1]
        yPt1 = max(listOfArea, key=lambda x: x[2])[2]
        xPt2 = min(listOfArea, key=lambda x: x[1])[1]
        yPt2 = min(listOfArea, key=lambda x: x[2])[2]
        rayon = pow(pow(max(xPt1,xPt2)-min(xPt1,xPt2),2) + pow(max(yPt1,yPt2)-min(yPt1,yPt2),2),0.5)
        cv2.circle(image, (int((max(xPt1,xPt2)-min(xPt1,xPt2))/2 + min(xPt1,xPt2)), int((max(yPt1,yPt2)-min(yPt1,yPt2))/2) + min(yPt1,yPt2)), int(rayon/2), (0, 255, 0), 1)
        totalArea = getTotalArea(listOfArea)
        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (int((max(xPt1,xPt2)-min(xPt1,xPt2))/2 + min(xPt1,xPt2)), int((max(yPt1,yPt2)-min(yPt1,yPt2))/2) + min(yPt1,yPt2))
        fontScale = 1
        fontColor = (0,255,0)
        lineType = 2
        cv2.putText(image,str(totalArea),bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
        """
        #Print a circle around the area using the extremums points of the bounding box
        xVer1 = max(max(listOfArea, key=lambda x: x[3])[3], max(listOfArea, key=lambda x: x[5])[5])
        yVer1 = max(max(listOfArea, key=lambda x: x[4])[4], max(listOfArea, key=lambda x: x[6])[6])
        xVer2 = min(min(listOfArea, key=lambda x: x[3])[3], min(listOfArea, key=lambda x: x[5])[5])
        yVer2 = min(min(listOfArea, key=lambda x: x[4])[4], min(listOfArea, key=lambda x: x[6])[6])
        rayon = pow(pow(max(xVer1,xVer2)-min(xVer1,xVer2),2) + pow(max(yVer1,yVer2)-min(yVer1,yVer2),2),0.5)/2
        circleXCentre = (max(xVer1,xVer2)-min(xVer1,xVer2))/2 + min(xVer1,xVer2)
        circleYCentre = (max(yVer1,yVer2)-min(yVer1,yVer2))/2 + min(yVer1,yVer2)
        cv2.circle(image, (int(circleXCentre), int(circleYCentre)), int(rayon), (0, 255, 0), 1)
        totalArea = getTotalArea(listOfArea)
        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomRightCornerOfText = (int((max(xVer1,xVer2)-min(xVer1,xVer2)) + min(xVer1,xVer2)), int((max(yVer1,yVer2)-min(yVer1,yVer2))) + min(yVer1,yVer2))
        fontScale = 1
        fontColor = (0,255,0)
        lineType = 1
        cv2.putText(image,str(totalArea),bottomRightCornerOfText, font, fontScale, fontColor, lineType)
        """
        #See the two choosen points
        cv2.circle(image, (xVer1, yVer1), 3, (0, 255, 0), -1)
        cv2.circle(image, (xVer2, yVer2), 3, (0, 255, 0), -1)
        """
        
def getTotalArea(listOfAreas):
    """
        Arguments:  Takes a list of areas
        Return:     Sum of all the areas inside the list
    """
    totalArea = 0
    for area in listOfAreas:
        totalArea = totalArea + area[0]
    return totalArea

def storeCapture(capture_name, directory=""):
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    cv2.imwrite(directory+capture_name, frame)
    
def getCapture():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    return frame
                        


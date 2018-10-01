"""

    Editor: Hugo Daniel
    Project name: AreoBot U.N.
    Date: September 2018
    Location: Universidad National de Colombia sede Medellin

    Description: Vision algorythme to detect plants and deternimate proprieties
    
    
"""
# Library
import cv2
import numpy as np
import copy


def imageContoursProp(imageDirectory, listOfAreas):
    # Global def
    TreshArea = 0
    
    ### Load an color image
    img = cv2.imread(imageDirectory,-1)
    
    
    ### Resize image
    r = 1000.0 / img.shape[1]
    dim = (1000, int(img.shape[0] * r))
     
    # perform the actual resizing of the image and show it
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    
    imgCopy = copy.deepcopy(img)
    
    
    ### Color to HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Define range of blue color in HSV
    lower_green = np.array([30,40,0])
    upper_green = np.array([125,255,250])
    
    ### Binarised image
    maskHSV = cv2.inRange(imgHSV, lower_green, upper_green)
    
    ### Find contours
    _, contours, hierarchy = cv2.findContours(maskHSV, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
     
    ### Draw Box contours
    listOfAreas
    for c in contours:    
        if cv2.contourArea(c) > TreshArea: # Treshold value to eliminate little areas
            # get the bounding rect
            x, y, w, h = cv2.boundingRect(c)
            # draw a green rectangle to visualize the bounding rect
            cv2.rectangle(maskHSV, (x, y), (x+w, y+h), (0, 255, 0), 2)
         
            # get the min area rect
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            # convert all coordinates floating point values to int
            box = np.int0(box)
            # draw a red 'nghien' rectangle
            cv2.drawContours(img, [box], 0, (0, 0, 255))
        
            # Print data
            #print(cv2.contourArea(c))
            
            M = cv2.moments(c)
            # calculate x,y coordinate of center
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(img, (cX, cY), 3, (0, 255, 0), -1)
            #cv2.circle(img, (np.uint8(np.ceil(x/kpCnt)), np.uint8(np.ceil(y/kpCnt))), 1, (0, 0, 255), 3)
            
            # save data
            listOfAreas.append([cv2.contourArea(c), cX, cY]) # list of areas with their center of mass
    return img


def analyseAreasProximity(listOfAreas, dist_tresh):
    listOfAreasInsideTresh = []
    for area_a in listOfAreas:
        list1Area = []
        list1Area.append(area_a)
        flag = True
        for area_b in listOfAreas:
            dist = pow(pow(max(area_a[1],area_b[1])-min(area_a[1],area_b[1]),2) + pow(max(area_a[2],area_b[2])-min(area_a[2],area_b[2]),2),0.5)
            if dist < dist_tresh and area_b != area_a:
                list1Area.append(area_b)  
        #for listAreas in listOfAreasInsideTresh:
         #   if Counter(listAreas) == Counter(list1Area):
         #       flag = False
        #if flag:
        listOfAreasInsideTresh.append(list1Area)
    return listOfAreasInsideTresh

def findDuplicatesAreas(listOfAreasInsideTresh):           
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

def drawAreas(listOfAreas, image):
    for listOfArea in listOfAreas:
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
        
        
def getTotalArea(listOfArea):
    totalArea = 0
    for area in listOfArea:
        totalArea = totalArea + area[0]
    return totalArea
                        

def main(): 
    listOfAreas = []
    
    img = imageContoursProp("/Users/hugodaniel/MATLAB-Drive/Medellin/Images/Bebeplantes.jpg", listOfAreas)
    
    listOfAreasInsideTresh = analyseAreasProximity(listOfAreas, 150)
    #for elem in listOfAreasInsideTresh:
    #    print(len(elem))
    listAreaGroup = findDuplicatesAreas(listOfAreasInsideTresh)
    drawAreas(listAreaGroup, img)
    
    cv2.namedWindow("image")
    cv2.imshow("image",img)

    cv2.waitKey(0)
  
    
if __name__=="__main__":
    main()


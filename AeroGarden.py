"""

    Editor: Hugo Daniel
    Project name: AreoBot U.N.
    Date: September 2018
    Location: Universidad National de Colombia sede Medellin

    Description: Class that defines the areoponic bed proproties
    
    
"""

import numpy as np
#import webcamRaspBerryPi as camera

class DictOfPlantes:
    # list = [("name", area1, area2),("name", area1, area2)...]
    # -> Areas or used to know how much place is recquired for a plant of a certain size
    myList = [("Tomato", 100, 400),("Basil", 100, 150),("Lettuce", 100, 400)]


class Plant:
    
    def __init__(self, name, area):
        self.name = name
        self.area = area
    

class AreoBed:
    _bedLength = 4 # lenght of one bed in meters: Private
    _bedWidth = 2 # width of one bed in meters: Private
    _unitLength = 1 # lenght of one unit in meters: Private
    _unitWidth = 1 # width of one unit in meters: Private
    _unitQuantityLength = 6 # quantity of units for the length: Private
    _unitQuantityWidth = 5 # quantity of units for the width: Private
        
    _unitArea = _unitLength * _unitWidth # unit area in meter^2
    _bedUnitQuantity = _unitQuantityLength * _unitQuantityWidth # total quanty of units
    
    def __init__(self):    
        self.listOfPlants = [] # List of plants
        # Bed map with plants location denoted with line and column: [line][column]
        self.bedMap = np.array([[None, None, None, None, None],
                                [None, None, None, None, None],
                                [None, None, None, None, None],
                                [None, None, None, None, None],
                                [None, None, None, None, None],
                                [None, None, None, None, None]])
    
    def addPlant(self, name="none", area=0):
        self.listOfPlants.append(Plant(name, area))
    
    def deletePlant(self, position):
        for plant in self.listOfPlants:
            if np.array_equal(plant.position, position):                
                self.listOfPlants.remove(plant)
    
    def addPlantMap(self, line, column, plant_tuple, area=0):
        self.bedMap[line][column] = Plant(plant_tuple[0],area)
    
    def deletePlantMap(self, line, column, name):
        self.bedMap[line][column] = None # -1 because arrays starts at 0, but entering 1 is more natural
    
    def displayBedMap(self):
        print(self.bedMap)
    
class Row:
    
    def __init__(self,name="none"):
        self.name = name    
        self.listOfBeds = [] # List of aeroponics beds
    
    def addAreoBed(self):
        self.listOfBeds.append(AreoBed())
        
    def deleteBed(self,bed_number):
        self.listOfBeds.pop(bed_number)

class Garden:
    
    # Init method
    def __init__(self, name="Areoponic Garden"):
        self.name = name    
        self.listOfRows = [] # List of rows
    
    # Functiannaries methods
    def addRow(self,name="none"):
        self.listOfRows.append(Row(name))
    
    def addBed(self, row_number):
        self.listOfRows[row_number].addAreoBed()       
        
    def addPlant(self, row_number, bed_number, plant_position, plant_name="none"):
        self.listOfRows[row_number].listOfBeds[bed_number].addPlant(plant_position,plant_name)
        
    def deletePlant(self, row_number, bed_number, plant_position):
        self.listOfRows[row_number].listOfBeds[bed_number].deletePlant(plant_position)
        
    def deleteBed(self, row_number, bed_number):
        self.listOfRows[row_number].deleteBed(bed_number)
        
    def deleteRow(self,row_number):
        self.listOfRows.pop(row_number)
        
        
    def addPlantMapGarden(self, row_number, bed_number, line, column, plant_tuple):
        if self.listOfRows[row_number].listOfBeds[bed_number].bedMap[line][column] == None:
            self.listOfRows[row_number].listOfBeds[bed_number].addPlantMap(line,column,plant_tuple)
            return 0
        else:
            print("ERROR in: addPlantMap. Existing plant in this location")
            return 1
    
    def deletePlantMap(self, row_number, bed_number, line, column):
        if self.listOfRows[row_number].listOfBeds[bed_number].bedMap[line][column] != None and self.listOfRows[row_number].listOfBeds[bed_number].bedMap[line][column] != "Used":
            self.listOfRows[row_number].listOfBeds[bed_number].bedMap[line][column] = None
            return 0
        else:
            print("ERROR in: deletePlantMap. No existing plant in this location")
            return 1
            
    def coppyPositionPlantMap(self, row_number, bed_number, line, column):
        if self.listOfRows[row_number].listOfBeds[bed_number].bedMap[line][column] != None and self.listOfRows[row_number].listOfBeds[bed_number].bedMap[line][column] != "Used":
            return self.listOfRows[row_number].listOfBeds[bed_number].bedMap[line][column]
        else:
            print("ERROR in: coppyPositionPlantMap. No existing plant in this location")
            return 1
        
    def updatePlantsArea(self):
        for row in self.listOfRows:
            for bed in row.listOfBeds:
                for line in range(bed._unitQuantityLength):
                    for column in range(bed._unitQuantityWidth):
                        if bed.bedMap[line][column] != None and bed.bedMap[line][column] != "Used":
                            bed.bedMap[line][column].area = 200
                            #camera.getPlantArea = self.listOfRows[row_number].listOfBeds[bed_number].bedMap[line][column].area
    
    """
    def findSpaceForPlant(self,coordinates):
        for row in self.listOfRows:
            for bed in row.listOfBeds:
                for line in range(1,bed._unitQuantityLength-1):
                    for column in range(1,bed._unitQuantityWidth-1):
                        if bed.bedMap[line-1][column] == None and bed.bedMap[line][column+1] == None and bed.bedMap[line][column-1] == None and bed.bedMap[line+1][column] == None:                
                            coordinates[0] = line
                            coordinates[1] = column
                            return 0
        return 1
    """
    
                            
    # Working in the garden methods
    def addSetOfPlants(self, plant_tuple, quantity_of_plants):   
        # Look for available space
        quantity_of_available_units = 0
        for row in self.listOfRows:
            for bed in row.listOfBeds:
                quantity_of_available_units = quantity_of_available_units + (bed.bedMap==None).sum()
        
        if quantity_of_available_units < quantity_of_plants:
            print("ERROR in: addSetOfPlants. Not enough available space in the garden")
            print(quantity_of_available_units, " units are availables")           
            return 1
        else:   
            plants_to_plant = quantity_of_plants
            
            for row in self.listOfRows:
                for bed in row.listOfBeds:
                    for line in range(bed._unitQuantityLength):
                        for column in range(bed._unitQuantityWidth):
                            if plants_to_plant == 0:
                                return 0
                            elif bed.bedMap[line][column] == None:
                                bed.addPlantMap(line, column, plant_tuple)
                                plants_to_plant = plants_to_plant - 1
    
    def movePlant(self, row_number, bed_number, line, column, new_line, new_column):
        plant = self.coppyPositionPlantMap(row_number, bed_number, line, column)
        if plant == 1:
            return 1        
        if self.listOfRows[row_number].listOfBeds[bed_number].bedMap[new_line][new_column] == None:
            self.listOfRows[row_number].listOfBeds[bed_number].bedMap[new_line][new_column] = plant
        else:
            print("ERROR in: addPlantMap. Existing plant in this location")
            return 1
        if self.deletePlantMap(row_number, bed_number, line, column):
            return 1
                  
    """
    def moveMaturePlants(self):
        # Function looks in the areas of the plants and compare them with a treshold value
        # to determine if they needs more space
        for row in self.listOfRows:
            for bed in row.listOfBeds:
                for line in range(bed._unitQuantityLength):
                    for column in range(bed._unitQuantityWidth):
                        for ref_plant in DictOfPlantes.myList:
                            if bed.bedMap[line][column] != None and bed.bedMap[line][column] != "Used":
                                if bed.bedMap[line][column].name == ref_plant[0] and bed.bedMap[line][column].area > ref_plant[1]:                                         
                                    coordinates = np.array([None,None])
                                    if self.findSpaceForPlant(coordinates) != 1:     
                                        #The plant will take the space of 4 plants
                                        bed.bedMap[coordinates[0]][coordinates[1]] = bed.bedMap[line][column] 
                                        bed.bedMap[coordinates[0]-1][coordinates[1]] = "Used"
                                        bed.bedMap[coordinates[0]][coordinates[1]+1] = "Used"
                                        bed.bedMap[coordinates[0]][coordinates[1]-1] = "Used"
                                        bed.bedMap[coordinates[0]+1][coordinates[1]] = "Used"
      """                                              
                                                    
    
    #def harvestPlantMap(self):
        
        
    # User friendly functions
    def displayGarden(self):
        print("Garden name: ",self.name)
        for row in self.listOfRows:
            print("Row: ",1 + self.listOfRows.index(row))
            for bed in row.listOfBeds:
                print("Bed: ",1 + row.listOfBeds.index(bed))
                for plant in bed.listOfPlants:
                    print("Plant name and position: ", plant.name," at ", plant.position)
                    
    def displayGardenMap(self):
        print("Garden name: ",self.name)
        for row in self.listOfRows:
            print("Row: ",1 + self.listOfRows.index(row))
            for bed in row.listOfBeds:
                print("Bed: ",1 + row.listOfBeds.index(bed))
                
                coppy_array = np.array([[None, None, None, None, None],
                                [None, None, None, None, None],
                                [None, None, None, None, None],
                                [None, None, None, None, None],
                                [None, None, None, None, None],
                                [None, None, None, None, None]])
                for line in range(bed._unitQuantityLength):
                    for column in range(bed._unitQuantityWidth):
                        if bed.bedMap[line][column] != None and bed.bedMap[line][column] != "Used":
                            coppy_array[line][column] = bed.bedMap[line][column].name
                        elif bed.bedMap[line][column] == "Used":
                            coppy_array[line][column] = bed.bedMap[line][column]
                print(coppy_array)
        
    def displayGardenMapAreas(self):
        print("Garden name: ",self.name)
        for row in self.listOfRows:
            print("Row: ",1 + self.listOfRows.index(row))
            for bed in row.listOfBeds:
                print("Bed: ",1 + row.listOfBeds.index(bed))
                
                coppy_array = np.array([[None, None, None, None, None],
                                [None, None, None, None, None],
                                [None, None, None, None, None],
                                [None, None, None, None, None],
                                [None, None, None, None, None],
                                [None, None, None, None, None]])
                for line in range(bed._unitQuantityLength):
                    for column in range(bed._unitQuantityWidth):
                        if bed.bedMap[line][column] != None and bed.bedMap[line][column] != "Used":
                            coppy_array[line][column] = bed.bedMap[line][column].area
                        elif bed.bedMap[line][column] == "Used":
                            coppy_array[line][column] = bed.bedMap[line][column]
                print(coppy_array)
                








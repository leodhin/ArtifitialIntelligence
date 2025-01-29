from constants import WEIGHT_DISTANCE

class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
# Class to represent a cell in the grid
class Cell:
    def __init__(self, pos, parent):
        self.pos = pos
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0
        self.isWalkable = True
        self.isEnd = False
        self.isStart = False
        
    # set the g value
    def calculateAccumulatedWeight(self):
        if self.parent == None:
            self.g = WEIGHT_DISTANCE
        else:
          self.g = self.parent.g + WEIGHT_DISTANCE
    # set the h value
    def calculateHeuristic(self, end):
        self.h = abs(self.pos.x - end.x) + abs(self.pos.y - end.y)
        return self.h
    
    # set the f value
    def calculateF(self):
        self.f = self.g + self.h
    # set the f value 
    def calculateValues(self, end):
        self.calculateAccumulatedWeight()
        self.calculateHeuristic(end)
        self.calculateF()
        
    # set the h value
    def set_h(self, value):
        self.h = value
    
    # print the cell
    def __str__(self):
        return f'Cell({self.pos.x}, {self.pos.y})'
WEIGHT_DISTANCE = 10
exit = (6, 6)

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
        self.isWalkable = False
        self.isEnd = False
        self.isStart = False
        
    # set the g value
    def calculateAccumulatedWeight(self):
        self.g = self.parent.g + WEIGHT_DISTANCE
    # set the h value
    def calculateHeuristic(self):
        self.h = abs(self.pos.x - exit[0]) + abs(self.pos.y - exit[1])
        return self.h
    
    # set the f value
    def calculateF(self):
        self.f = self.g + self.h
    # set the f value 
    def calculateValues(self):
        self.calculateAccumulatedWeight()
        self.calculateHeuristic()
        self.calculateF()
        
    # set the h value
    def set_h(self, value):
        self.h = value
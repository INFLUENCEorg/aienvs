from random import randint
from numpy import array, ndarray


class Map():
    """
    Contains a static discrete square map
    Each position in the map can have various values, 
    eg a free space or a wall.
    This map is like a paper map of the environment,
    so without moving parts.
    """

    def __init__(self, map:list):
        """
        @param map: list of strings. Each string represents one line (x direction) 
        of the map. All lines must have same length.  There must be at least one line.
        The first line represents y=0, the second line y=1, etc.
        The first column of each like represents x=0, the second x=1, etc.
        """
        self._map = map
        width = self.getWidth()
        for line in map:
            if width != len(line):
                raise ValueError("Map must be square")
        (self._cachedTaskPositions, self._cachedTaskWeights) = self._taskPositions()

    def getWidth(self) -> int:
        return len(self._map[0])
    
    def getHeight(self) -> int:
        return len(self._map)
    
    def get(self, pos:ndarray) -> str:
        """
        @param pos the map position as (x,y) tuple 
        @return character at given pos 
        """
        return self._map[pos[1]][pos[0]]
    
    def getTaskPositions(self) -> list:
        """
        @return: the list of task positions ( (x,y) tuples )
        """
        return self._cachedTaskPositions
    
    def getTaskWeights(self) -> list:
        """
        @return: list of task weights, ordered to match getTaskPositions
        """
        return self._cachedTaskWeights
    
    def _taskPositions(self):
        poslist = []
        weightlist = []
        for y in range(self.getHeight()):
            for x in range(self.getWidth()):
                value = self.get((x, y))
                if value in "123456789":
                    poslist += [ array([x, y]) ]
                    weightlist += [ int(value)]
        weightsum = sum(weightlist)
        return (poslist, [x / weightsum for x in weightlist])
    
    def getRandomPosition(self) -> array:
        """
        @return: numpy array : random position on the map. The returned position 
        will be #isInside but may be on a wall.
        """
        return array([randint(0, self.getWidth() - 1), randint(0, self.getHeight() - 1)])
    
    def isInside(self, pos:ndarray) -> bool:
        """
        @return: true iff the position is within the bounds of this map. The top left is [0,0]
        """
        return pos[0] >= 0 and pos[0] < self.getWidth() and pos[1] >= 0 and pos[1] < self.getHeight()
    
    def getPart(self, area:ndarray):  # -> Map
        """
        @param area a numpy array of the form [[xmin,ymin],[xmax,ymax]]. 
        @return: A copy of a part of this map, spanning from [xmin,ymin] to [xmax, ymax]
        (both ends inclusive). 
        """
        newmap = []
        for y in range(area[0, 1], area[1, 1] + 1):
            newmap = newmap + [self._map[y][area[0, 0]:area[1, 0] + 1]]
        return Map(newmap)
    

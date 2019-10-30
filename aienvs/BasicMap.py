from random import Random
import random
from numpy import array, ndarray
import copy
from aienvs.utils import hashf


class BasicMap():
    """
    Contains a static (immutable) discrete square map
    Each position in the map can have various values, 
    eg a free space or a wall.
    This map is like a paper map of the environment,
    so without moving parts.
    immutable: nobody should access private variables
    and there are no setters so this object will never change.
    """

    def __init__(self, map:list):
        """
        @param map: list of strings. Each string represents one line (x direction) 
        of the map. All lines must have same length.  There must be at least one line.
        The first line represents y=0, the second line y=1, etc.
        The first column of each like represents x=0, the second x=1, etc.
        There are a number of agreed-on characters on the map:
        - * indicates a wall
        - '.' indicates a free floor tile
        - digit 1..9 indicates a location where a task can appear. The number indicates
        the weight of the task: the task location is picked by weighted random choice.
        But these are optional and only to ensure a reasonable standard interpretation.
        This BasicMap does not care what characters
        are placed on the map and what they mean. 
        """
        self._map = map
        width = self.getWidth()
        for line in map:
            if width != len(line):
                raise ValueError("All lines in map must have width " + str(self.getWidth()) + " but found " + str(line))
        self._squares = self._getSquaresDict()

    def getWidth(self) -> int:
        return len(self._map[0])
    
    def getHeight(self) -> int:
        return len(self._map)
    
    def getFullMap(self):
        """
        @return: a copy of the original map provided to the constructor
        """
        return copy.deepcopy(self._map)
    
    def get(self, pos:ndarray) -> str:
        """
        @param pos the map position as (x,y) tuple 
        @return character at given pos or None if point is outside map
        """
        if not self.isInside(pos):
            return None
        return self._map[pos[1]][pos[0]]
    
    def getMapPositions(self, allowed:str) -> list:
        """
        @param allowed string containing all allowed characters
        @return the map positions (list of ndarray) that contain allowed chars
        """
        poslist = []
        for char in allowed:
            if char in self._squares.keys():
                poslist = poslist + self._squares[char]
        return poslist
    
    def getFreeMapPosition(self) -> array:
        """
        @return:random map position (x,y) that is not occupied by a wall.
        WARNING: this may hang indefinitely if there are no positions without walls
        on the map.
        """
        freepos = self.getMapPositions(".")
        if (len(freepos) == 0):
            raise Exception("The map does not contain any free tiles")
        return random.choice(freepos)
            
    def getRandomPosition(self) -> array:
        """
        @param random number generator,  instance of Random()
        @return: numpy array : random position on the map. The returned position 
        will be #isInside but may be on a wall.
        """
        return array([random.randint(0, self.getWidth() - 1), random.randint(0, self.getHeight() - 1)])
    
    def isInside(self, pos:ndarray) -> bool:
        """
        @return: true iff the position is within the bounds of this map. The top left is [0,0]
        """
        return pos[0] >= 0 and pos[0] < self.getWidth() and pos[1] >= 0 and pos[1] < self.getHeight()
    
    def isFree(self, pos:ndarray):
        """
        @return true iff the given pos has space for a robot,
        so it must be on the map and not on a wall.
        This assumes the conventional "*" char is used to indicate walls.
        """
        return self.isInside(pos) and self.get(pos) != "*"         

    def getPart(self, area:ndarray):  # -> Map
        """
        @param area a numpy array of the form [[xmin,ymin],[xmax,ymax]]. 
        @return: A copy of a part of this map, spanning from [xmin,ymin] to [xmax, ymax]
        (both ends inclusive). 
        """
        newmap = []
        for y in range(area[0, 1], area[1, 1] + 1):
            newmap = newmap + [self._map[y][area[0, 0]:area[1, 0] + 1]]
        return BasicMap(newmap)
    
    def _getSquaresDict(self) -> dict:
        """
        Build the squares dict
        """
        squares = {}
        for y in range(0, len(self._map)):
            row = self._map[y]
            for x in range(0, len(row)):
                char = row[x]
                pos = array([x, y])
                if char in squares.keys():
                    squares[char].append(pos)
                else:
                    squares[char] = [pos]
        
        return squares
    
    def __deepcopy__(self, memo):
        # A MAP IS IMMUTABLE so this is easy
        return self
    
    def __eq__(self, other):
        return self._map == other._map

    def __hash__(self) -> int:
        return hashf(self._map)
 

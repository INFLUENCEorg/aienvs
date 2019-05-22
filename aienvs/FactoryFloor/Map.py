from random import randint


class Map():
    """
    Contains a discrete square map
    Each position in the map can have various values, 
    eg a free space or a wall. 
    """

    def __init__(self, map:list):
        """
        @param map: list of strings. Each string represents one line (x direction) 
        of the map. All lines must have same length.  There must be at least one line.
        """
        self._map = map
        width = self.getWidth()
        for line in map:
            if width != len(line):
                raise ValueError("Map must be square")
        self._cachedTaskPositions = self._taskPositions()

    def getWidth(self):
        return len(self._map[0])
    
    def getHeight(self):
        return len(self._map)
    
    def get(self, pos:tuple):
        """
        @param pos the map position as (x,y) tuple 
        @return character at given pos 
        """
        return self._map[pos[1]][pos[0]]
    
    def getTaskPositions(self):
        """
        @return: the list of task positions ( (x,y) tuples )
        """
        return self._cachedTaskPositions
    
    def _taskPositions(self):
        result = []
        for y in range(self.getHeight()):
            for x in range(self.getWidth()):
                if self.get((x, y)) in "123456789":
                    result += [ (x, y) ]
        return result
    
    def getRandomPosition(self):
        """
        @return: random position on the map. The returned position 
        will be #isInside but may be on a wall.
        """
        return (randint(0, self.getWidth() - 1), randint(0, self.getHeight() - 1))
    
    def isInside(self, pos:tuple):
        """
        @return true iff the position is within the bounds of this map.
        """
        return pos[0] >= 0 and pos[0] < self.getWidth() and pos[1] >= 0 and pos[1] < self.getHeight()
    

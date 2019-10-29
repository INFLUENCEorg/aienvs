from random import Random
import random
from numpy import array, ndarray
import copy
from aienvs.BasicMap import BasicMap


class Map(BasicMap):
    """
    Contains a static (immutable) discrete square map
    Each position in the map can have various values, 
    eg a free space or a wall.
    This map is like a paper map of the environment,
    so without moving parts.
    immutable means nobody should access private variables
    and there are no setters so this object will never change.
    """

    def __init__(self, map:list, ptask:float):
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
        @param ptask: probability that a task is added in a time step (this is assuming
        a stepped simulation, rather than a timed one). Ignored if there are no digits
         on the floor
        """
        super().__init__(map)
        self._taskProbability = ptask
        self._cachedTaskPositions = tuple(Map._getTasksList(map))
         
        weights = Map._getWeightsList(map)
        totalweight = sum(weights)
        if totalweight == 0:
            self._cachedTaskWeights = tuple([])
        else:
            self._cachedTaskWeights = tuple([w / totalweight for w in weights])
    
    def getTaskProbability(self):
        """
        @return: the probability that a task will appear on the map 
        during a time step
        """
        return self._taskProbability
  
    def getTaskPositions(self) -> tuple:
        """
        @return: the list of task positions ( (x,y) tuples )
        """
        return self._cachedTaskPositions
     
    def getTaskWeights(self) -> tuple:
        """
        @return: list of task weights, ordered to match getTaskPositions
        """
        return self._cachedTaskWeights
    
    @staticmethod
    def _getTasksList(map:list):
        """
        @param map the map , see __init__
        Get list of all task positions on the map, in order of colums / rows.
        Positions are numpy arrays [x,y].
        """
        poslist = []
        for y in range(len(map)):
            for x in range(len(map[0])):
                if map[y] [x] in "123456789":
                    poslist += [ array([x, y]) ]
        return poslist
    
    @staticmethod
    def _getWeightsList(map:list):
        """
        @param map the map , see __init__
        Get list of all weights on the map, in order of colums / rows
        """
        weightlist = []
        for row in map:
            for value in row:
                if value in "123456789":
                    weightlist += [ int(value) ]
        return weightlist
    
    def getPart(self, area:ndarray):  # -> Map
        """
        @param area a numpy array of the form [[xmin,ymin],[xmax,ymax]]. 
        @return: A copy of a part of this map, spanning from [xmin,ymin] to [xmax, ymax]
        (both ends inclusive). 
        """
        newmap = super().getPart(area)._map
        
        # use raw original values to compute scalings
        oldweight = sum(Map._getWeightsList(self._map))
        if oldweight == 0:
            newtaskp = 0
        else:
            newtaskp = self._taskProbability * sum(Map._getWeightsList(newmap)) / oldweight
        return Map(newmap, newtaskp)
    

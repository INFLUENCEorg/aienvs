from numpy import array, ndarray, array_equal
from aienvs.utils import hashf


class Robot():
    """
    A robot on the BasicFloor. Immutable.
    """

    def __init__(self, robotId, pos:ndarray):
        """
        @param pos tuple (x,y) with initial robot position.
        Initializes the robot
        """
        if not isinstance(pos, ndarray):
            raise ValueError("pos must be numpy array but got " + str(type(pos)))
        self._id = robotId
        self._pos = pos

    def getId(self):
        """
        returns the robot identifier
        """
        return self._id

    def getPosition(self):
        """
        @return: (x,y) array with current robot position
        """
        return self._pos
    
    def __str__(self):
     """
     for hashing
     """
     return "Id: " + self._id + " Pos: " + str(self._pos)
        
    def __eq__(self, other):
        return self._id == other._id and array_equal(self._pos, other._pos)
    
    def __hash__(self) -> int:
        return hash(self._id) + hashf(self._pos)


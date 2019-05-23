from numpy import array, ndarray


class FactoryFloorRobot():
    """
    A robot on the factory floor
    """
    idCounter = 1;  # static, used for ID generation
    
    def __init__(self, pos:ndarray):
        """
        @param pos tuple (x,y) with initial robot position.
        Initializes the robot
        """
        if not isinstance(pos, ndarray):
            raise ValueError("pos must be numpy array but got " + str(type(pos)))
        self._pos = pos
        self._id = "robot" + str(FactoryFloorRobot.idCounter)
        FactoryFloorRobot.idCounter += 1

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
    
    def setPosition(self, newpos):
        """
        @param newpos: an array (x,y) with the new robot position
        """
        self._pos = newpos
    
    def __str__(self):
     return self._id
        

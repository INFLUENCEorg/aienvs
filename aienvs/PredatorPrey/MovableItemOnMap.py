from numpy import array, ndarray
from numpy.linalg import norm


class MovableItemOnMap:
    """
    A movable item on the map. immutable.
    """

    def __init__(self, id:str, pos:ndarray, active:bool):
        """
        @param entityId the 
        @param pos tuple (x,y) with initial entity position.
        @param active true iff the item is still active (not removed).
        Items are removed according to game rules when they catch/get caught
        """
        if not isinstance(pos, ndarray):
            raise ValueError("pos must be numpy array but got " + str(type(pos)))
        self._id = id
        self._pos = pos
        self._active = active

    def getId(self) -> str:
        """
        returns the unique identifier
        """
        return self._id

    def getPosition(self) -> ndarray:
        """
        @return: numpy array with current position
        """
        return self._pos
    
    def isAdjacent(self, pos:ndarray):
        """
        @return true iff given pos is adjacent to self.pos (N,E,S or W)
        """
        return norm(pos - self._pos) <= 1
    
    def isActive(self):
        """
        @return true iff the object is still active (not removed from the map)
        """
        return self._active
    
    def withStep(self, action:int) -> MovableItemOnMap:
        """
        @param action the action number to be done- 0=y+1 1=y-1 2=x-1 3=x+1. 
        @return:  new MovableItemOnMap, with step applied.
        This does not check any legality of the new position, so the 
        position may run off the map or on a wall.
        """
        newpos = self._pos
        if action == 0:
            newpos = newpos + [0, 1]
        elif action == 1:
            newpos = newpos + [0, -1]
        elif action == 2:
            newpos = newpos + [-1, 0]
        elif action == 3:
            newpos = newpos + [1, 0]
        return MovableItemOnMap(self._id, newpos, self._active)
    
    def __eq__(self, other):
        return self._id == other._id and self._pos == other._pos 

    def __str__(self):
     """
     for hashing
     """
     return "Id: " + self._id + " Pos: " + str(self._pos)

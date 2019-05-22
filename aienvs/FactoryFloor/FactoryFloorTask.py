class FactoryFloorTask():
    """
    A task on the factory floor
    """

    def __init__(self, id_, newpos:tuple):
        """
        Initializes the task, places it at (0,0)
        """
        self.pos = newpos
        self._id = id_

    def getId(self):
        """
        returns the task identifier
        """
        return self._id

    def getPosition(self):
        """
        @return: (x,y) tuple with task position
        """
        return self.pos
    
    def __str__(self):
     return "Task"+str(self._id)
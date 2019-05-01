class FactoryFloorTask():
    """
    A task on the factory floor
    """

    def __init__(self, id_, pos_x:int=0, pos_y:int=0):
        """
        Initializes the task, places it at (0,0)
        """
        self.pos_x = pos_x
        self.pos_y = pos_y
        self._id = id_

    def getId(self):
        """
        returns the task identifier
        """
        return self._id


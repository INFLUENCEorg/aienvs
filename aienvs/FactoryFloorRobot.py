class FactoryFloorRobot()
    """
    A robot on the factory floor
    """

    def __init__(self, pos_x:int=0, pos_y:int=0):
        """
        Initializes the robot, places it at (0,0)
        """
        self._pos_x = pos_x
        self._pos_y = pos_y

    def takeAction(self, actionId):
        """
        Taking action
        """
        if ACTION.

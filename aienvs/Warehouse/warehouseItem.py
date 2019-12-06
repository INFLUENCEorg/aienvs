from numpy import ndarray


class WarehouseItem():
    """
    A task on the factory floor
    """
    ID = 1  # to generate new task ids

    def __init__(self, item_id, pos:ndarray):
        """
        Initializes the item, places it at (0,0)
        """
        self._pos = pos
        self._id = item_id

    def get_id(self):
        """
        returns the task identifier
        """
        return self._id

    def get_position(self):
        """
        @return: (x,y) tuple with task position
        """
        return self._pos

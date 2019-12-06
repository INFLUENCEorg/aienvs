import numpy as np
from aienvs.FactoryFloor.Map import Map


class WarehouseState():

    def __init__(self, n_rows, n_columns, robots, items):
        """
        """
        self.n_rows = n_rows
        self.n_columns = n_columns
        self.robots = robots
        self.items = items

    def get_state_bitmap(self):
        """
        """
        state_bitmap = np.zeros([self.n_rows, self.n_columns, 2], dtype=np.int)
        for item in self.items:
            position = item.get_position()
            state_bitmap[position[0], position[1], 0] = 1
        for robot in self.robots:
            position = robot.get_position()
            state_bitmap[position[0], position[1], 1] = 1

        return state_bitmap

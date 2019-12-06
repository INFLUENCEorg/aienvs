from numpy import array, ndarray


class WarehouseRobot():
    """
    A robot on the warehouse
    """
    def __init__(self, robot_id, robot_position, robot_domain, max_n_items):
        """
        @param pos tuple (x,y) with initial robot position.
        Initializes the robot
        """
        self._id = robot_id
        self._pos = robot_position
        self.robot_domain = robot_domain
        self.max_n_items = max_n_items
        self.items_collected = 0
        self.done = False


    def get_id(self):
        """
        returns the robot identifier
        """
        return self._id

    def get_position(self):
        """
        @return: (x,y) array with current robot position
        """
        return self._pos

    def observe(self, state):
        """
        Retrieve observation from envrionment state
        """

        observation = state[self.robot_domain[0]: self.robot_domain[2],
                            self.robot_domain[1]: self.robot_domain[3], :]
        return observation

    def act(self, action):
        """
        Take an action
        """
        if action == 0:
            new_pos = [self._pos[0], self._pos[1] + 1]
        if action == 1:
            new_pos = [self._pos[0], self._pos[1] - 1]
        if action == 2:
            new_pos = [self._pos[0] - 1, self._pos[1]]
        if action == 3:
            new_pos = [self._pos[0] + 1, self._pos[1]]
        self.set_position(new_pos)

    def set_position(self, new_pos):
        """
        @param new_pos: an array (x,y) with the new robot position
        """
        if self.robot_domain[0] <= new_pos[0] <= self.robot_domain[2] and \
           self.robot_domain[1] <= new_pos[1] <= self.robot_domain[3]:
            self._pos = new_pos

    def collect_item(self):
        self.items_collected += 1
        if self.items_collected >= self.max_n_items:
            self.done = True

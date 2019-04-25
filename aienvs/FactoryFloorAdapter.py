class FactoryFloorAdapter(gym.Env):
    """
    An adapter for the factory floor environment
    """

    def __init__(self,  parameters:dict={'steps':1000):
        """
        TBA
        """
        self.parameters = parameters
        self._robots = []
        self._tasks = []
        self.reset()
    
    def step(self, action:spaces.Dict):
        for robot in self._robots:
            robot.takeAction(action['robot_id'])

        self._newTasksAppear()
        global_reward = self._computePenalty(self._tasks)
        done = (self.parameters['steps'] >= self._step)
        
        return obs, global_reward, done, []
    
    def reset(self):
        self._step=0
        
    def render(self):
        pass # todo
    
    def close(self):
        pass # todo

    def seed(self):
        pass # todo

    ########## Private functions ##########################


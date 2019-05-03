import gym
from gym import spaces
from aienvs.FactoryFloorRobot import FactoryFloorRobot
from aienvs.FactoryFloorTask import FactoryFloorTask


class FactoryFloorAdapter(gym.Env):
    """
    An adapter for the factory floor environment
    """

    def __init__(self, parameters:dict={'steps':1000, 'n_robots':2, 'n_tasks':5, 'x_size':10, 'y_size':15}):
        """
        TBA
        """
        self.parameters = parameters

        self._robots = []
        while len(self._robots) < parameters['n_robots']:
            self._robots.append(FactoryFloorRobot(id_=len(self._robots)))

        self._tasks = []
        while len(self._tasks) < parameters['n_tasks']:
            self._tasks.append(FactoryFloorTask(id_=len(self._tasks)))

        self.observation_space = spaces.MultiDiscrete([parameters['x_size'], parameters['y_size']])
        self.action_space = self._getActionSpace()
        self.reset()
    
    def step(self, actions:spaces.Dict):
        for robot in self._robots:
            self._applyAction(robot, actions[robot.getId()])

        self._newTasksAppear()
        global_reward = self._computePenalty()
        done = (self.parameters['steps'] <= self._step)
        obs = self.observation_space.sample()
        self._step += 1
        
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

    def _applyAction(self, robot, action):
        if ACTIONS.get(action) == "ACT":
            for task in self._tasks:
                if (robot.pos_x, robot.pos_y) == (task.pos_x, task.pos_y):
                    self._tasks.pop(task.getId())
        elif ACTIONS.get(action) == "UP":
            return NotImplementedError
        elif ACTIONS.get(action) == "RIGHT":
            return NotImplementedError
        else if ACTIONS.get(action) == "DOWN":
            return NotImplementedError
        else if ACTIONS.get(action) == "LEFT":
            return NotImplementedError

    def _newTasksAppear(self):
        pass

    def _computePenalty(self):
        penalty = 0
        for task in self._tasks:
            penalty += 1
        return penalty

    def _getActionSpace(self):
        """
        @returns the actionspace:
         two possible actions for each lightid: see PHASES variable
        """
        return spaces.Dict({robot.getId():spaces.Discrete(len(ACTIONS)) for robot in self._robots})

ACTIONS={
    0: "ACT",
    1: "UP",
    2: "RIGHT",
    3: "DOWN",
    4: "LEFT"
}   

import gym
from gym import spaces
from aienvs.FactoryFloor.FactoryFloorRobot import FactoryFloorRobot
from aienvs.FactoryFloor.FactoryFloorTask import FactoryFloorTask
from aienvs.Environment import Env
import numpy as np
from numpy import array
from numpy import vstack
import copy


class FactoryFloor(Env):
    """
    The factory floor environment
    """
    DEFAULT_PARAMETERS = {'steps':1000, 
                'n_robots':2, 
                'n_tasks':5, 
                'x_size':10,
                'y_size':15,
                'task_prob':0.3
                }

    ACTIONS={
        0: "ACT",
        1: "UP",
        2: "RIGHT",
        3: "DOWN",
        4: "LEFT"
    }   

    def __init__(self, parameters:dict={}):
        """
        TBA
        """
        self._parameters = copy.deepcopy(self.DEFAULT_PARAMETERS)
        self._parameters.update(parameters)

        self._robots = []
        while len(self._robots) < self._parameters['n_robots']:
            self._robots.append(FactoryFloorRobot(id_=len(self._robots)))

        self._tasks = []
        samplingSpace = spaces.MultiDiscrete([self._parameters['x_size'], self._parameters['y_size']])
        while len(self._tasks) < self._parameters['n_tasks']:
            self._tasks.append(FactoryFloorTask(id_=len(self._tasks), pos_x=samplingSpace.sample()[0], pos_y=samplingSpace.sample()[1]))

    def step(self, actions:spaces.Dict):
        for robot in self._robots:
            self._applyAction(robot, actions[robot.getId()])

        self._newTasksAppear()
        global_reward = self._computePenalty()
        done = (self._parameters['steps'] <= self._step)
        obs = self._createBitmap()
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

    @property
    def observation_space(self):
        return spaces.MultiDiscrete([2, self._parameters['x_size'], self._parameters['y_size']]) # one layer for tasks the second layer for robots

    @property
    def action_space(self):
        return spaces.Dict({robot.getId():spaces.Discrete(len(self.ACTIONS)) for robot in self._robots})

    ########## Private functions ##########################

    def _createBitmap(self):
        bitmapRobots = np.zeros((self._parameters['x_size'], self._parameters['y_size']))
        bitmapTasks = np.zeros((self._parameters['x_size'], self._parameters['y_size']))
        for robot in self._robots:
            bitmapRobots[robot.pos_x, robot.pos_y]+=1

        for task in self._tasks:
            bitmapTasks[task.pos_x, task.pos_y]+=1

        return vstack((bitmapRobots, bitmapTasks))

    def _applyAction(self, robot, action):
        if not self._isActionAllowed( robot, action ):
            return False

        if self.ACTIONS.get(action) == "ACT":
            for task in self._tasks:
                if (robot.pos_x, robot.pos_y) == (task.pos_x, task.pos_y):
                    self._tasks.pop(task.getId())

        elif self.ACTIONS.get(action) == "UP":
            robot.pos_y=+1
        elif self.ACTIONS.get(action) == "RIGHT":
            robot.pos_x+=1
        elif self.ACTIONS.get(action) == "DOWN":
            robot.pos_y-=1
        elif self.ACTIONS.get(action) == "LEFT":
            robot.pos_x-=1

    def _newTasksAppear(self):
        samplingSpace = spaces.MultiDiscrete([self._parameters['x_size'], self._parameters['y_size']])
        self._tasks.append(FactoryFloorTask(id_=0, pos_x=samplingSpace.sample()[0]-1, pos_y=samplingSpace.sample()[1]-1))

    def _isActionAllowed(self, robot, action):
        if( self.ACTIONS.get(action) == "UP" and robot.pos_y == self._parameters['y_size']-1 ):
            return False
        if( self.ACTIONS.get(action) == "DOWN" and robot.pos_y == 0 ):
            return False
        if( self.ACTIONS.get(action) == "RIGHT" and robot.pos_x == self._parameters['x_size']-1 ):
            return False
        if( self.ACTIONS.get(action) == "LEFT" and robot.pos_x == 0 ):
            return False

        return True

    def _computePenalty(self):
        penalty = 0
        for task in self._tasks:
            penalty += 1
        return penalty


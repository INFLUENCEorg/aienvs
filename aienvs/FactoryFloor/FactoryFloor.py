import gym
from gym import spaces
from aienvs.FactoryFloor.FactoryFloorRobot import FactoryFloorRobot
from aienvs.FactoryFloor.FactoryFloorTask import FactoryFloorTask
from aienvs.Environment import Env
import numpy as np
from numpy import array
from numpy import vstack
import copy
from random import random
from random import randint


class FactoryFloor(Env):
    """
    The factory floor environment
    """
    DEFAULT_PARAMETERS = {'steps':1000, 
                'n_robots':2, 
                'n_tasks':5, 
                'x_size':10,
                'y_size':15,
                'task_prob':0.9, # P(ACT will succeed)
                'allow_robot_overlap':False,
                'allow_task_overlap':False
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
        self._taskIdCounter=1 # to generate new task ids

        self._robots = []
        while len(self._robots) < self._parameters['n_robots']:
            self._robots.append(FactoryFloorRobot(id_=len(self._robots)))

        self._tasks = []
        samplingSpace = spaces.MultiDiscrete([self._parameters['x_size'], self._parameters['y_size']])
        while len(self._tasks) < self._parameters['n_tasks']:
            self._addTask()

    def step(self, actions:spaces.Dict):
        for robot in self._robots:
            self._applyAction(robot, actions[robot.getId()])

        self._addTask()
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
            pos = task.getPosition()
            bitmapTasks[pos[0], pos[1]]+=1

        return vstack((bitmapRobots, bitmapTasks))

    def _applyAction(self, robot, action):
        """
        robot tries to execute given action.
        @param robot a FactoryFloorRobot
        @param action the ACTION number. If ACT, then the robot executes all
        tasks that are in the tasks list and at the robot's location 
        """
        if not self._isActionAllowed( robot, action ):
            return False
        if random() > self._parameters['task_prob']:
            return False
        
        newpos = pos = robot.getPosition()
        
        if self.ACTIONS.get(action) == "ACT":
            for task in self._tasks:
                if pos == task.getPosition():
                    self._tasks.remove(task)
                    print("removed ",task)
        elif self.ACTIONS.get(action) == "UP":
            newpos=(pos[0],pos[1]+1)
        elif self.ACTIONS.get(action) == "RIGHT":
            newpos=(pos[0]+1,pos[1])
        elif self.ACTIONS.get(action) == "DOWN":
            newpos=(pos[0],pos[1]-1)
        elif self.ACTIONS.get(action) == "LEFT":
            newpos=(pos[0]-1,pos[1])

        # note, because robot occupies its own position,
        # setPosition will not be called if newpos=old pos.
        if self._parameters['allow_robot_overlap'] or not(self.isOccupied(newpos)):
            robot.setPosition(newpos)


    def isOccupied(self,position):
        """
        @param position a tuple (x,y) that must be checked
        @return: true iff a position is occupying position
        """        
        for robot in self._robots:
            if position==robot.getPosition():
                return True
        return False
        

    def _addTask(self):
        """
        Add one new task to the task pool
        """
        if (len(self._tasks) == self._parameters['x_size'] * self._parameters['y_size']):
            return
        #samplingSpace = spaces.MultiDiscrete([self._parameters['x_size'], self._parameters['y_size']])
        while True: # do until newpos is not yet tasked, or task overlap allowed
            newpos = (randint(0,self._parameters['x_size']-1 ),randint(0,self._parameters['y_size']-1 ))
            if self._parameters['allow_task_overlap'] or self._getTask(newpos)==None:
                break;
            
        self._tasks.append(FactoryFloorTask(self._taskIdCounter , newpos))
        self._taskIdCounter+=1


    def _getTask(self, pos:tuple):
        """
        @return task at given position, or None if no task at position
        """
        for task in self._tasks:
            if task.getPosition() == pos:
                return task
        return None
        
        
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

import gym
from gym import spaces
from aienvs.FactoryFloor.FactoryFloorRobot import FactoryFloorRobot
from aienvs.FactoryFloor.FactoryFloorTask import FactoryFloorTask
from aienvs.Environment import Env
import numpy as np
from numpy import array, vstack, ndarray
import copy
import random 
from aienvs.FactoryFloor.Map import Map
from numpy.random import choice as weightedchoice


class FactoryFloor(Env):
    """
    The factory floor environment
    """
    DEFAULT_PARAMETERS = {'steps':1000,
                'robots':[ [3, 4], 'random'],
                # P(ACT will succeed)
                'P_action_succeed':{'LEFT':0.9, 'RIGHT':0.9, 'ACT':0.5, 'UP':0.9, 'DOWN':0.9},
                'P_task_appears':0.99,  # P(new task appears in step) 
                'allow_robot_overlap':False,
                'allow_task_overlap':False,
                'map':['..........',
                       '...8......',
                       '..3.*.....',
                       '....*.5...',
                       '...99999..']
                }

    ACTIONS = {
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
        self._tasks = []
        self._map = Map(self._parameters['map'])
        # use "set" to get rid of weird wrappers
        if set(self._parameters['P_action_succeed'].keys()) != set(FactoryFloor.ACTIONS.values()):
            raise ValueError("P_action_succeed must contain values for all actions")

        self._robots = []
        for pos in self._parameters['robots']:
            if isinstance(pos, list):
                if len(pos) != 2:
                    raise ValueError("position vector must be length 2 but got " + str(pos))
                robot = FactoryFloorRobot(array([pos[0], pos[1]]))  # convert to tuple
            elif pos == 'random':
                robot = FactoryFloorRobot(self._getFreeMapPosition())
            else:
                raise ValueError("Unknown robot position, expected tuple but got " + str(pos))
            self._robots.append(robot)

    def step(self, actions:spaces.Dict):
        for robot in self._robots:
            self._applyAction(robot, actions[robot.getId()])
        if random.random() > self._parameters['P_task_appears']:
            self._addTask()
        global_reward = self._computePenalty()
        done = (self._parameters['steps'] <= self._step)
        obs = self._createBitmap()
        self._step += 1
        
        return obs, global_reward, done, []
    
    def reset(self):
        self._step = 0
        
    def render(self):
        pass  # todo
    
    def close(self):
        pass  # todo

    def seed(self):
        pass  # todo

    def observation_space(self):
        """
        Returns 2 layers: first is for the robot positions, second for the task positions
        """
        return spaces.MultiDiscrete([2, self._map.getWidth(), self._map.getHeight()]) 
 
    def action_space(self):
        return spaces.Dict({robot.getId():spaces.Discrete(len(self.ACTIONS)) for robot in self._robots})

    ########## Private functions ##########################

    def _createBitmap(self):
        bitmapRobots = np.zeros((self._map.getWidth(), self._map.getHeight()))
        bitmapTasks = np.zeros((self._map.getWidth(), self._map.getHeight()))
        for robot in self._robots:
            pos = robot.getPosition()
            bitmapRobots[pos[0], pos[1]] += 1

        for task in self._tasks:
            pos = task.getPosition()
            bitmapTasks[pos[0], pos[1]] += 1

        return vstack((bitmapRobots, bitmapTasks))

    def _applyAction(self, robot, action):
        """
        robot tries to execute given action.
        @param robot a FactoryFloorRobot
        @param action the ACTION number. If ACT, then the robot executes all
        tasks that are in the tasks list and at the robot's location 
        """
        actstring = self.ACTIONS.get(action)
        if random.random() > self._parameters['P_action_succeed'][actstring]:
            return False
        pos = robot.getPosition()
        
        if actstring == "ACT":
            task = self._getTask(pos)
            if task != None:
                self._tasks.remove(task)
                print("removed ", task)
        else:  # move
            newpos = self._newPos(pos, action)
            if self._isFree(newpos):
                robot.setPosition(newpos)
  
    def _newPos(self, pos:ndarray, action):
        """
        @param pos the current (old) position of the robot (numpy array)
        @param action the action to be done in given position
        @return:  what would be the new position (ndarray) if robot did action.
        This does not check any legality of the new position, so the 
        position may run off the map or on a wall.
        """
        newpos = pos
        if self.ACTIONS.get(action) == "UP":
            newpos = pos + [0, 1]
        elif self.ACTIONS.get(action) == "RIGHT":
            newpos = pos + [1, 0]
        elif self.ACTIONS.get(action) == "DOWN":
            newpos = pos + [0, -1]
        elif self.ACTIONS.get(action) == "LEFT":
            newpos = pos + [-1, 0]
        return newpos
    
    def _getFreeMapPosition(self):
        """
        @return:random map position (x,y) that is not occupied by robot or wall.
        """
        while True:
            pos = self._map.getRandomPosition()
            if self._isFree(pos):
                return pos

    def _isRobot(self, position:ndarray):
        """
        @param position a numpy ndarray [x,y] that must be checked
        @return: true iff a robot occupies position
        """        
        for robot in self._robots:
            if (position == robot.getPosition()).all():
                return True
        return False

    def _isFree(self, pos:ndarray):
        """
        @return true iff the given pos has space for a robot,
        so it must be on the map and not on a wall and possibly
        not already containing a robot
        """
        return self._map.isInside(pos) and self._map.get(pos) != "*" \
            and (self._parameters['allow_robot_overlap'] or not(self._isRobot(pos)))
        
    def _addTask(self):
        """
        Add one new task to the task pool
        """
        poslist = self._map.getTaskPositions()
        if len(self._tasks) >= len(poslist):
            return
        # samplingSpace = spaces.MultiDiscrete([self._parameters['x_size'], self._parameters['y_size']])
        while True:  # do until newpos is not yet tasked, or task overlap allowed
            # work around numpy bug when list contains tuples
            i = weightedchoice(list(range(len(poslist))), 1, p=self._map.getTaskWeights())[0]
            newpos = poslist[i]
            if self._parameters['allow_task_overlap'] or self._getTask(newpos) == None:
                break;
            
        self._tasks.append(FactoryFloorTask(newpos))

    def _getTask(self, pos:tuple):
        """
        @return task at given position, or None if no task at position
        """
        for task in self._tasks:
            if (task.getPosition() == pos).all():
                return task
        return None

    def _computePenalty(self):
        penalty = 0
        for task in self._tasks:
            penalty += 1
        return penalty


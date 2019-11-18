import logging
from gym import spaces
from aienvs.Environment import Env
# from numpy import set_printoptions, transpose, zeros
from numpy import array, dstack, ndarray
import copy
from aienvs.GroupingRobots.Robot import Robot
# from random import Random
# from aienvs.FactoryFloor.Map import Map
# from numpy.random import seed as npseed
# from numpy.random import choice as weightedchoice
# import time
import random
# import pdb
# import numbers
from aienvs.gym.CustomObjectSpace import CustomObjectSpace
from aienvs.GroupingRobots.WorldState import WorldState
from aienvs.BasicMap import BasicMap


class GroupingRobots(Env):
    """
    An environment where robots get rewards for grouping.
    The more robots on a single tile, the higher the reward.
    This object is not immutable.
    """
    DEFAULT_PARAMETERS = {'steps':1000,
                'robots':[ {'id': "robot1", 'pos':[3, 4]}, {'id': "robot2", 'pos': 'random'}],  # initial robot positions
                'seed':None,
                'map':['..........',
                       '....***...',
                       '....*.....',
                       '....*..*..',
                       '.......*..']
                }

    def __init__(self, parameters:dict={}):
        """
        @param parameters a dict containing the following keys
        'robots', contains a list of robotinfo objects (see below)
        'seed', contains initial value for random seed, or None
        'map', contains list used to generate BasicMap
        
        robotinfo: a dict containing the following keys:
        'id': unique name (string) of a robot
        'pos': a list with 2 args: initial x and y position, or 'random'
        """
        self._parameters = copy.deepcopy(self.DEFAULT_PARAMETERS)
        self._parameters.update(parameters)

        self.seed(self._parameters['seed'])
        self._state = WorldState({}, BasicMap(self._parameters['map']), self._parameters['steps'])

        for item in self._parameters['robots']:
            pos = item['pos']
            robotId = item['id']
            if isinstance(pos, list):
                if len(pos) != 2:
                    raise ValueError("position vector must be length 2 but got " + str(pos))
                robot = Robot(robotId, array(pos))
            elif pos == 'random':
                robot = Robot(robotId, self._state.getFreeWithoutRobot())
            else:
                raise ValueError("Unknown robot position, expected list but got " + str(type(pos)))
            self._state = self._state.withRobot(robot)
    
        self._actSpace = spaces.Dict({robot.getId():spaces.Discrete(len(self._state.ACTIONS)) for robot in self._state.getRobots()})

    # Override
    def step(self, actions:dict):
        for robot in self._state.robots.values():
            rid = robot.getId()
            if rid in actions.keys():
                self._state = self._state.withAction(robot, actions[rid])
        global_reward = self._state.getReward()
        self._state = self._state.withTeleport().withStep()
        done = (self._parameters['steps'] <= self._state.getSteps())

        return self._state, global_reward, done, []
    
    def reset(self) -> WorldState:
        self.__init__(self._parameters)
        return self._state
        
    def render(self, delay=0.0, overlay=False):
        themap = self._state.getMap().getFullMap()
        # add the robots using the char as indicator
        char = 'R' 
        for robot in self._state.getRobots():
            pos = robot.getPosition()
            oldline = themap[pos[1]]
            oldline = oldline[:pos[0]] + char + oldline[(pos[0] + 1):]
            themap[pos[1]] = oldline
        # print row 0 at the bottom
        print("\n".join(themap.reverse())) 
        
    def close(self):
        pass  

    # Override
    def seed(self, seed):
        # FIXME this is setting global seed, affecting everyone!
        return random.seed(seed)

    def getState(self) -> WorldState:
        return self._state

    @property
    def observation_space(self):
        return CustomObjectSpace(self._state);

    @property
    def action_space(self):
        return self._actSpace


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
from aienvs.GroupingRobots.State import State
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

    ACTIONS = {
        0: "UP",
        1: "DOWN",
        2: "LEFT",
        3: "RIGHT"
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

        self._state = State({}, BasicMap(self._parameters['map']))

        # TODO: remove code duplication
        for item in self._parameters['robots']:
            pos = item['pos']
            robotId = item['id']
            if isinstance(pos, list):
                if len(pos) != 2:
                    raise ValueError("position vector must be length 2 but got " + str(pos))
                robot = Robot(robotId, array(pos))
            elif pos == 'random':
                robot = Robot(robotId, self._state.getFreePosNoRobot())
            else:
                raise ValueError("Unknown robot position, expected list but got " + str(type(pos)))
            self._state = self._state.withRobot(robot)
    
        self._actSpace = spaces.Dict({robotId:spaces.Discrete(len(self.ACTIONS)) for robotId in self._state.robots.keys()})

    # Override
    def step(self, actions:dict):
        if(actions):
            for robot in self._state.robots.values():
                self._applyAction(robot, actions[robot.getId()])
        global_reward = self._state.getReward()
        self._state = self._state.withTeleport();
        self._state = self._state.withStep()
        done = (self._parameters['steps'] <= self._state.getSteps())

        return self._state, global_reward, done, []
    
    def reset(self):
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

    def seed(self, seed):
        random.seed(seed)

    def getState(self) -> State:
        return self._state

    @property
    def observation_space(self):
        return CustomObjectSpace(self._state);

    @property
    def action_space(self):
        return self._actSpace
            
    ########## Getters ###############################
    
    def getMap(self):
        """
        @return: the map of this floor
        """
        return self._state.getMap()
 
    def isPossible(self, robot:Robot, action):
        """
        @param robot a Robot requesting an action
        @param action (integer) the action to be performed
        @return: true iff the action will be possible (can succeed) at this point.
        ACT is considered possible if there is a task at the current position.
        """
        return self.getMap().isFree(self._newPos(robot.getPosition(), action))
        
    def getPossibleActions(self, robot:Robot):
        """
        @return the possible actions for the given robot on the floor
        """
        return [action for action in self.ACTIONS if self.isPossible(robot, action)]

    ########## Private functions ##########################
   
    def _withAction(self, robot, action) -> State:
        """
        robot tries to execute given action.
        @param robot a FactoryFloorRobot
        @param action the ACTION number.
        @return new State if this action would be applied
        """
        pos = robot.getPosition()
        newpos = self._newPos(pos, action)
        if self._isFree(newpos):
            newrobot = Robot(robot.getId(), newpos)
            self._state = self._state.withRobot(newrobot)
  
    def _newPos(self, pos:ndarray, action):
        """
        @param pos the current (old) position of the robot (numpy array)
        @param action the action to be done in given position
        @return:  what would be the new position (ndarray) if robot did action.
        This does not check any legality of the new position, so the 
        position may run off the map or on a wall.
        """
        newpos = pos
        if self.ACTIONS.get(action) == "DOWN":
            newpos = pos + [0, 1]
        elif self.ACTIONS.get(action) == "RIGHT":
            newpos = pos + [1, 0]
        elif self.ACTIONS.get(action) == "UP":
            newpos = pos + [0, -1]
        elif self.ACTIONS.get(action) == "LEFT":
            newpos = pos + [-1, 0]
        return newpos

    def _isRobot(self, position:ndarray):
        """
        @param position a numpy ndarray [x,y] that must be checked
        @return: true iff a robot occupies position
        """        
        for robot in self._state.robots.values():
            if (position == robot.getPosition()).all():
                return True
        return False


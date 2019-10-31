import numpy as np
from aienvs.BasicMap import BasicMap
import copy
from aienvs.GroupingRobots.Robot import Robot
from numpy import array, ndarray, delete, array_equal
from xml.etree.ElementPath import prepare_self
import random
from aienvs.utils import rm, hashf

from typing import TypeVar, Generic


class WorldState:
    """
    The state of the GroupingRobots world.
    This is adding Robot's to the BasicMap.
    Immutable.
    """
    ACTIONS = {
        0: "UP",
        1: "DOWN",
        2: "LEFT",
        3: "RIGHT"
    }   

    def __init__(self, robots:dict, map:BasicMap, steps:int):
        """
        @param robots: dict of the robots (key) and 
        Robot (value) where key = Robot.getId()
        @param map the floor BasicMap, immutable
        @param steps the number of steps taken so far.
        """
        self._robots = robots
        self._map = map
        self._steps = steps

    # see PEP 484: WorldState not yet defined (geez), in that case use ''
    def withRobot(self, robot:Robot) -> 'WorldState':
        """
        @param robot a Robot to be added/updated
        @return:  new state with new robot added to this state, or replaces an 
        existing robot with the same ID with the given one.
        """
        newrobots = self._robots.copy()
        newrobots.update({robot.getId(): robot})
        return WorldState(newrobots, self._map, self._steps)
    
    def withStep(self) -> 'WorldState':
        """
        Returns new state with the step counter incremented
        """
        return WorldState(self._robots, self._map, self._steps + 1)
    
    def withTeleport(self) -> 'WorldState':
        """
        New state where all grouped robots are teleported to random free position
        May throw if there are not enough free positions on the map
        """
        newstate = self
        for robot in self.getGroupedRobots():
            newpos = random.choice(newstate.getFreeWithoutRobot())
            newstate = newstate.withRobot(Robot(robot.getId(), newpos))
            
        return newstate
    
    def withAction(self, robot:Robot, action) -> 'WorldState':
        """
        robot tries to execute given action.
        @param robot a Robot
        @param action the ACTION number.
        @return new State if this action would be applied
        """
        pos = robot.getPosition()
        newpos = self._newPos(pos, action)
        if self._map.isFree(newpos):
            return self.withRobot(Robot(robot.getId(), newpos))
        return self
    
    def getFreeWithoutRobot(self) -> array:
        """
        @return all positions that are free and do not contain robot.
        """
        free = self._map.getMapPositions('.')
        for robot in self._robots.values():
            free = rm(free, robot.getPosition())
        return free
            
    def getGroupedRobots(self) -> set:
        """
        @return set of all robots that are in a group now
        """
        robots = set()
        for robot in self._robots.values():
            for otherrobot in self._robots.values():
                if robot != otherrobot and array_equal(robot.getPosition(), otherrobot.getPosition()):
                    robots.add(robot)
        return robots

    def isPossible(self, robot:Robot, action):
        """
        @param robot a Robot requesting an action
        @param action (integer) the action to be performed
        @return: true iff the new pos is containing free tile '.'.
        """
        return self._map.get(self._newPos(robot.getPosition(), action)) == '.'

    def getPossibleActions(self, robot:Robot):
        """
        @return the possible actions for the given robot on the floor
        """
        return [action for action in self.ACTIONS if self.isPossible(robot, action)]

    def getRobots(self) -> list:  # <Robot>
        """
        @return list of Robots in this world  
        """
        return list(self._robots.values())

    def getMap(self):  # map is immutablke
        return self._map
    
    def getSteps(self):
        """
        @return number of steps taken so far
        """
        return self._steps
    
    def getReward(self) -> int:
        """
        @return reward for current state, which is the sum
        of the rewards of all robots.
        Each robot gets a reward = #robots at its current position -1
        """
        reward = 0
        for robot in self._robots.values():
            reward = reward + len(self._getRobotsAt(robot.getPosition())) - 1
        return reward
            
    def _getRobotsAt(self, pos:ndarray):
        """
        @return all robots at given position
        """
        return [robot for robot in self._state.getRobots() if pos.array_equal(robot.getPosition)]

    def _newPos(self, pos:ndarray, action):
        """
        @param pos the current (old) position of the robot (numpy array)
        @param action the action to be done in given position
        @return:  what would be the new position (ndarray) if robot did action.
        This does not check any legality of the new position, so the 
        position may run off the map or on a wall.
        """
        newpos = pos
        if self.ACTIONS[action] == "DOWN":
            newpos = pos + [0, 1]
        elif self.ACTIONS[action] == "RIGHT":
            newpos = pos + [1, 0]
        elif self.ACTIONS[action] == "UP":
            newpos = pos + [0, -1]
        elif self.ACTIONS[action] == "LEFT":
            newpos = pos + [-1, 0]
        return newpos

    def __eq__(self, other):
        return self._robots == other._robots and self._map == other._map

    def __hash__(self) -> int:
        return hashf(self._robots) + hashf(self._map) + hashf(self._steps)
    

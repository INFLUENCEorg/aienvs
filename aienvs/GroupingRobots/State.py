import numpy as np
from aienvs.BasicMap import BasicMap
import copy

from numpy import array, ndarray
from xml.etree.ElementPath import prepare_self


class State():
    """
    The state of the GroupingRobots world.
    Immutable.
    """

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

    def withRobot(self, robot) -> State:
        newrobots = self.getRobots().update({robot.getId(): robot})
        return State(newrobots, map, self._steps)
    
    def withStep(self) -> State:
        return State(self._robots, self._map, self._steps + 1)
    
    def withTeleport(self) -> State:
        """
        New state where all grouped robots are teleported to random free position
        WARNING this may hang if getFreePosNoRobot hangs.
        """
        newstate=self
        for robot in self.getGroupedRobots():
            newstate = /....
            
    def getGroupedRobots(self):
        """
        @return set of all robots that are in a group now
        """
        robots = set()
        for robot in self._robots.values():
            for otherrobot in self._robot.values():
                if robot!=otherrobot and robot.getPosition().array_equals(otherrobot.getPosition()):
                    robots.add(robot)
        return robots
        

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
    
    def getFreePosNoRobot(self):
        """
        @return a position on the map that has no wall and no robot.
        WARNING this may hang indefinitely if there is no free map
        position.
        """
        while True:
            pos = self._map.getFreeMapPosition()
            if len(self._getRobotsAt(pos)) == 0:
                return pos
            
    def _getRobotsAt(self, pos:ndarray):
        """
        @return all robots at given position
        """
        return [robot for robot in self._state.getRobots() if pos.array_equal(robot.getPosition)]

    def __str__(self):
        """
        for hashing
        """
        return str(encodeStateAsArray(self))

    def __eq__(self, other):
        return self._robots == other._robots and self._map == other._map


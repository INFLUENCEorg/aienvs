# import sys
# import os
# import unittest
import logging
from test.LoggedTestCase import LoggedTestCase
# from aienvs.FactoryFloor.FactoryFloor import FactoryFloor
# import random
# import yaml
from numpy import array, array_equal
# from numpy import ndarray
# from aienvs.Environment import Env
# from aienvs.runners.Episode import Episode
# from aienvs.runners.Experiment import Experiment
# from aienvs.utils import getParameters
from unittest.mock import Mock
# from aienvs.loggers.JsonLogger import JsonLogger
# import io
from aienvs.GroupingRobots.WorldState import WorldState
from aienvs.loggers.PickleLogger import PickleLogger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ROBOT1 = "robot1"
# 3 different "positions"
A = array([1, 1])
B = array([2, 2])
C = array([3, 3])


class testWorldState(LoggedTestCase):
    """
    This is an integration test that also tests aiagents.
    aiagents project must be installed 
    """

    def test_smoke(self):
        WorldState({}, Mock(), 1)
        
    def test_step(self):
        s = WorldState({}, Mock(), 1)
        s = s.withStep()
        self.assertEquals(2, s.getSteps())
    
    def test_withRobot(self):
        s = WorldState({}, Mock(), 1)
        robot = Mock()
        robot.getId = Mock(return_value="robot1")
        s = s.withRobot(robot)
        self.assertEquals([robot], s.getRobots())

    def test_freeWithoutRobot(self):
        env = Mock()
        env.getFreeMapPositions = Mock(return_value=[A, B, C])
        robot = Mock()
        robot.getId = Mock(return_value=ROBOT1)
        robot.getPosition = Mock(return_value=A)
        s = WorldState({ROBOT1:robot}, env, 1)

        free = s.getFreeWithoutRobot()
        self.assertTrue(array_equal([B, C], free))
        

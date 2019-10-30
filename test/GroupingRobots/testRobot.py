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
from aienvs.GroupingRobots.Robot import Robot

# from aienvs.loggers.PickleLogger import PickleLogger
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

ROBOT1 = "robot1"
ROBOT2 = "robot2"
ROBOT3 = "robot3"
# 3 different "positions". Nunpy has its own specialty functions
# so we need to stick with numpy things to get things working...
A = array([1, 1])
B = array([2, 2])
C = array([3, 3])


class testRobot(LoggedTestCase):
    """
    This is an integration test that also tests aiagents.
    aiagents project must be installed 
    """

    def test_smoke(self):
        Robot(ROBOT1, A)
        
    def test_bad_robot(self):
        with self.assertRaises(Exception) as context:
            Robot(ROBOT1, 1)
        self.assertEquals("pos must be numpy array but got <class 'int'>" , str(context.exception))
    
    def test_equals(self):
        self.assertEquals(Robot(ROBOT1, A), Robot(ROBOT1, A))
        self.assertNotEqual(Robot(ROBOT1, A), Robot(ROBOT1, B))
        self.assertNotEqual(Robot(ROBOT1, A), Robot(ROBOT2, A))

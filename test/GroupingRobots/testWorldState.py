# import sys
# import os
# import unittest
import logging
from test.LoggedTestCase import LoggedTestCase
# from aienvs.FactoryFloor.FactoryFloor import FactoryFloor
# import random
# import yaml
# from numpy import array
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

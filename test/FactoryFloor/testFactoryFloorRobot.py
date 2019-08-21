from numpy import array
from test.LoggedTestCase import LoggedTestCase
from aienvs.FactoryFloor.FactoryFloorRobot import FactoryFloorRobot


class FactoryFloorRobotTest(LoggedTestCase):
           
    def test_numpy_array(self):
        FactoryFloorRobot(**{"robotId": "robot", "pos": array([1, 2])})
        

from numpy import array
from LoggedTestCase import LoggedTestCase
from aienvs.FactoryFloor.FactoryFloorRobot import FactoryFloorRobot


class FactoryFloorRobotTest(LoggedTestCase):
    
    def test_smoke_expected(self):
        self.assertRaises(ValueError, FactoryFloorRobot, (1, 2))

    def test_smoke_expected2(self):
        self.assertRaises(ValueError, FactoryFloorRobot, [1, 2])
        
    def test_numpy_array(self):
        FactoryFloorRobot(array([1, 2]))
        

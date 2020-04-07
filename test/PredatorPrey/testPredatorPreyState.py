
from test.LoggedTestCase import LoggedTestCase
from aienvs.PredatorPrey.PredatorPreyState import PredatorPreyState
from aienvs.BasicMap import BasicMap
from aienvs.PredatorPrey.Predator import Predator
from numpy import array

testmap = BasicMap(['...', '...', '...'])
pred1 = Predator('pred1', array([0, 0]), True)
prey1 = Predator('prey1', array([0, 1]), True)


class testPredatorPreyState(LoggedTestCase):

    def testSmoke(self):
        env = PredatorPreyState([], [], testmap, 0, 0, 1)

    def testIsFinal(self):
        env = PredatorPreyState([], [], testmap, 1, 1, 1)
        self.assertTrue(env.isFinal())

    def testGetMap(self):
        env = PredatorPreyState([], [], testmap, 1, 1, 1)
        self.assertEqual(testmap, env.getMap())
    
    def testGetPredators(self):
        env = PredatorPreyState([pred1], [], testmap, 1, 1, 1)
        self.assertEqual([pred1], env.getPredators())
        
    def testGetPreys(self):
        env = PredatorPreyState([], [prey1], testmap, 1, 1, 1)
        self.assertEqual([prey1], env.getPreys())
        
    def testGetObservationMatrix(self):
        env = PredatorPreyState([pred1], [prey1], testmap, 1, 1, 1)
        self.assertEqual({'pred1':[ \
            [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], \
            [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]], \
            [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0]] \
            ]}, env.getObservationMatrix())

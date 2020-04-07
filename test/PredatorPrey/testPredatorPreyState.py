
from test.LoggedTestCase import LoggedTestCase
from aienvs.PredatorPrey.PredatorPreyState import PredatorPreyState
from aienvs.BasicMap import BasicMap
from aienvs.PredatorPrey.Predator import Predator
from numpy import array

testmap = BasicMap(['...', '...', '...'])
pred1 = Predator('pred1', array([0, 0]), True)
pred2 = Predator('pred2', array([1, 2]), True)
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
    
    def testIsPredatorAt(self):
        env = PredatorPreyState([pred1, pred2], [prey1], testmap, 1, 1, 1)
        self.assertTrue(env.isPredatorAt(pred1.getPosition()))
        self.assertTrue(env.isPredatorAt(pred2.getPosition()))
        self.assertFalse(env.isPredatorAt(prey1.getPosition()))
        self.assertFalse(env.isPredatorAt(array([1, 1])))
        
    def testIsPreyAt(self):
        env = PredatorPreyState([pred1, pred2], [prey1], testmap, 1, 1, 1)
        self.assertFalse(env.isPreyAt(pred1.getPosition()))
        self.assertFalse(env.isPreyAt(pred2.getPosition()))
        self.assertTrue(env.isPreyAt(prey1.getPosition()))
        self.assertFalse(env.isPreyAt(array([1, 1])))

    def testGetObservationMatrix(self):
        env = PredatorPreyState([pred1], [prey1], testmap, 1, 1, 1)
        self.assertEqual({'pred1':[ \
            [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], \
            [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]], \
            [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0]] \
            ]}, env.getObservationMatrix())
    
    def testAdjacentPreds(self):
        env = PredatorPreyState([pred1, pred2], [prey1], testmap, 1, 1, 1)
        self.assertEquals([pred1], env.getAdjacentPredators(array([0, 1])))
        self.assertEquals([pred2], env.getAdjacentPredators(array([1, 1])))
        self.assertEquals([], env.getAdjacentPredators(array([2, 0])))



from test.LoggedTestCase import LoggedTestCase
from aienvs.PredatorPrey.PredatorPreyState import PredatorPreyState
from aienvs.BasicMap import BasicMap
from aienvs.PredatorPrey.Predator import Predator
from numpy import array

testmap = BasicMap(['...', '...', '...'])
pred1 = Predator('pred1', array([0, 0]), True)
pred2 = Predator('pred2', array([1, 2]), True)
pred3 = Predator('pred2', array([1, 1]), True)
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

    def testWithCatchOk(self):
        env = PredatorPreyState([pred1, pred3], [prey1], testmap, 1, 1, 2)
        env1 = env.withCatch(prey1, pred1, pred3)
        self.assertEqual([], env1.getPredators())
        self.assertEqual([], env1.getPreys())
        self.assertEqual(11, env1.getReward())  # 10 added to existing reward 1

    def testWithCatchBlockedByFinal(self):
        env = PredatorPreyState([pred1, pred3], [prey1], testmap, 1, 1, 1)
        self.assertTrue(env.isFinal())
        env1 = env.withCatch(prey1, pred1, pred3)
        self.assertEqual(env, env1)

    def testWithReward(self):
        env = PredatorPreyState([pred1, pred2], [prey1], testmap, 1, 1, 2)
        env1 = env.withReward(-0.5)
        self.assertEqual(0.5, env1.getReward())  

    def testWithStep(self):
        env = PredatorPreyState([pred1, pred2], [prey1], testmap, 1, 1, 2)
        env1 = env.withStep(pred1, 1)  # east
        self.assertEqual(str(array([1, 0])), str(env1.getPredators()[0].getPosition()))

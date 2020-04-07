from test.LoggedTestCase import LoggedTestCase
from numpy import array
from aienvs.PredatorPrey.Predator import Predator


class testPredator(LoggedTestCase):
    """
    We test predator instead of MovableItemOnMap so that 
    we also test inheritance.
    """

    def testSmoke(self):
        Predator('pred1', array([1, 1]), True)

    def testStep(self):
        pos = array([1, 1])
        pred = Predator('pred1', pos, True)
        pred1 = pred.withStep(0)  # north
        self.assertEqual(str(pos), str(pred.getPosition()))
        self.assertEqual(str(pos + array([0, 1])), str(pred1.getPosition()))

    def testActive(self):
        self.assertTrue(Predator('pred1', array([1, 1]), True).isActive())

    def testAdjacent(self):
        p = Predator('pred1', array([1, 1]), True)
        self.assertTrue(p.isAdjacent(array([0, 1])))
        self.assertTrue(p.isAdjacent(array([1, 0])))
        self.assertTrue(p.isAdjacent(array([2, 1])))
        self.assertTrue(p.isAdjacent(array([1, 2])))
        self.assertFalse(p.isAdjacent(array([0, 0])))
        self.assertFalse(p.isAdjacent(array([10, 0])))
        self.assertFalse(p.isAdjacent(array([-1, 1])))
                

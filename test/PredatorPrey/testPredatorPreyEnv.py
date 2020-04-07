from test.LoggedTestCase import LoggedTestCase
from aienvs.PredatorPrey.PredatorPreyState import PredatorPreyState
from aienvs.BasicMap import BasicMap
from aienvs.PredatorPrey.Predator import Predator
from numpy import array
from aienvs.PredatorPrey.PredatorPreyEnv import PredatorPreyEnv


class testPredatorPreyEnv(LoggedTestCase):
    """
    PredatorPreyEnv is harder to test because it's mutable.
    But most tests are already done on state.
    """

    def testSmoke(self):
        PredatorPreyEnv()

    def testStep(self):
        env = PredatorPreyEnv()
        env.step({'predator1': 0, 'predator2': 0})  # both North
        # that mutates env into a new env. Check positions
        self.assertEqual(str(array([3, 5])), str(env.getState().getPredators()[0].getPosition()))
        self.assertEqual(str(array([7, 3])), str(env.getState().getPredators()[1].getPosition()))
    
    def testRenderSmoke(self):
        env = PredatorPreyEnv()
        env.render()
        env.step({'predator1': 0, 'predator2': 0})  # both North
        print("both predators move north")
        env.render()

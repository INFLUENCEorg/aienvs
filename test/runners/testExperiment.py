from aienvs.listener.DefaultListenable import DefaultListenable
from test.LoggedTestCase import LoggedTestCase
from unittest.mock import Mock
from aienvs.runners.Experiment import Experiment


class test_Experiment(LoggedTestCase):

    def testRun1step(self):
        agent = Mock()
        env = Mock()
        # each episode succeeds in step 1
        env.step = Mock(return_value=('observation', 3.0, True, {}))
        firstAction = Mock()
        exp = Experiment(agent, env, 100, None, False, 0)
        result, interval = exp.run()
        
        self.assertEqual(3.0, result.mean)
 
    def testRun3steps(self):
        agent = Mock()
        env = Mock()

        env.step = Mock()
        # each episode succeeds after 3 steps, then restart 10*
        env.step.side_effect = [('observation1', 3.0, False, {}), ('observation2', 4.0, False, {}), ('observation3', 5.0, True, {})] * 10
        firstAction = Mock()
        exp = Experiment(agent, env, 30, None, False, 0)
        result, interval = exp.run()
        # each episode has reward 12
        self.assertEqual(12.0 , result.mean)
        
    def testListener(self):
        agent = Mock()
        env = Mock()
        env.step = Mock(return_value=('observation', 3.0, True, {}))
        firstAction = Mock()
        exp = Experiment(agent, env, 30, None, False, 0)
        
        listener = Mock()
        exp.addListener(listener)
        result = exp.run()
        # check we got 30 callbacks
        self.assertEquals(30, len(listener.notifyChange.mock_calls))

from aienvs.listener.DefaultListenable import DefaultListenable
from test.LoggedTestCase import LoggedTestCase
from unittest.mock import Mock
from aienvs.runners.Episode import Episode


class testEpisode(LoggedTestCase):

    def testRun1step(self):
        agent = Mock()
        env = Mock()
        env.step = Mock(return_value=('observation', 3.0, True, {}))
        firstAction = Mock()
        episode = Episode(agent, env, firstAction, False, 0)
        result = episode.run()
        
        self.assertEqual((1, 3.0), result)

    def testMock(self):
        env = Mock()
        env.step = Mock(return_value=[1, 2, 3])
        print (env.step('a'))
        print (env.step('b'))
    
    def testRun3steps(self):
        agent = Mock()
        env = Mock()

        env.step = Mock(return_value=[('observation1', 3.0, False, {}), ('observation2', 4.0, False, {}), ('observation3', 5.0, True, {})])
        firstAction = Mock()
        episode = Episode(agent, env, firstAction, False, 0)
        result = episode.run()
        
        self.assertEqual((3, 5.0), result)
        # if you get not enough values to unpack then 
        # the Episode runner did not halt when env said 
        # it was done.
        

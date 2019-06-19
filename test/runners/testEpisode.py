from aienvs.listener.DefaultListenable import DefaultListenable
from test.LoggedTestCase import LoggedTestCase
from unittest.mock import Mock
from aienvs.runners.Episode import Episode


class testEpisode(LoggedTestCase):

    def testRun(self):
        agent = Mock()
        env = Mock()

        def dostep(self):
            return 'observation', 3.0, True, {}

        env.step = dostep
        firstAction = Mock()
        episode = Episode(agent, env, firstAction, False, 0)
        result = episode.run()
        
        self.assertEqual((1, 3.0), result)
        

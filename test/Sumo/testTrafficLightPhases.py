from aienvs.Sumo.TrafficLightPhases import TrafficLightPhases
from test.LoggedTestCase import LoggedTestCase
import logging
from io import StringIO

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class testGym(LoggedTestCase):
        
    def test_load(self):
        res = TrafficLightPhases('test.tll.xml')
        self.assertEqual(['0', '1'], res.getIntersectionIds())
        self.assertEqual([0, 1], res.getPhases('1'))
        self.assertEqual("GGggrrrrGGggrrrr", res.getPhase("0", 0))

    
if __name__ == '__main__':
    unittest.main()

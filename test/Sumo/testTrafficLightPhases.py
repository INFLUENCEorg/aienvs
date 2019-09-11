from aienvs.Sumo.TrafficLightPhases import TrafficLightPhases
from test.LoggedTestCase import LoggedTestCase
import logging
from io import StringIO
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class testGym(LoggedTestCase):
        
    def test_load(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "test.tll.xml")

        res = TrafficLightPhases(filename)
        self.assertEqual(['0', '1'], res.getIntersectionIds())
        self.assertEqual(1, res.getNrPhases('1'))  # one has yellow
        self.assertEqual(4, res.getNrPhases('0'))  # 4 of 8 have yellow
        self.assertEqual("GGggrrrrGGggrrrr", res.getPhase("0", 0))

    
if __name__ == '__main__':
    unittest.main()

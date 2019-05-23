import unittest
import logging
from LoggedTestCase import LoggedTestCase
from aienvs.FactoryFloor.FactoryFloor import FactoryFloor
import random
from numpy import array

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class testFactoryFloor(LoggedTestCase):
        
    def test_smoke(self):
        env = FactoryFloor()
        
    def test_simplerun(self):
        env = FactoryFloor()
        env.reset()
        action_space = env.action_space()

        done = False
        while not done:
            actions = action_space.sample()
            observation, reward, done, info = env.step(actions)

    def test_importParametersFromYaml(self):
        import yaml
        with open("test/resources/settings.yaml", 'r') as stream:
                settings = yaml.safe_load(stream)
                print ("succesfully read settings", settings)
                # and proof that the settings are good, quick hack
                env = FactoryFloor(settings)           
    
    def test_getPart(self):
        env = FactoryFloor()
        floor = env.getPart(array([[2, 1], [4, 4]]))
        self.assertEquals(['.8.', '3.*', '..*', '.99'], floor.getMap().getFullMap())                        
        self.assertEquals(.99 * (8 + 3 + 9 + 9) / (8 + 3 + 5 + 9 + 9 + 9 + 9 + 9), floor.getMap().getTaskProbability())

        
if __name__ == '__main__':
    unittest.main()

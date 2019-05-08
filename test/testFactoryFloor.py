import unittest
import logging
from LoggedTestCase import LoggedTestCase
from aienvs.FactoryFloor.FactoryFloor import FactoryFloor
import random

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class testFactoryFloorAdapter(LoggedTestCase):
        
    def test_smoke(self):
        env = FactoryFloor()
        env.reset()
        action_space=env.action_space

        done=False
        while not done:
            actions = action_space.sample()
            observation, reward, done, info=env.step(actions)
            print(observation)
            print(actions[0])
            print(actions[1])
        
if __name__ == '__main__':
    unittest.main()

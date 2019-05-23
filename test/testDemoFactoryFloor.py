import unittest
import logging
from LoggedTestCase import LoggedTestCase
from aienvs.FactoryFloor.FactoryFloor import FactoryFloor
import random

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class testFactoryFloor(LoggedTestCase):
        
    def test_demo(self):
        env = FactoryFloor()
        env.reset()
        action_space = env.action_space()

        done = False
        while not done:
            actions = action_space.sample()
            observation, reward, done, info = env.step(actions)
            # transpose because  observation is a matrix. 
            # matrix rendering has first 
            # index (x) in the vertical direction.
            # after swap, y stil goes down however.
            print(observation.transpose())
            print(actions)
            print (reward)

        
if __name__ == '__main__':
    unittest.main()

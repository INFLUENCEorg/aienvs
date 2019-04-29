import unittest
from aienvs.FactoryFloorAdapter import FactoryFloorAdapter
import random

class testFactoryFloorAdapter(unittest.TestCase):
        
    def test_smoke(self):
        env = FactoryFloorAdapter()
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

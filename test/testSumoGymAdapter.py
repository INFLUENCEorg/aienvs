import unittest
from  SumoGymAdapter import SumoGymAdapter
import random

class testGymEnvAdapter(unittest.TestCase):
        
    def test_smoke(self):
        env = SumoGymAdapter()
        env.reset()
        for _ in range(1000):
            env.render()
            result = env.step(env.action_space.sample())
        env.close()
        print(result)
    

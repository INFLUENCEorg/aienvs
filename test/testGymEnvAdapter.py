import unittest
from  GymEnvAdapter import  GymEnvAdapter
import random

class testGymEnvAdapter(unittest.TestCase):
        
    def test_smoke(self):
        env = GymEnvAdapter('Breakout-v0')
        actions=env.getActionMap()[0]
        env.initialize({'render':True})
        result={'done':False}
        while not result['done']:
            result=env.step({0:random.choice(actions)})
        env.close()
        print(result)
        
    

import unittest
import aienvs
from aienvs.SumoGymAdapter import SumoGymAdapter

class testSumoGymAdapter(unittest.TestCase):
        
    def test_smoke(self):
        env = SumoGymAdapter()
        env.reset()
        for _ in range(1000):
            env.render()
            result = env.step(env.action_space.sample())
        env.close()
        print(result)

if __name__ == '__main__':
    unittest.main()
    

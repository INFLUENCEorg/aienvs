import unittest
import aienvs
import logging
import yaml
import sys
from aienvs.SumoGymAdapter import SumoGymAdapter

class testSumoGymAdapter(unittest.TestCase):
    
    def test_new_traffic(self):
        with open("configs/new_traffic_loop_ppo.yaml", 'r') as stream:
            try:
                parameters=yaml.safe_load(stream)['parameters']
            except yaml.YAMLError as exc:
                print(exc)

        env = SumoGymAdapter(parameters)
        for i in range(1000):
            logging.info("Step " + str(i))
            result = env.step(env.action_space.sample())
        env.close()
        
    def test_smoke(self):
        env = SumoGymAdapter()
        for _ in range(1000):
            result = env.step(env.action_space.sample())
        env.close()
        logging.info(result)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    logging.info("Logging initialized")
    unittest.main()
    

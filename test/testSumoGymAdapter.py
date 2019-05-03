import unittest
import aienvs
import logging
import yaml
import sys
from LoggedTestCase import LoggedTestCase
from aienvs.SumoGymAdapter import SumoGymAdapter

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class testSumoGymAdapter(LoggedTestCase):
    
    def test_new_traffic(self):
        logging.info("Starting test_new_traffic")
        with open("configs/new_traffic_loop_ppo.yaml", 'r') as stream:
            try:
                parameters=yaml.safe_load(stream)['parameters']
            except yaml.YAMLError as exc:
                print(exc)

        env = SumoGymAdapter(parameters)
        for i in range(1000):
            logging.debug("Step " + str(i))
            result = env.step(env.action_space.sample())
        env.close()
        
    def test_smoke(self):
        logging.info("Starting test_smoke")
        env = SumoGymAdapter(parameters={'generate_conf':False})

        for _ in range(1000):
            result = env.step(env.action_space.sample())
        env.close()
        logging.info(result)


if __name__ == '__main__':
    unittest.main()
    

import unittest
import aienvs
import aiagents
import logging
import yaml
import sys
from LoggedTestCase import LoggedTestCase
from aienvs.Sumo.SumoGymAdapter import SumoGymAdapter

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
        
    def test_smoke(self):
        logging.info("Starting test_smoke")
        env = SumoGymAdapter(parameters={'generate_conf':False, 'gui': False})
        
        done = False
        i=0
 
        while(not done):
            logging.debug("Step " + str(i))
            i+=1
            obs, global_reward, done, info = env.step(env.action_space.sample())

    def test_random_agent(self):
        logging.info("Starting test_random_agent")
        env = SumoGymAdapter(parameters={'generate_conf':False, 'gui':False})

        for _ in range(1000):
            result = env.step(env.action_space.sample())


if __name__ == '__main__':
    unittest.main()
    

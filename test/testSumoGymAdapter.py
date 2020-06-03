import sys
import os
import unittest
import logging
import yaml
from test.LoggedTestCase import LoggedTestCase
from aienvs.Sumo.SumoGymAdapter import SumoGymAdapter
from aienvs.runners.Experiment import Experiment

logger = logging.getLogger()
logger.setLevel(50)


class testSumoGymAdapter(LoggedTestCase):
    """
    This is an integration test that also tests aiagents.
    aiagents project must be installed 
    """

    def test_smoke(self):
        logging.info("Starting test_smoke")
        env = SumoGymAdapter(parameters={'generate_conf':False, 'gui': False, 'maxConnectRetries':2})
        env.reset()
        
        done = False
        i = 0
 
        while (not done) and i < 10:
            logging.debug("Step " + str(i))
            i += 1
            obs, global_reward, done, info = env.step(env.action_space.sample())
 
    def test_new_traffic(self):
        self._runPpoLoop()

    def test_runTwice(self):
        """
        Tests that we can open SumoGymAdapter twice #43.
        """
        self._runPpoLoop()
        self._runPpoLoop()
    
    def _runPpoLoop(self):
        parameters = self._get_params()
        env = SumoGymAdapter(parameters)
        env.reset()

        for i in range(1000):
            logging.debug("Step " + str(i))
            result = env.step(env.action_space.sample())
        # env.close() #DO WE NEED THIS?
    
    def _get_params(self) -> dict:
        """
        @return new_traffic_loop_ppo parameters
        """
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "configs/new_traffic_loop_ppo.yaml")

        with open(filename, 'r') as stream:
            try:
                parameters = yaml.safe_load(stream)['parameters']
            except yaml.YAMLError as exc:
                print(exc)
        return parameters
 
        
if __name__ == '__main__':
    unittest.main()
    

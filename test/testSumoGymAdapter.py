import sys
import os
import unittest
import aienvs
from aiagents.multi.BasicComplexAgent import BasicComplexAgent
from aiagents.single.RandomAgent import RandomAgent
from aiagents.single.PPO.PPOAgent import PPOAgent
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

    def test_new_traffic(self):
        logging.info("Starting test_new_traffic")
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "configs/new_traffic_loop_ppo.yaml")

        with open(filename, 'r') as stream:
            try:
                parameters = yaml.safe_load(stream)['parameters']
            except yaml.YAMLError as exc:
                print(exc)

        env = SumoGymAdapter(parameters)
        env.reset()

        for i in range(1000):
            logging.debug("Step " + str(i))
            result = env.step(env.action_space.sample())
        
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

    def test_random_agent(self):
        logging.info("Starting test_random_agent")
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "configs/new_traffic_loop_ppo.yaml")

        with open(filename, 'r') as stream:
            try:
                parameters = yaml.safe_load(stream)['parameters']
            except yaml.YAMLError as exc:
                logging.error(exc)

        env = SumoGymAdapter(parameters)
        env.reset()

        randomAgents = []
        for intersectionId in env.action_space.spaces.keys():
            randomAgents.append(RandomAgent(intersectionId, env))

        complexAgent = BasicComplexAgent(randomAgents)
        experiment = Experiment(complexAgent, env, parameters['max_steps'])
        experiment.run()

    def test_PPO_agent(self):
        logging.info("Starting test_PPO_agent")
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "configs/new_traffic_loop_ppo.yaml")

        with open(filename, 'r') as stream:
            try:
                parameters = yaml.safe_load(stream)['parameters']
            except yaml.YAMLError as exc:
                logging.error(exc)

        env = SumoGymAdapter(parameters)
        env.reset()

        PPOAgents = []
        for intersectionId in env.action_space.spaces.keys():
            PPOAgents.append(PPOAgent(intersectionId, env, parameters))

        complexAgent = BasicComplexAgent(PPOAgents)
        experiment = Experiment(complexAgent, env, parameters['max_steps'])
        experiment.run()

        
if __name__ == '__main__':
    unittest.main()
    

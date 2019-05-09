import unittest
import aienvs
from aiagents.multi.ComplexAgentComponent import ComplexAgentComponent
from aiagents.single.RandomAgent import RandomAgent
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
        env = SumoGymAdapter(parameters={'generate_conf':False, 'gui': False})

        randomAgents = []
        for intersectionId in env.action_space.spaces.keys():
            randomAgents.append(RandomAgent(intersectionId, env.action_space.spaces.get(intersectionId)))

        complexAgent=ComplexAgentComponent(randomAgents)

        for _ in range(1000):
            actions = complexAgent.select_actions()
            obs, global_reward, done, info = env.step(actions)
            complexAgent.observe(obs)

        env.close()

    def test_PPO_agent(self):
        logging.info("Starting test_PPO_agent")
        env = SumoGymAdapter(parameters={'generate_conf':False, 'gui': False})

        ppoAgents = []
        for intersectionId in env.action_space.spaces.keys():
            ppoAgents.append(PPOAgent(intersectionId, env.action_space.spaces.get(intersectionId)))

        complexAgent=ComplexAgentComponent(PPOAgents)

        for _ in range(1000):
            actions = complexAgent.select_actions()
            obs, global_reward, done, info = env.step(actions)
            complexAgent.observe(obs)
        

if __name__ == '__main__':
    unittest.main()
    

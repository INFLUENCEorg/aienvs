import sys
import unittest
import aienvs
from aiagents.multi.ComplexAgentComponent import ComplexAgentComponent
from aiagents.single.RandomAgent import RandomAgent
from aiagents.single.PPO.PPOAgent import PPOAgent
import logging
import yaml
from LoggedTestCase import LoggedTestCase
from aienvs.Sumo.SumoGymAdapter import SumoGymAdapter

logger = logging.getLogger()
logger.setLevel(50)


class testSumoGymAdapter(LoggedTestCase):
    """
    This is an integration test that also tests aiagents.
    aiagents project must be installed 
    """

    def test_new_traffic(self):
        logging.info("Starting test_new_traffic")
        with open("configs/new_traffic_loop_ppo.yaml", 'r') as stream:
            try:
                parameters = yaml.safe_load(stream)['parameters']
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
        i = 0
 
        while(not done):
            logging.debug("Step " + str(i))
            i += 1
            obs, global_reward, done, info = env.step(env.action_space.sample())

    def test_random_agent(self):
        logging.info("Starting test_random_agent")
        with open("configs/new_traffic_loop_ppo.yaml", 'r') as stream:
            try:
                parameters = yaml.safe_load(stream)['parameters']
            except yaml.YAMLError as exc:
                logging.error(exc)

        env = SumoGymAdapter(parameters)

        randomAgents = []
        for intersectionId in env.action_space.spaces.keys():
            randomAgents.append(RandomAgent(intersectionId, env.action_space.spaces.get(intersectionId)))

        complexAgent = ComplexAgentComponent(randomAgents)
 
        steps = 0
        episode = 0
        while steps < parameters["max_steps"]:
            # actions=env.action_space.sample()
            actions = {'0': 0}
            print(actions)
            env.reset()
            done = False
            cumulative_reward = 0

            while not done:
                obs, global_reward, done, info = env.step(actions)
                complexAgent.observe(obs, global_reward, done)
                actions = complexAgent.select_actions()
                # rendering the part of the image
                # env.render()
                steps += 1
                cumulative_reward += global_reward

            episode += 1
            print("Episode " + str(episode) + " cumulative reward" + str(cumulative_reward))
                
        env.close()

    def test_PPO_agent(self):
        logging.info("Starting test_PPO_agent")

        with open("test/configs/new_traffic_loop_ppo.yaml", 'r') as stream:
            try:
                parameters = yaml.safe_load(stream)['parameters']
            except yaml.YAMLError as exc:
                logging.error(exc)

        env = SumoGymAdapter(parameters)
        PPOAgents = []
        for intersectionId in env.action_space.spaces.keys():
            PPOAgents.append(PPOAgent(parameters, env.observation_space, env.action_space.spaces.get(intersectionId), intersectionId))

        complexAgent = ComplexAgentComponent(PPOAgents)
        steps = 0
        episode = 0

        while steps < parameters["max_steps"]:
            # actions=env.action_space.sample()
            actions = {'0': 0}
            print(actions)
            env.reset()
            done = False
            cumulative_reward = 0

            while not done:
                obs, global_reward, done, info = env.step(actions)
                complexAgent.observe(obs, global_reward, done)
                actions = complexAgent.select_actions()
                # rendering the part of the image
                # env.render()
                steps += 1
                cumulative_reward += global_reward

            episode += 1
            print("Episode " + str(episode) + " cumulative reward" + str(cumulative_reward))

        
if __name__ == '__main__':
    unittest.main()
    

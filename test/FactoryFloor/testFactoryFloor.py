import sys
import os
import unittest
import logging
from test.LoggedTestCase import LoggedTestCase
from aienvs.FactoryFloor.FactoryFloor import FactoryFloor
from aiagents.single.PPO.PPOAgent import PPOAgent
from aiagents.single.RandomAgent import RandomAgent
from aiagents.single.mcts.mctsAgent import mctsAgent
from aiagents.AgentComponent import AgentComponent
from aiagents.multi.ComplexAgentComponent import ComplexAgentComponent
import random
import yaml
from numpy import array
from numpy import ndarray
from aienvs.Environment import Env
from aienvs.runners.Episode import Episode
from aienvs.runners.Experiment import Experiment
from aienvs.utils import getParameters
from unittest.mock import Mock
from aienvs.loggers.JsonLogger import JsonLogger
import io
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class testFactoryFloor(LoggedTestCase):
    """
    This is an integration test that also tests aiagents.
    aiagents project must be installed 
    """

    def test_smoke(self):
        env = FactoryFloor()
        
    def test_simplerun(self):
        env = FactoryFloor()
        env.reset()
        action_space = env.action_space

        done = False
        while not done:
            actions = action_space.sample()
            observation, reward, done, info = env.step(actions)

    def test_importParametersFromYaml(self):
        with open("test/resources/settings.yaml", 'r') as stream:
                settings = yaml.safe_load(stream)
                print ("succesfully read settings", settings)
                # and proof that the settings are good, quick hack
                env = FactoryFloor(settings)           
    
    def test_getPart(self):
        env = FactoryFloor()
        floor = env.getPart(array([[2, 1], [4, 4]]))
        self.assertEquals(['.8.', '3.*', '..*', '.99'], floor.getMap().getFullMap())                        
        self.assertEquals(.99 * (8 + 3 + 9 + 9) / (8 + 3 + 5 + 9 + 9 + 9 + 9 + 9), floor.getMap().getTaskProbability())

    def test_seed(self):
        """
        we test that we are really having deterministic behaviour 
        """        
        env = FactoryFloor({'seed':42})
        # convert to string as array needs equalsAll which is 
        # not supported by assertEquals FAIK
        self.assertEquals("[4 1]", str(env._getFreeMapPosition()))
        self.assertEquals("[3 1]", str(env._getFreeMapPosition()))
        self.assertEquals("[1 4]", str(env._getFreeMapPosition()))

    def test_mcts_agent(self):
        """
        Really a smoketest/demo how to run an agent
        """
        logging.info("Starting test_mcts_agent")
        logoutput = io.StringIO("episode output log")
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "../configs/factory_floor_simple.yaml")
        parameters = getParameters(filename)
        env = FactoryFloor(parameters)

        mctsAgents = []
        for robotId in env.action_space.spaces.keys():
            mctsAgents.append(mctsAgent(agentId=robotId, environment=env, timeLimit=None, iterationLimit=5000))

        complexAgent = ComplexAgentComponent(mctsAgents)

        episode = Episode(complexAgent, env, None, render=True)
        episode.addListener(JsonLogger(logoutput))
        episode.run()
        print(logoutput.getvalue())

    def est_random_agent(self):
        logging.info("Starting test random agent")
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "../configs/factory_floor.yaml")
        parameters = getParameters(filename)

        env = FactoryFloor(parameters)
        randomAgents = []
        for robotId in env.action_space.spaces.keys():
            randomAgents.append(RandomAgent(robotId, env.action_space.spaces.get(robotId)))

        complexAgent = ComplexAgentComponent(randomAgents)
        steps = 0

        Experiment(complexAgent, env, 1000, True).run()

    def test_PPO_agent(self):
        logging.info("Starting test PPO agent")
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "../configs/factory_floor.yaml")
        parameters = getParameters(filename)

        env = FactoryFloor(parameters)
        PPOAgents = []
        for robotId in env.action_space.spaces.keys():
            PPOAgents.append(PPOAgent(parameters, env.observation_space, env.action_space.spaces.get(robotId), robotId))

        complexAgent = ComplexAgentComponent(PPOAgents)
        steps = 0

        while steps < parameters["max_steps"]:
            steps += Episode(complexAgent, env, env.action_space.sample()).run()
        

if __name__ == '__main__':
    unittest.main()

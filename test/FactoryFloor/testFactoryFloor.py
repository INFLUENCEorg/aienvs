import sys
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
from unittest.mock import Mock

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
        import yaml
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
        logging.info("Starting test_mcts_agent")
        parameters = self._get_parameters("test/configs/factory_floor_simple.yaml")
        env = FactoryFloor(parameters)
        env.reset()

        mctsAgents = []
        for robotId in env.action_space.spaces.keys():
            mctsAgents.append(mctsAgent(agentId=robotId, environment=env, timeLimit=None, iterationLimit=5000))

        complexAgent = ComplexAgentComponent(mctsAgents)

        env.render(delay=0.0, overlay=False)
        self._loopTillDone(complexAgent, env, None)

    def test_random_agent(self):
        logging.info("Starting test_PPO_agent")
        parameters = self._get_parameters("test/configs/factory_floor.yaml")

        env = FactoryFloor(parameters)
        randomAgents = []
        for robotId in env.action_space.spaces.keys():
            randomAgents.append(RandomAgent(robotId, env.action_space.spaces.get(robotId)))

        complexAgent = ComplexAgentComponent(randomAgents)
        steps = 0

        while steps < parameters["max_steps"]:
            steps += self._loopTillDone(complexAgent, env, env.action_space.sample(), True)

    def test_PPO_agent(self):
        logging.info("Starting test_PPO_agent")
        parameters = self._get_parameters("test/configs/factory_floor.yaml")

        env = FactoryFloor(parameters)
        PPOAgents = []
        for robotId in env.action_space.spaces.keys():
            PPOAgents.append(PPOAgent(parameters, env.observation_space, env.action_space.spaces.get(robotId), robotId))

        complexAgent = ComplexAgentComponent(PPOAgents)
        steps = 0

        while steps < parameters["max_steps"]:
            steps += self._loopTillDone(complexAgent, env, env.action_space.sample())
    
    def test_notification(self):
        parameters = self._get_parameters("test/configs/factory_floor.yaml")
        env = FactoryFloor(parameters)
        l = Mock()
        env.addListener(l)
        env.step(None)
        l.notifyChange.assert_called_with({'steps':1, 'reward':-2})
        
    ################# PRIVATE UTIL FUNCS #####################
    def _runExperiment(self, agent:AgentComponent, env: Env, maxSteps:int, render:bool=False):
        """
        Resets env. Loop env.step and agent.select_actions() until number of steps have been made.
        If an env is done before the number of steps have been reached, the env is reset.
        @param agent an AgentComponent holding an agent
        @param env the openai gym Env that we are running in
        @param render True iff environment must be rendered each step.
        @return the number of steps it took to reach done state
        """
        steps = 0
        while steps < maxSteps:
            steps += self._loopTillDone(agent, env, None)
                
    def _loopTillDone(self, agent:AgentComponent, env: Env, firstActions:ndarray, render:bool=False):
        """
        Resets env. Loop env.step and agent.select_actions() until env is done.
        @param agent an AgentComponent holding an agent
        @param env the openai gym Env that we are running in
        @param firstActions the actions for the first step to be taken by agent, encoded as an ndarray as usual in gym environments
        @param render True iff environment must be rendered each step.
        @return the number of steps it took to reach done state
        """
        actions = firstActions
        env.reset()
        done = False
        steps = 0

        while not done:
            obs, global_reward, done, info = env.step(actions)
            agent.observe(obs, global_reward, done)
            actions = agent.select_actions()
            if render:
                env.render(delay=0)
            steps += 1

        return steps

    def _get_parameters(self, filename:str) -> dict:
        """
        @param filename yaml file
        @return: dictionary with parameters in given (yaml) file
        """
        with open(filename, 'r') as stream:
            try:
                parameters = yaml.safe_load(stream)['parameters']
            except yaml.YAMLError as exc:
                logging.error(exc)
        return parameters

        
if __name__ == '__main__':
    unittest.main()

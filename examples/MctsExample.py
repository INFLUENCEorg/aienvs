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
from aienvs.loggers.PickleLogger import PickleLogger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def main():
    """
    Demo how to run an agent
    """
    logging.info("Starting example MCTS agent")
    logoutput = io.StringIO("episode output log")
    logoutputpickle = io.BytesIO()
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "../test/configs/factory_floor_simple.yaml")
    parameters = getParameters(filename)
    env = FactoryFloor(parameters)

    mctsAgents = []
    for robotId in env.action_space.spaces.keys():
        mctsAgents.append(mctsAgent(agentId=robotId, environment=env, timeLimit=None, iterationLimit=10000))

    complexAgent = ComplexAgentComponent(mctsAgents)

    episode = Episode(complexAgent, env, None, render=True)
    episode.addListener(JsonLogger(logoutput))
    episode.addListener(PickleLogger(logoutputpickle))
    episode.run()
    print("json output:", logoutput.getvalue())
    print("pickle output (binary):", logoutputpickle.getvalue())

	
if __name__ == "__main__":
	main()
	

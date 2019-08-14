import os
import logging
from aienvs.FactoryFloor.FactoryFloor import FactoryFloor
from aiagents.single.RandomAgent import RandomAgent
from aiagents.single.FactoryFloorAgent import FactoryFloorAgent
from aiagents.single.mcts.mctsAgent import MctsAgent
from aiagents.multi.ComplexAgentComponent import ComplexAgentComponent
import random
from aienvs.runners.Episode import Episode
from aienvs.utils import getParameters
from aienvs.loggers.JsonLogger import JsonLogger
import io
from aienvs.loggers.PickleLogger import PickleLogger
import copy
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def main():
    """
    Demo how to run an agent
    """
    if(len(sys.argv) > 1):
        configName = str(sys.argv[1])
        filename = configName
    else:
        print("Default config ")
        configName = "./configs/factory_floor_dilemma.yaml"
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, configName)

    print("Config name " + configName)
    logging.info("Starting example MCTS agent")
    logoutput = io.StringIO("episode output log")
    logoutputpickle = io.BytesIO()
    parameters = getParameters(filename)
    random.seed(parameters['seed'])

    env = FactoryFloor(parameters['environment'])
    obs = env.reset()

    mctsAgents = []
    for robotId in env.action_space.spaces.keys():
        sim = copy.deepcopy(env)
        otherAgentsList = list()
        for otherRobotId in env.action_space.spaces.keys():
            if otherRobotId != robotId:
                # this needs to be done by a factory inside mctsAgent
                # otherAgentsList.append(RandomAgent(otherRobotId, sim, parameters={}))
                otherAgentsList.append(FactoryFloorAgent(otherRobotId, sim, parameters={}))
        rolloutAgent = RandomAgent(robotId, sim, parameters={})
        treeAgent = RandomAgent(robotId, sim, parameters={})
        mctsAgents.append(MctsAgent(agentId=robotId, environment=env, parameters=parameters['agents'], treeAgent=treeAgent, rolloutAgent=rolloutAgent, otherAgents=copy.deepcopy(ComplexAgentComponent(otherAgentsList)), simulator=sim))

    complexAgent = ComplexAgentComponent(mctsAgents)
    episode = Episode(complexAgent, env, obs, render=True)
    episode.addListener(JsonLogger(logoutput))
    episode.addListener(PickleLogger(logoutputpickle))

    episode.run()
    print("json output:", logoutput.getvalue())
    print("pickle output (binary):", logoutputpickle.getvalue())

	
if __name__ == "__main__":
        main()
	

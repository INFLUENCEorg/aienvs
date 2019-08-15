import os
import logging
from aienvs.FactoryFloor.FactoryFloor import FactoryFloor
from aiagents.AgentFactory import createAgent
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
    dirname = os.path.dirname(__file__)

    if(len(sys.argv) > 1):
        env_configName = str(sys.argv[1])
        agent_configName = str(sys.argv[2])

    else:
        print("Default config ")
        env_configName = "./configs/factory_floor_dilemma.yaml"
        env_filename = os.path.join(dirname, env_configName)
        agent_configName = "./configs/agent_config.yaml"
        agent_filename = os.path.join(dirname, agent_configName)

    env_parameters = getParameters(env_filename)
    agent_parameters = getParameters(agent_filename)
    random.seed(env_parameters['seed'])
    env = FactoryFloor(env_parameters['environment'])


    logging.info("Starting example MCTS agent")
    logoutput = io.StringIO("episode output log")
    logoutputpickle = io.BytesIO()


    obs = env.reset()
    complexAgent = createAgent(env, agent_parameters)

    print(env.action_space.spaces.keys())
 #   for robotId in env.action_space.spaces.keys():
 #       sim = copy.deepcopy(env)
 #       otherAgentsList = list()
 #       for otherRobotId in env.action_space.spaces.keys():
 #           if otherRobotId != robotId:
                # this needs to be done by a factory inside mctsAgent
                # otherAgentsList.append(RandomAgent(otherRobotId, sim, parameters={}))
 #               otherAgentsList.append(FactoryFloorAgent(otherRobotId, sim, parameters={}))
 #       rolloutAgent = RandomAgent(robotId, sim, parameters={})
 #       treeAgent = RandomAgent(robotId, sim, parameters={})
 #       mctsAgents.append(MctsAgent(agentId=robotId, environment=env, parameters=parameters['agents'], treeAgent=treeAgent, rolloutAgent=rolloutAgent, otherAgents=copy.deepcopy(BasicComplexAgent(otherAgentsList))))

    episode = Episode(complexAgent, env, obs, render=True)
    episode.addListener(JsonLogger(logoutput))
    episode.addListener(PickleLogger(logoutputpickle))

    episode.run()
    print("json output:", logoutput.getvalue())
    print("pickle output (binary):", logoutputpickle.getvalue())

	
if __name__ == "__main__":
        main()
	

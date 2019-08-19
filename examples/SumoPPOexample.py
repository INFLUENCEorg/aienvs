import os
import logging
from aienvs.Sumo.SumoGymAdapter import SumoGymAdapter
from aiagents.single.PPO.PPOAgent import PPOAgent
from aiagents.multi.BasicComplexAgent import BasicComplexAgent
import random
from aienvs.runners.Episode import Episode
from aienvs.runners.Experiment import Experiment
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
    if( len(sys.argv) > 1 ):
        configName = str(sys.argv[1])
        filename = configName
    else:
        print("Default config ")
        configName = "./configs/new_traffic_loop_ppo.yaml"
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, configName)

    print( "Config name " + configName )
    logging.info("Starting example PPO agent")
    logoutput = io.StringIO("episode output log")
    parameters = getParameters(filename)

    env = SumoGymAdapter(parameters['all'])

    # here we initialize all agents (in that case one)
    PPOAgents = []
    # only to get the observation space, not a real run
    env.reset()
    for intersectionId in env.action_space.spaces.keys():
        PPOAgents.append(PPOAgent(agentId=intersectionId, environment=env, parameters=parameters['all']))
    complexAgent = BasicComplexAgent(PPOAgents)
    
    # experiment is a sequence of episodes with same agents and
    experiment = Experiment(complexAgent, env, parameters['all']['max_steps'], parameters['all']['seedlist'], render=True)
    experiment.addListener(JsonLogger(logoutput))
    experiment.run()

    #print("json output:", logoutput.getvalue()) # logs from all episodes within the experiment
	
if __name__ == "__main__":
        main()
	

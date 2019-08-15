import os
import logging
from aienvs.FactoryFloor.FactoryFloor import FactoryFloor
from aiagents.AgentFactory import createAgent
import random
from aienvs.runners.Experiment import Experiment
from aienvs.utils import getParameters
from aienvs.loggers.JsonLogger import JsonLogger
import io
from aienvs.loggers.PickleLogger import PickleLogger
import copy
import sys
import pickle

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
        env_configName = "./configs/factory_floor_experiment.yaml"
        env_filename = os.path.join(dirname, env_configName)
        agent_configName = "./configs/agent_config.yaml"
        agent_filename = os.path.join(dirname, agent_configName)

    env_parameters = getParameters(env_filename)
    agent_parameters = getParameters(agent_filename)
    random.seed(env_parameters['seed'])
    maxSteps=env_parameters['max_steps']
    env = FactoryFloor(env_parameters['environment'])

    logging.info("Starting example MCTS agent")
    logoutput = io.StringIO("episode output log")

    try:
        logoutputpickle = open('./'+os.environ["SLURM_JOB_ID"] +'.pickle', 'wb')
    except KeyError:
        print("No SLURM_JOB_ID found")
        logoutputpickle = io.BytesIO()

    obs = env.reset()
    complexAgent = createAgent(env, agent_parameters)

    experiment = Experiment(complexAgent, env, maxSteps, render=True)
    experiment.addListener(JsonLogger(logoutput))
    experiment.addListener(PickleLogger(logoutputpickle))
    experiment.run()
    logoutputpickle.close()

    print("json output:", logoutput.getvalue())

 #   instream = open('./file3', 'rb')
 #   while True:
 #       try:
 #           print(pickle.load(instream))
 #       except EOFError:
 #           break
 #   instream.close()

	
if __name__ == "__main__":
        main()
	

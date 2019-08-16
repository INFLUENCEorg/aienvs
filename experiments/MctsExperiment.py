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
from shutil import copyfile

logger = logging.getLogger()
logger.setLevel(logging.ERROR)


def main():
    """
    MCTS Factory Floor experiment
    """
    dirname = os.path.dirname(__file__)

    if(len(sys.argv) > 1):
        env_configName = str(sys.argv[1])
        agent_configName = str(sys.argv[2])
    else:
        print("Default config ")
        env_configName = "./debug_configs/factory_floor_experiment.yaml"
        env_filename = os.path.join(dirname, env_configName)
        agent_configName = "./debug_configs/agent_config.yaml"
        agent_filename = os.path.join(dirname, agent_configName)

    try:
        data_outputdir = os.path.join(dirname, "./data/"+os.environ["EXPERIMENT_JOB_ID"])
        os.mkdir(data_outputdir)
        logoutputpickle = open('./' + data_outputdir +'/output.pickle', 'wb')
        copyfile(env_filename, data_outputdir + "/env.yaml")
        copyfile(agent_filename, data_outputdir + "/agent.yaml")
    except KeyError:
        print("No EXPERIMENT_JOB_ID found")
        logoutputpickle = io.BytesIO()


    env_parameters = getParameters(env_filename)
    agent_parameters = getParameters(agent_filename)

    print(env_parameters)
    print(agent_parameters)

    random.seed(env_parameters['seed'])
    maxSteps=env_parameters['max_steps']
    env = FactoryFloor(env_parameters['environment'])

    logging.info("Starting example MCTS agent")
    logoutput = io.StringIO("episode output log")

    obs = env.reset()
    complexAgent = createAgent(env, agent_parameters)

    experiment = Experiment(complexAgent, env, maxSteps, render=False)
    experiment.addListener(JsonLogger(logoutput))
    experiment.addListener(PickleLogger(logoutputpickle))
    stats, confidence_ints = experiment.run()
    logoutputpickle.close()

    print("json output:", logoutput.getvalue())
    print("\n\nREWARD STATS: " + str(stats) + " \nCONFIDENCE INTERVALS " + str(confidence_ints))

 #   instream = open('./file3', 'rb')
 #   while True:
 #       try:
 #           print(pickle.load(instream))
 #       except EOFError:
 #           break
 #   instream.close()

	
if __name__ == "__main__":
        main()
	

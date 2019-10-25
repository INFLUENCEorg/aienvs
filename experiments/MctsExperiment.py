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
import yaml
from shutil import copyfile
from scipy import stats
import configargparse

logger = logging.getLogger()
logger.setLevel(logging.ERROR)


def main():
    """
    MCTS Factory Floor experiment
    """
    dirname = os.path.dirname(__file__)

    parser = configargparse.ArgParser()
    parser.add('-e', '--env-config', dest="env_filename", 
            default=os.path.join(dirname, "./debug_configs/factory_floor_experiment.yaml"))
    parser.add('-a', '--agent-config', dest="agent_filename",
            default=os.path.join(dirname, "./debug_configs/agent_config.yaml"))
    parser.add('-d', '--data-dirname', dest="data_dirname", default="data")

    args = parser.parse_args()

    try:
        data_outputdir = os.path.join(dirname, "./"+ args.data_dirname + "/"+os.environ["SLURM_JOB_ID"])
        os.makedirs(data_outputdir)
        logoutputpickle = open('./' + data_outputdir +'/output.pickle', 'wb')
        rewardsFile = open('./' + data_outputdir + '/rewards.yaml', 'w+') 
    except KeyError:
        print("No SLURM_JOB_ID found")
        logoutputpickle = io.BytesIO()
        rewardsFile = io.StringIO()

    env_parameters = getParameters(args.env_filename)
    agent_parameters = getParameters(args.agent_filename)

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
    rewards = experiment.run()
    statistics, confidence_ints = stats.describe(rewards), stats.bayes_mvs(rewards)
    logoutputpickle.close()

    yaml.dump(rewards, rewardsFile)
    rewardsFile.close()

    print("json output:", logoutput.getvalue())
    print("\n\nREWARD STATS: " + str(statistics) + " \nCONFIDENCE INTERVALS " + str(confidence_ints))

 #   instream = open('./file3', 'rb')
 #   while True:
 #       try:
 #           print(pickle.load(instream))
 #       except EOFError:
 #           break
 #   instream.close()

	
if __name__ == "__main__":
        main()
	

import logging
from aiagents.AgentComponent import AgentComponent
from aienvs.Environment import Env
from gym import spaces
import yaml

def runExperiment(agent:AgentComponent, env: Env, maxSteps:int, render:bool=False, renderDelay=0):
    """
    Resets env. Loop env.step and agent.select_actions() until number of steps have been made.
    If an env is done before the number of steps have been reached, the env is reset.
    @param agent an AgentComponent holding an agent
    @param env the openai gym Env that we are running in
    @param render True iff environment must be rendered each step.
    @return the number of steps it took to reach done state
    """
    steps = 0
    episodeCount = 0
    totalReward = 0

    while steps < maxSteps:
        env.reset()
        episodeSteps, episodeReward = runEpisode(agent, env, render, renderDelay)
        steps += episodeSteps
        totalReward += episodeReward
        episodeCount += 1

    return totalReward / episodeCount
            
def runEpisode(agent:AgentComponent, env: Env, firstActions:spaces.Dict=None, render:bool=False, renderDelay=0):
    """
    Resets env. Loop env.step and agent.select_actions() until env is done.
    @param agent an AgentComponent holding an agent
    @param env the openai gym Env that we are running in
    @param firstActions the actions for the first step to be taken by agent
    @param render True iff environment must be rendered each step.
    @return the number of steps it took to reach done state, total reward
    """
    actions = firstActions
    done = False
    steps = 0
    totalReward = 0

    while not done:
        obs, globalReward, done, info = env.step(actions)
        agent.observe(obs, globalReward, done)
        totalReward += globalReward
        actions = agent.select_actions()
        if render:
            env.render(renderDelay)
        steps += 1

    return steps, totalReward

def getParameters(filename:str) -> dict:
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



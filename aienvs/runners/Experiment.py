from aiagents.AgentComponent import AgentComponent
from aienvs.Environment import Env
from gym import spaces
from aienvs.runners.Episode import Episode


class Experiment():
    """
    Contains all info to run an experiment

    """

    def __init__(self, agent:AgentComponent, env: Env, maxSteps:int, render:bool=False, renderDelay=0):
        """
        @param agent an AgentComponent holding an agent
        @param env the openai gym Env that we are running in
        @param render True iff environment must be rendered each step.
        """
        self._agent = agent
        self._env = env
        self._maxSteps = maxSteps
        self._render = render
        self._renderDelay = 0
        
    def run(self):
        """
        Resets env. Loop env.step and agent.select_actions() until number of steps have been made.
        If an env is done before the number of steps have been reached, the env is reset.
        @return the total reward divided by the total number of episodes 
        """
        steps = 0
        episodeCount = 0
        totalReward = 0
    
        while steps < self._maxSteps:
            self._env.reset()
            episodeSteps, episodeReward = Episode(self._agent, self._env, self._render, self._renderDelay).run()
            steps += episodeSteps
            totalReward += episodeReward
            episodeCount += 1
    
        return totalReward / episodeCount

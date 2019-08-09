from aiagents.AgentComponent import AgentComponent
from aienvs.Environment import Env
from gym import spaces
from aienvs.runners.Episode import Episode
from aienvs.runners.DefaultRunner import DefaultRunner
from aienvs.listener.DefaultListenable import DefaultListenable
from aienvs.listener.Listener import Listener


class Experiment(DefaultRunner, DefaultListenable, Listener):
    """
    Contains all info to run an experiment

    """

    def __init__(self, agent:AgentComponent, env: Env, maxSteps:int, render:bool=False, renderDelay=0):
        """
        @param agent an AgentComponent holding an agent
        @param env the openai gym Env that we are running in
        @param render True iff environment must be rendered each step.
        """
        super().__init__()
        self._agent = agent
        self._env = env
        self._maxSteps = maxSteps
        self._render = render
        self._renderDelay = 0
        
    def run(self):
        """
        Resets env. Loop env.step and agent.step() until number of steps have been made.
        If an env is done before the number of steps have been reached, the env is reset.
        @return the total reward divided by the total number of episodes 
        """
        steps = 0
        episodeCount = 0
        totalReward = 0
        firstActions = None
    
        while steps < self._maxSteps:
            obs = self._env.reset()
            episode = Episode(self._agent, self._env, obs, self._render, self._renderDelay)
            episode.addListener(self)
            episodeSteps, episodeReward = episode.run()
            steps += episodeSteps
            totalReward += episodeReward
            episodeCount += 1
    
        return totalReward / episodeCount

    def notifyChange(self, data):
        self.notifyAll(data)
    

from aiagents.AgentComponent import AgentComponent
from aienvs.Environment import Env
from gym import spaces
import yaml
from aienvs.runners.DefaultRunner import DefaultRunner
from aienvs.listener.DefaultListenable import DefaultListenable


class Episode(DefaultRunner, DefaultListenable):
    """
    Contains all info to run an episode (single run till environment is done)
    """

    def __init__(self, agent:AgentComponent, env: Env, firstActions:spaces.Dict=None, render:bool=False, renderDelay=0):
        """
        @param agent an AgentComponent holding an agent
        @param env the openai gym Env that we are running in
        @param firstActions the actions for the first step to be taken by agent
        @param render True iff environment must be rendered each step.
        """
        super().__init__()
        self._agent = agent
        self._env = env
        self._firstActions = firstActions
        self._render = render
        self._renderDelay = renderDelay

    def run(self):
        """
        Resets env. Loop env.step and agent.select_actions() until env is done.
        @return the number of steps it took to reach done state, total reward
        """
        actions = self._firstActions
        done = False
        steps = 0
        totalReward = 0
    
        while not done:
            obs, globalReward, done, info = self._env.step(actions)
            self.notifyAll({'steps':steps, 'reward':globalReward, 'done':done, 'actions':actions})
            self._agent.observe(obs, globalReward, done)
            totalReward += globalReward
            actions = self._agent.select_actions()
            if self._render:
                self._env.render(self._renderDelay)
            steps += 1
    
        return steps, totalReward

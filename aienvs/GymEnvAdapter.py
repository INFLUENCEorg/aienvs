import gym
import string
from Environment import Environment 
from EnvironmentState import EnvironmentState

class GymEnvAdapter(Environment):
    """
    Adapter that converts any Gym environment ijnto a Influence environment
    """
    def __init__(self, envname:string):
        """
        @param envname the name of the gym env, eg 'CartPole-v0' or 'Breakout-v0' (Atari game)
        """
        self.env = gym.make(envname)
        
    def initialize(self, parameters:dict):
        """
        @param parameters a dictionary with the following keys and values:
        'render': render the scene every step iff value is True.
        """
        self.__options=parameters
        self.env.reset()
        
    def getActionMap(self) -> dict:
        """
        Gym supports only 1 entity. Key 0 contains all possible actions for it. 
        """
        # this should be made smarter for general gym envs
        return {0:list(range(self.env.action_space.n))}
    
    def step(self, actions: dict) -> EnvironmentState:
        """
        @param actions: the actions to be taken. gym supporst only one entity, 
        given here the id  0. So put key 0 and the appropriate action value (usually an integer) 
        @return: dictionary with keys 'done' and 'observation'.
        'done' = true iff the environment reached the end
        'observation' = the content of the observation. You need
        to read the manual of your environment to understand the meaning
        of this value, see http://gym.openai.com/docs/#spaces
        'reward' = the reward attained in the game at this point
        """
        observation, reward, done, info = self.env.step(actions[0])
        if (self.__options['render']):
            self.env.render()
        return {'done':done, 'observation':observation, 'reward':reward}
    
    def close(self):
        self.env.close()
    
    
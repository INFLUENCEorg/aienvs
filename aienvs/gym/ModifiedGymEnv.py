from aienvs.Environment import Env
from gym.spaces import Dict
from aienvs.gym.ModifiedActionSpace import ModifiedActionSpace
from collections import OrderedDict


class ModifiedGymEnv(Env):
    '''
    Modifies a gym environment by compressing specified actions
    into compound actions.
    '''
    
    def __init__(self, env:Env, newactspace: ModifiedActionSpace):
        '''
        @param env the environment that is to be modified
        @param newactspace an actionspace 
        that replaces the actionspace in the given env
        '''
        self._env = env
        self._newactionspace = newactspace
        
    def step(self, actions:OrderedDict):
        if not self._env.action_space == self._newactionspace.getOriginalSpace():
            raise Exception("Unsupported: can't handle action space change")
        return self._env.step(self._newactionspace.unpack(actions))

    def setState(self, state):
        self._env.setState(state)

    def getState(self, state):
        self._env.getState()

    @property
    def action_space(self) -> Dict:
        return self._newactionspace

    ############ Forward other commands directly to self._env

    # Set this in SOME subclasses
    @property
    def metadata(self):
        return self._env.metadata()

    @property
    def reward_range(self):
        return self._env.reward_range()

    @property
    def spec(self):
        return self._env.spec()

    def observation_space(self):
        return self._env.observation_space()

    def reset(self):
        return self._env.reset()

    def render(self, mode='human'):
        return self._env.render(mode)
    
    def close(self):
        return self._env.close()

    def seed(self, seed=None):
        return self._env.seed(seed)
   

from aienvs.Environment import Env
from gym.spaces import Dict
from aienvs.DecoratedSpace import DecoratedSpace
from ModifiedActionSpace import ModifiedActionSpace
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
        if not self._env.action_space() == self._newactionspace.getOriginalSpace():
            raise Exception("Unsupported: can't handle action space change")
        return self._env.step(self._newactionspace.unpack(actions))
    
    def action_space(self) -> Dict:
        return self._newactionspace


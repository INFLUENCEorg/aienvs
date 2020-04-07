import logging
from gym import spaces
from gym.spaces import Dict, MultiBinary, Tuple
from aienvs.Environment import Env
from numpy import set_printoptions, transpose, zeros
from numpy import array, dstack, ndarray
import copy
from random import Random
from numpy.random import seed as npseed
from numpy.random import choice as weightedchoice
import time
import random
import pdb
import numbers
from aienvs.gym.CustomObjectSpace import CustomObjectSpace
from aienvs.BasicMap import BasicMap
from aienvs.PredatorPrey.PredatorPreyState import PredatorPreyState
from aienvs.PredatorPrey.Predator import Predator
from aienvs.PredatorPrey.Prey import Prey
from typing import List

USE_PossibleActionsSpace = False


class PredatorPreyEnv(Env):
    """
    The predator-prey environment. 
    This is a generalization from https://arxiv.org/pdf/1910.00091.pdf section 5.1
    The map in the original paper is 10x10 without obstacles. 
    There are M entities on the map, hunting for N prey.
    The map can contain obstacles that neither hunters nor prey can step on.
    Each entity ('agent' in the paper) can move in 1 of 4 compass directions,
    remain still, to try to catch adjacent prey.
    Impossible actions, ie moves into an occupied target position or
    catching when there is no adjacent prey, are treated as unavailable
    (unavailable means ignored in this implementation)
    The prey moves by randomly selecting one available movement,
    or remains motionless if all surrounding positions are occupied.
    If two adjacent agents execute the catch action, a prey is caught 
    and both the prey and the catching agents are removed from the grid.
    FIXME explain this.
    An agent's observation is a 5x5 sub-grid centered around it, with one channel
    showing entities and another indicating prey.  FIXME explain channels.
    Removed entities and prey are no longer visible and removed entities receive
    a special observation of all zeros. FIXME zeroes?
    An episode ends if all entities have been removed or after STEPS time steps. 
    Capturing a prey is rewarded r=10, but unsuccessful attempts by single 
    entities are punished by a negative reward p.
    
    The following parameters can be used:
    * p: the punishment/reward, added for unsuccessful captures. defaults to 0.
     should be negative to really act as a punishment.
    * steps: Max number of time steps of the env. defaults to 200.
    * predators: a list of dicts. Each dict contains 'id' (unique entity label)
     and 'pos' with list [X,Y] where X,Y is the initial position of the entity
    * map: the BasicMap on which the game is played, see BasicMap.
    * returnRealState: if True, step returns the real state object.
        if False, step returns a gym state
    """
    DEFAULT_PARAMETERS = {'steps':200,
                'p':0,
                'predators':[ {'id': "predator1", 'pos':[3, 4]}, {'id': "predator2", 'pos': 'random'}],  # initial predator positions
                'preys':[ {'id': "prey1", 'pos':[7, 1]}, {'id': "prey2", 'pos': 'random'}],  # initial prey positions
                'seed':None,
                'returnRealState':False,
                'map':['..........',
                       '..........',
                       '..........',
                       '..........',
                       '..........',
                       '..........',
                       '..........',
                       '..........',
                       '..........',
                       '..........']
                }

    # notice actions 0-4 are same as MovableItemOnMap
    ACTIONS = {
        0: "UP",
        1: "DOWN",
        2: "LEFT",
        3: "RIGHT",
        4: "CATCH"
    }   

    def __init__(self, parameters:dict={}):
        """
        init 
        @param parameters the env settings, see the default settings above. 
        """
        self._parameters = copy.deepcopy(self.DEFAULT_PARAMETERS)
        self._parameters.update(parameters)

        self.seed(self._parameters['seed'])
        predators = [Predator(p['id'], array(p['pos']), True) for p in self._parameters['predators']]
        preys = [Prey(p['id'], array(p['pos']), True) for p in self._parameters['preys']]
        map = BasicMap(self._parameters['map'])
        self._state = PredatorPreyState(predators, preys, map, 0, 0, self._parameters['steps'])
        self._actSpace = spaces.Dict({pred.getId():spaces.Discrete(len(self.ACTIONS)) \
                                      for pred in self._state.getPredators()})

    # Override
    def step(self, actions:dict):
        self._step(actions)
        s = self._state
        if self._parameters['returnRealState']:
            return s, s.getReward(), s.isFinal(), []
        else:
            return s.getStateMatrix(), s.getReward(), s.isFinal(), []
    
    def _step(self, actions:dict):
        if(self._state.isFinal()) or (not actions):
            return 
        self._catch(actions)
        self._stepPredators(actions)
        self._stepPreys()
        self._state = self._state.increment()
    
    def reset(self):
        self.__init__(self._parameters)
        return copy.deepcopy(self._state)  # should return initial observation

    # Override
    def render(self, delay=0.0, overlay=False):
        map = self._state.getFullMap()  # list of strings
        for y in range(len(map)):
            for x in range(len(map[y])):
                if self._state.isPredatorAt(array(x, y)):
                    map[y][x] = 'P'
                if self._state.isPreyAt(array(x, y)):
                    map[y][x] = '='
        print(*map, sep="\n")
        time.sleep(delay)

    # Override
    def close(self):
        pass  

    # Override
    def seed(self, seed):
        self._parameters['seed'] = seed
        if isinstance(self._parameters['seed'], numbers.Number):
            npseed(self._parameters['seed'])
        random.seed(seed)

    def getState(self) -> PredatorPreyState:
        return self._state

    def setState(self, newState:PredatorPreyState):
        self._state = newState  # no copy needed, immutable

    @property
    def observation_space(self):
        """
        If returnRealSpace=true, the observation is simply the full state.
        if falsle each entity receives as observation 3 5x5 binary matrices. 
        Refer to PredatorPreyState#getStateMatrix for details.
        """
        if self._parameters['returnRealSpace']:
            return CustomObjectSpace(self._state);
        else:
            mb = MultiBinary(5)  # 5x1 binary matrix
            mbs = Tuple(mb, mb, mb, mb, mb)  # 5 of them for 5x5 binary
            entityobs = Tuple(mbs, mbs, mbs)  # an obs is 3 5x5 matrices
            return Dict ({ pred.getId() : entityobs \
                           for pred in self._state.getPredators()})
        
    @property
    def action_space(self):
        if USE_PossibleActionsSpace:
            actSpace = spaces.Dict({robotId:PossibleActionsSpace(self, robot) 
                for robotId, robot in self._state.robots.items()})
        else:        
            actSpace = self._actSpace
        return actSpace
            
    def getMap(self) -> BasicMap:
        """
        @return: the map of this floor
        """
        return self._state.getMap()

    ########## Private functions ##########################

    def _stepPreys(self):
        """
        Let the active preys make their step
        """
        for prey in self._state.getPreys() :
            if prey.isActive():
                self._state = self._state.withPreyStep(prey, random.choice(range(4)))
    
    def _stepPredators(self, actions:dict):
        """
        Do the actions of all active predators and update state accordingly.
        actions of inactive predators are ignored.
        It is assumed that all succesful 'catch' actions of predators
        have been executed already. So predators that are still here
        and do a 'catch' missed the prey and get penalized.
        @param actions a dict, keys are predator ids and actions are int ACTIONS.
        """
        for predator in self._state.getPredators() :
            if not predator.isActive():
                continue
            act = actions[predator.getId()]
            if self.ACTIONS[act] == 'CATCH':
                # note, negative reward.
                self._state = self._state.withReward(self._parameters['p'])
            else:  # a step action. 
                self._state = self._state.withStep(predator, act)

    def _catch(self, actions:dict):
        """
        Removes all caught prey and their predators from state
        """
        # Copy the list as we are going to modify state
        preys = self._state.getPreys() 
        for prey in preys: 
            adjacent = self._state.getAdjacentPredators(prey.getPosition())
            adjacent = filter(lambda adj: self.ACTIONS[actions[adj]] == 'CATCH', adjacent)
            if len(adjacent) >= 2:
                # remove prey and first two that catch it 
                self._state = self._state.withCatch(prey, adjacent[0], adjacent[1]) 
    

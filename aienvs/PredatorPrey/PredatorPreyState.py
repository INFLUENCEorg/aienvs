import numpy as np
from aienvs.FactoryFloor.Map import Map
from typing import List
from aienvs.PredatorPrey.Predator import Predator
from aienvs.PredatorPrey.Prey import Prey


class PredatorPreyState():
    """
    Stores the entire state of the PredatorPreyEnv:
    the map, the positions of the entities and preys,
    current total reward etc. immutable
    """

    def __init__(self, predatorsList:List[Predator], preyList:List[Prey], themap:Map, r:float, s:int, maxs: int):
        """
        @param predatorsList: list of PredatorEntity objects, each having a unique id.
        @param preyList: list of Prey objects, each having a unique id.
        @param themap the floor map, immutable
        @param r the current total reward.
        @param s the current step count
        @param maxs the max number of steps 
        """
        self._predators = predatorsList
        self._preys = preyList
        self._map = themap
        self._reward = r
        self._step = s
        self._maxsteps = maxs

    def getMap(self):
        return self._map
    
    def getPredators(self):
        return self._predators.copy()
    
    def getPreys(self):
        return self._preys.copy()
    
    def withCatch(self, prey:Prey, catcher1:Predator, catcher2:Predator) -> PredatorPreyState:
        """
        Execute a catch. 
        @param prey the prey that was caught
        @param catcher1 the first Predator that did the catch
        @param catcher2 the second Predator that did the catch
        @return the new PredatorPreyState. prey, catcher1 and catcher2 have been
        removed, and a reward of 10 is added. 
        """
        if self.isFinal():
            return self
        newpreys = self.getPreys()
        newpreys.remove(prey)
        newpreds = self.getPredators()
        newpreds.remove(catcher1)
        newpreds.remove(catcher2)
        return PredatorPreyState(newpreds, newpreys, self._map, \
            self._reward + 10, self._step, self._maxsteps)
        
    def increment(self) -> PredatorPreyState:
        if self.isFinal():
            return self
        """
        Increment the step counter
        """
        return PredatorPreyState(self._predators, self._preys, self._map, \
                                 self._reward, self._step + 1, self._maxsteps)
    
    def isFinal(self):
        """
        returns true if all entities have been removed or after STEPS time steps. 
        """
        activePredator = any([predator.isActive() for predator in self._predators])
        return (not activePredator) or self._s >= self._maxs

    def __eq__(self, other):
        return self._predators == other._predators \
            and self._preys == other._preys \
            and self._map == other._map \
            and self._reward == other._reward \
            and self._step == other._step
            

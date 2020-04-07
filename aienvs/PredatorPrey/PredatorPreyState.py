from numpy import array, ndarray, array_equal
from typing import List
from aienvs.PredatorPrey.Predator import Predator
from aienvs.PredatorPrey.Prey import Prey
from aienvs.BasicMap import BasicMap


class PredatorPreyState():
    """
    Stores the entire state of the PredatorPreyEnv:
    the map, the positions of the entities and preys,
    current total reward etc. immutable
    
    NOTICE the equals function uses ALL fields and therefore 
    might not be appropriate for learning.
    """

    def __init__(self, predatorsList:List[Predator], preyList:List[Prey], themap:BasicMap, r:float, s:int, maxs: int):
        """
        @param predatorsList: list of PredatorEntity objects, each having a unique id.
        @param preyList: list of Prey objects, each having a unique id.
        @param themap the floor map, immutable
        @param r the current total reward.
        @param s the current step count
        @param maxs the max number of steps 
        """
        self._predators = predatorsList.copy()
        self._preys = preyList.copy()
        self._map = themap
        self._reward = r
        self._step = s
        self._maxsteps = maxs

    def getMap(self) -> BasicMap:
        return self._map
    
    def getPredators(self) -> List[Predator]:
        return self._predators.copy()
    
    def getPreys(self) -> List[Prey]:
        return self._preys.copy()
    
    def getObservationMatrix(self):
        """
        @return a gym-style dict with for each entity (predator) 
        a 3x5x5 matrix, containing the observations for all predators. 
        See _getPredatorObsMatrix for more details on each 3x5x5 matrix
        """
        return { pred.getId(): self._getPredatorObsMatrix(pred)\
                for pred in self._predators}
    
    def isPredatorAt(self, pos:ndarray) -> bool:
        """
        @return true iff there is a predator at given position
        """
        return any(map(lambda pred: array_equal(pred.getPosition(), pos)), self._predators)

    def isPreyAt(self, pos:ndarray):
        """
        @return true iff there is a prey at given position
        """
        return any(map(lambda prey: array_equal(prey.getPosition(), pos)), self._preys)

    def getAdjacentPredators(self, pos:ndarray) -> List[Predator]:
        """
        @param pos a ndarray with some [x,y] position on the map
        @return all active predators that are directly N,E,S or W from given pos
        """
        return filter(lambda pred: pred.isAdjacent(pos) and pred.isActive(), \
                       self.getPredators())

    def withCatch(self, prey:Prey, catcher1:Predator, catcher2:Predator) -> 'PredatorPreyState':
        """
        Execute a catch. It is assumed that all are correctly placed to do this.
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
        
    def withReward(self, reward:float) -> 'PredatorPreyState':
        """
        @return new PredatorPreyState given reward added 
        """
        if self.isFinal():
            return self
        return PredatorPreyState(self._predators, self._preys, self._map, \
            self._reward + reward, self._step, self._maxsteps) 
        
    def withStep(self, pred: Predator, act: int) -> 'PredatorPreyState':
        """
        Predator does a move action
        @act an action in [0,3] moving N,E,S or W. 
        @return new PredatorPreyState with move executed if the new pos is free
        """
        newpred = pred.withStep(act)
        newpos = newpred.getPosition()
        
        if self.isPredatorAt(newpos) or self.isPreyAt(newpos)\
            or not self._map.isFree(newpos):
            return self
        
        # replace predator in the predators list
        preds = [newpred if p.getId() == pred.getId() else p for p in self._predators]
        return PredatorPreyState(preds, self._preys, self._map, \
            self._reward, self._step, self._maxsteps) 

    def withPreyStep(self, prey: Prey, act: int) -> 'PredatorPreyState':
        """
        Prey does a move action
        @act an action in [0,3] moving N,E,S or W. 
        """
        preys = self.getPreys()
        preys[prey.getId()] = prey.withStep(act)
        return PredatorPreyState(self._predators, preys, self._map, \
            self._reward, self._step, self._maxsteps) 
        
    def increment(self) -> 'PredatorPreyState':
        """
        Increment the step counter
        @return new PredatorPreyState with incremented step counter.
        """
        if self.isFinal():
            return self
        return PredatorPreyState(self._predators, self._preys, self._map, \
                                 self._reward, self._step + 1, self._maxsteps)
    
    def isFinal(self) -> bool:
        """
        @return true if all entities have been removed or after STEPS time steps.
        NOTICE this is according to the paper. BUT if only 1 entity is left,
        there is nothing he can do. 
        """
        activePredator = any([predator.isActive() for predator in self._predators])
        return (not activePredator) or self._step >= self._maxsteps

    def _getPredatorObsMatrix(self, pred:Predator):
        """
        @param pred the predator to get obs matrix for
        @return the observation matrix (3x5x5) of given predator.
        Each 5x5 matrix represents the 5x5 area around the entity, in 
        the top-left to bottom-right. So first line in the matrix
        is the NW to NE content. The last row the SW to SE content.
        The center position in the matrix (3,3) represents the 
        position of the predator himself.
        The first matrix contains a 1 at positions where there is a
        predator on the map.
        The second matrix contains 1 at positions where there is a 
        prey on the map
        The third matrix contains 1 at positions where there is an 
        obstacle on the map, eg a wall or edge of the map.
        The full obs space is a dict with a 3x5x5 matrix for each predator. 

        """
        predmap = [ [0] * 5 for row in range(5)]
        preymap = [ [0] * 5 for row in range(5)]
        obstmap = [ [0] * 5 for row in range(5)]
        mypos = pred.getPosition()
        for x in range(0, 5):
            for y in range(0, 5):
                pos = array([x - 2, y - 2]) + mypos
                if self._map.isFree(pos):
                    obstmap[y][x] = 1
                if self.isPredatorAt(pos):
                    predmap[y][x] = 1
                if self.isPreyAt(pos):
                    preymap[y][x] = 1
                    
        return [predmap, preymap, obstmap]

    def __eq__(self, other):
        return self._predators == other._predators \
            and self._preys == other._preys \
            and self._map == other._map \
            and self._reward == other._reward \
            and self._step == other._step
            

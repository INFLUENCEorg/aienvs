from gym.spaces.space import Space
import random
from aienvs.FactoryFloor.FactoryFloor import FactoryFloor


class PossibleActionsSpace(Space):
    """
    A gym space that returns the possible actions at this moment
    on the factory floor.
    REQUIREMENT: at all times, at least one action must be possible.
    If not, sample() may raise an exception
    @param thefloor: the FactoryFloor
    """

    def __init__(self, thefloor:FactoryFloor):
        super().__init__()
        self._floor = thefloor
    
    # override
    def sample(self):
        return [random.choice(self._floor.getPossibleActions(robot)) 
            for robot in self._floor.getState().getRobots()]
        
    def contains(self, act):
        robots = self._floor.getState().getRobots()
        if (len(robots) != len(act)):
            return False
        for i in range(len(robots)):
            if not self._floor.isPossible(robots[i], act[i]):
                return False
        return True
    

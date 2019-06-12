from gym.spaces.space import Space
import random
from aienvs.FactoryFloor.FactoryFloor import FactoryFloor
from aienvs.FactoryFloor.FactoryFloor import FactoryFloorRobot


class PossibleActionsSpace(Space):
    """
    A gym space that returns the possible actions at this moment
    on the factory floor for some robot.
    REQUIREMENT: at all times, at least one action must be possible.
    If not, sample() may raise an exception
    @param thefloor: the FactoryFloor
    @param bot: the FactoryFloorRobot
    """

    def __init__(self, fl:FactoryFloor, bot:FactoryFloorRobot):
        super().__init__()
        self._floor = fl
        self._robot = bot
    
    # override
    def sample(self):
        return random.choice(self._floor.getPossibleActions(self._robot))
        
    def contains(self, act):
        return self._floor.isPossible(self._robot, act)
    

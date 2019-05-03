from abc import ABC, abstractmethod
from aienvs.EnvironmentState import EnvironmentState

class Environment(ABC):
    """
    Abstract base class of all Influence environments
    """
    
    @abstractmethod
    def getActionMap(self) -> dict:
        """
        @return:  a dictionary of the currently possible actions. 
        Keys are the entity names, values are 
        the possible actions that that entity can do. 
        TODO refine values with parameters, 
        to avoid too many variants of each possible action?
        """
        pass
    
    @abstractmethod
    def step(self, actions: dict) -> EnvironmentState:
        """
        Let the environment make a discrete timestep.
        Can be called only after environment has been initialized.
        @param actions: a dictionary with actions to be taken in this step.
        Keys are the entity ids, values are a list of actions to be taken by the entity.
        Entities may handle more than 1 action every timestep, 
        this depends on the environment. Environments may throw if illegal actions are taken.
        The environment is assumed to proceed as follows.
        1. All entities take the actions as indicated in the actions dictionary
        2. The simulation advances one timestep.
        @return:  the new EnvironmentState
        """
        pass

   

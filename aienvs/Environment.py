from abc import ABC, abstractmethod

class Environment(ABC):
    """
    Abstract base class of all Influence environments
    """
    
    @abstractmethod
    def initialize(self, parameters:dict):
        """
        Initializes the environment, resets it to its initial state, using the parameters
        @param parameters: a dictionary with environment-specific configuration values 
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

    @abstractmethod
    def close(self):
        """
        Closes the environment, close windows and GUIs, release all resources,
        save final information and de-initializes the environment.
        initialize can be called to re-initialize the environment after a close.
        """
        pass
    
    
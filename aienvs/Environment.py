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
    def step(self) -> EnvironmentState:
        """
        Let the environment make a discrete timestep.
        Can be called only after environment has been initialized.
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
    
    
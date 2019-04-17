from abc import ABC, abstractmethod

class Environment(ABC):
    """
    Abstract base class of all Influence environments
    """
    @abstractmethod
    def step(self) -> State:
        """
        @return:  the new State of the environment
        """
        pass


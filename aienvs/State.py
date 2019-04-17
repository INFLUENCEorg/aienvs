from abc import ABC, abstractmethod

class State(ABC):
    """
    Abstract base class of the state of an environment
    """
    @abstractmethod
    def getActionMap(self) -> dict:
        """
        @return:  a dictionary of the currently possible actions. TODO refine with parameters, 
        to avoid too many variants of each possible action?
        """
        pass

    def getPercepts(self) -> dict:
        """
        @return: a dictionary of the currently available percepts. 
        Keys are the entities in the environment. Values are the actual percepts of each entity.
        """
        pass
    
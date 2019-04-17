from abc import ABC, abstractmethod

class EnvironmentState(ABC):
    """
    Abstract base class of the state of an environment
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
    def getPercepts(self) -> dict:
        """
        @return: a dictionary of the currently available percepts. 
        Keys are the entities in the environment. 
        Values are the actual percepts of each entity.
        """
        pass
    
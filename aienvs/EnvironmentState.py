from abc import ABC, abstractmethod

class EnvironmentState(ABC):


    @abstractmethod
    def getPercepts(self) -> dict:
        """
        @return: a dictionary of the currently available percepts. 
        Keys are the entities in the environment. 
        Values are the actual percepts of each entity.
        """
        pass
    
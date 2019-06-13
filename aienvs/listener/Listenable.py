from abc import ABC, abstractmethod
from aienvs.listener.Listener import Listener


class Listenable(ABC):

    @abstractmethod
    def addListener(self, l: Listener):
        """
        @param l a Listener to be added 
        """
        pass

    @abstractmethod
    def removeListener(self, l: Listener):
        """
        @param l a Listener to be removed 
        """
        pass
     

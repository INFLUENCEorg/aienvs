from gym.spaces import Space, Dict, Discrete, MultiDiscrete, Box, Tuple, MultiBinary
import math


class DecoratedSpace(Space):
    '''
    Decorates gym spaces with extra functionality to make it possible
    to handle all spaces in a generic way.
    '''

    def __init__(self, space:Dict):
        '''
        DO NOT CALL THIS DIRECTLY. Use create.
        @param space a gym dictionary space. 
        @param mergeInfo a list containing lists of keys to be merged. 
        For instance [['a','b'],['c','d','e']] indicates
        that the keys a and b are to be merged into a 
        new key a_b, and c,d,e are to be merged into new key c_d_e
        The remaining keys in the original space are left untouched.
        '''
        self._gymspace = space
        
    @staticmethod
    def create(space: Space):  # -> DecoratedSpace:
        '''
        factory method, creating the correct instance of 
        DecoratedSpace according to the type given
        '''
        if (isinstance(space, Dict)):
            return DictSpaceDecorator(space)
        if (isinstance(space, Discrete)):
            return DiscreteSpaceDecorator(space)
        if (isinstance(space, Box)):
            return BoxSpaceDecorator(space) 
        if (isinstance(space, Tuple)):
            return TupleSpaceDecorator(space) 
        if (isinstance(space, MultiDiscrete)):
            return MultiDiscreteSpaceDecorator(space)
        if (isinstance(space, MultiBinary)):
            return MultiBinarySpaceDecorator(space)

        raise Exception("Unsupported space type " + str(space))  

    def getSpace(self):
        '''
        the gym space that is decorated
        '''
        return self._gymspace
        
    def getSize(self):
        '''
        @return:  the total number of possible discrete values in this space.
        This has to be determined dynamically as 
        the space can change over time. May return math.inf
        to indicate infinite number of  discrete values are possible.
        '''
        raise NotImplementedError
    
    def getSubSpaces(self) -> list:  # list<DecoratedSpace>
        '''
        @return: (possibly empty) list of DecoratedSpaces that are child of this space.
        '''
        return []


class DictSpaceDecorator(DecoratedSpace):
    '''
    Decorates a spaces.Dictfrom abc import abstractclassmethod

    '''

    def __init__(self, space:Dict, mergeInfo:list=[]):
        '''
        @param mergeInfo optional. 
        contains lists of keys to be merged. 
        For instance [['a','b'],['c','d','e']] indicates
        that the keys a and b are to be merged into a 
        new key a_b, and c,d,e are to be merged into new key c_d_e
        The remaining keys in the original space are left untouched.
        '''
        super().__init__(space)
        
    def getSubSpaces(self):
        return [DecoratedSpace.create(space) for space in self.getSpace().spaces.values()]
        
    # Override
    def getSize(self):
        size = 1
        for space in self.getSubSpaces():
            size = size * space.getSize()
        return size


class DiscreteSpaceDecorator(DecoratedSpace):
    '''
    Decorates a spaces.Discrete
    '''

    # Override
    def getSize(self):
        return self.getSpace().n


class MultiDiscreteSpaceDecorator(DecoratedSpace):
    '''
    Decorates a spaces.MultipleDiscrete
    '''

    # Override
    def getSize(self):
        size = 1
        for n in self.getSpace().nvec:
            size = size * n
        return size


class TupleSpaceDecorator(DecoratedSpace):
    '''
    Decorates a spaces.Tuple
    '''

    # Override
    def getSize(self):
        size = 1
        for space in self.getSubSpaces():
            size = size * space.getSize()
        return size

    def getSubSpaces(self):
        return [DecoratedSpace.create(space) for space in list(self.getSpace().spaces)]


class BoxSpaceDecorator(DecoratedSpace):
    '''
    Decorates a spaces.Discrete
    '''

    # Override
    def getSize(self):
        return math.inf


class MultiBinarySpaceDecorator(DecoratedSpace):
    '''
    Decorates a spaces.Discrete
    '''

    # Override
    def getSize(self):
        return 2 ** self.getSpace().n

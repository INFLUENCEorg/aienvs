from LoggedTestCase import LoggedTestCase
from unittest.mock import Mock
from aienvs.DecoratedSpace import DecoratedSpace
from gym.spaces import Space, Dict, Discrete, MultiDiscrete, Box, Tuple, MultiBinary
import math


class DecoratedSpaceTest(LoggedTestCase):
    '''
    NOTE: We test directly against the real Space objects
    because we are highly dependent on their implementation internals.
    This is unfortunate but the way gym envs are defined and used
    '''

    def test_Discrete(self):
        space = DecoratedSpace.create(Discrete(5))
        self.assertEquals(5, space.getSize())
        self.assertEquals([], space.getSubSpaces())

    def test_Dict(self):
        space = DecoratedSpace.create(Dict({'a':Discrete(5), 'b':Discrete(2)}))
        self.assertEquals(10, space.getSize())
        self.assertEquals(2, len(space.getSubSpaces()))

    def test_Dict_with_Dict(self):
        space = DecoratedSpace.create(Dict({'p':Dict({'a':Discrete(5), 'b':Discrete(2)}), 'q':Discrete(7)}))
        self.assertEquals(70, space.getSize())
        self.assertEquals(2, len(space.getSubSpaces()))
        
    def test_Box(self):
        space = DecoratedSpace.create(Box(low=-1.0, high=2.0, shape=(3, 4)))
        self.assertEquals(math.inf, space.getSize())
                       
    def test_MultiDiscrete(self):
        space = DecoratedSpace.create(MultiDiscrete([5, 2, 3]))
        self.assertEquals(30, space.getSize())
        self.assertEquals([], space.getSubSpaces())
        
    def test_Tuple(self):
        space = DecoratedSpace.create(Tuple((Discrete(2), Discrete(3))))
        self.assertEquals(2, len(space.getSubSpaces()))
        self.assertEquals(6, space.getSize())

    def test_MultiBinary(self):
        space = DecoratedSpace.create(MultiBinary(7))
        self.assertEquals(2 ** 7, space.getSize())
        self.assertEquals([], space.getSubSpaces())

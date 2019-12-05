from test.LoggedTestCase import LoggedTestCase
from unittest.mock import Mock
from aienvs.gym.DecoratedSpace import DecoratedSpace
from gym.spaces import Space, Dict, Discrete, MultiDiscrete, Box, Tuple, MultiBinary
import math

'''
first element of each list: the space dimensions
second element: the selected element in the space
third element: the integer number of that selected element
''' 
numberListTestValues = [
    [[2, 2, 3], [0, 1, 2], 10],
    [[2, 2, 3], [1, 1, 2], 11],
    [[2, 2, 3], [0, 0, 0], 0],
    [[18, 2], [2, 1], 20],
    [[2, 18], [0, 10], 20],
    [[2, 18], [0, 15], 30],
    [[2, 18], [1, 16], 33]
    ];


class DecoratedSpaceTest(LoggedTestCase):
    '''
    NOTE: We test directly against the real Space objects
    because we are highly dependent on their implementation internals.
    This is unfortunate but the way gym envs are defined and used
    '''

    def test_numberToList(self):
        for val in numberListTestValues:
            self.assertEqual(val[1], DecoratedSpace.numberToList(val[2], val[0]))

    def test_listToNumber(self):
        for val in numberListTestValues:
            self.assertEqual(val[2], DecoratedSpace.listToNumber(val[1], val[0]))

    def test_Discrete(self):
        space = DecoratedSpace.create(Discrete(5))
        self.assertEquals(5, space.getSize())
        self.assertEquals([], space.getSubSpaces())
        self.assertEquals(2, space.getById(2))

    def test_Dict(self):
        space = DecoratedSpace.create(Dict({'a':Discrete(5), 'b':Discrete(2)}))
        self.assertEquals(10, space.getSize())
        self.assertEquals(2, len(space.getSubSpaces()))
        space.getById(8)  # smoke test 
        self.assertEquals({'a':3, 'b':1}, space.getById(8))
        
    def test_emptyDict(self):
        space = DecoratedSpace.create(Dict({}))
        self.assertEquals(0, space.getSize())

    def test_Dict_with_Dict(self):
        space = DecoratedSpace.create(Dict({'p':Dict({'a':Discrete(5), 'b':Discrete(2)}), 'q':Discrete(7)}))
        self.assertEquals(70, space.getSize())
        self.assertEquals(2, len(space.getSubSpaces()))
        self.assertEquals({'p':{'a':4, 'b':0}, 'q':3}, space.getById(34))
        
    def test_Box(self):
        space = DecoratedSpace.create(Box(low=-1.0, high=2.0, shape=(3, 4)))
        self.assertEquals(math.inf, space.getSize())
        self.assertRaises(Exception, space.getOriginalSpace, 1)
                       
    def test_MultiDiscrete(self):
        space = DecoratedSpace.create(MultiDiscrete([5, 2, 3]))
        self.assertEquals(30, space.getSize())
        self.assertEquals([], space.getSubSpaces())
        self.assertEquals([2, 1, 2], list(space.getById(27)))

    def test_Tuple(self):
        space = DecoratedSpace.create(Tuple((Discrete(2), Discrete(3))))
        self.assertEquals(2, len(space.getSubSpaces()))
        self.assertEquals(6, space.getSize())
        self.assertEquals((0, 2), space.getById(4))

    def test_MultiBinary(self):
        space = DecoratedSpace.create(MultiBinary(7))
        self.assertEquals(2 ** 7, space.getSize())
        self.assertEquals([], space.getSubSpaces())
        # reverse of normal binary notation
        self.assertEquals([0, 1, 0, 1, 1, 0, 1], list(space.getById(64 + 16 + 8 + 2)))

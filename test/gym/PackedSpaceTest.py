from test.LoggedTestCase import LoggedTestCase
from unittest.mock import Mock
from aienvs.gym.PackedSpace import PackedSpace
from gym.spaces import Dict  , Discrete


class PackedSpaceTest(LoggedTestCase):
    '''
    NOTE: We test directly against the real Space objects
    because we are highly dependent on their implementation internals.
    This is unfortunate but the way gym envs are defined and used
    '''

    def test_smoke_bad_actionspace(self):
        with self.assertRaises(Exception) as context:
            PackedSpace({'a':1, 'b':2, 'c':3}, {'a_b':['a', 'b']})
        self.assertContains('Unsupported space type', context.exception)

    def test_smoke_bad_packingkeys(self):
        space = Dict({'a':Discrete(4), 'b':Discrete(3), 'c':Discrete(5)})
        with self.assertRaises(Exception) as context:
            PackedSpace(space, {'x':['unknownkey']})
        self.assertContains('refers unknown key' , context.exception)

    def test_smoke(self):
        space = Dict({'a':Discrete(4), 'b':Discrete(3), 'c':Discrete(5)})
        PackedSpace(space, {'a_b':['a', 'b']})
    

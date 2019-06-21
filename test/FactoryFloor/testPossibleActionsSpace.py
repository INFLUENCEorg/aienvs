from aienvs.FactoryFloor.FactoryFloor import PossibleActionsSpace
from aienvs.FactoryFloor.FactoryFloor import FactoryFloor
from unittest.mock import Mock
from test.LoggedTestCase import LoggedTestCase


class testPossibleActionsSpace(LoggedTestCase):

    def test_sample(self):
        bot = Mock()  # FactoryFloorRobot
        state = Mock()
        factory = Mock()
        factory.getState.return_value = state
        factory.getPossibleActions.return_value = ['act1', 'act2']
        space = PossibleActionsSpace(factory, bot)
        sample = space.sample()
        print (sample)
        self.assertTrue(sample in ['act1', 'act2'])

    def test_contains(self):
        bot = Mock()  # FactoryFloorRobot
        state = Mock()
        factory = Mock()

        def myPossible(*args, **kwargs): 
            return args[1] == 'act1'

        factory.isPossible.side_effect = myPossible
        space = PossibleActionsSpace(factory, bot)
        
        self.assertTrue(space.contains('act1'))
        self.assertFalse(space.contains('act0'))
        

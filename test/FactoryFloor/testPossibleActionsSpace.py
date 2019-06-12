from aienvs.FactoryFloor.PossibleActionsSpace import PossibleActionsSpace
from aienvs.FactoryFloor.FactoryFloor import FactoryFloor
from unittest.mock import Mock
from test.LoggedTestCase import LoggedTestCase


class testPossibleActionsSpace(LoggedTestCase):

    def test_sample(self):
        state = Mock()
        state.getRobots.return_value = ['robota', 'robotb', 'robotc']
        factory = Mock()
        factory.getState.return_value = state
        factory.getPossibleActions.return_value = ['act1', 'act2']
        space = PossibleActionsSpace(factory)
        sample = space.sample()
        print (sample)
        self.assertEqual(3, len(sample))

    def test_contains(self):
        state = Mock()
        state.getRobots.return_value = ['robota', 'robotb', 'robotc']
        factory = Mock()
        factory.getState.return_value = state

        def myPossible(*args, **kwargs):
            return (args[0] == 'robota' and args[1] == 'act1') or \
                (args[0] == 'robotb' and args[1] == 'act2') or \
                (args[0] == 'robotc' and args[1] == 'act1')

        factory.isPossible.side_effect = myPossible
        space = PossibleActionsSpace(factory)
        
        self.assertTrue(space.contains(['act1', 'act2', 'act1']))
        self.assertFalse(space.contains(['act0', 'act2', 'act1']))
        

from test.LoggedTestCase import LoggedTestCase
from unittest.mock import Mock
from aienvs.gym.ModifiedGymEnv import ModifiedGymEnv


class ModifiedGymEnvTest(LoggedTestCase):
    
    def test_smoke(self):
        gymenv = Mock()
        actmodifier = Mock()  # PackedSpace
        ModifiedGymEnv(gymenv, actmodifier)

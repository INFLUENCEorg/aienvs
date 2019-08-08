from LoggedTestCase import LoggedTestCase
from aienvs.Environment import Env
from unittest.mock import Mock
from aienvs.EnvironmentFactory import createEnvironment, classForName, classForNameTyped
import datetime


class testAgentFactory(LoggedTestCase):
    """
    This is an integration test that also tests aiagents.
    aiagents project must be installed 
    """
    
    def test_get_class(self):
        D = classForName("datetime.datetime")
        time = D.now()
        actualtime = datetime.datetime.now()
        self.assertEquals(str(time)[0:10], str(actualtime)[0:10])

    def test_get_class_typed(self):
        D = classForNameTyped("datetime.datetime", datetime.datetime)
        time = D.now()
        actualtime = datetime.datetime.now()
        self.assertEquals(str(time)[0:10], str(actualtime)[0:10])

    def test_get_class_typed_wrong(self):
        self.assertRaises(Exception, classForNameTyped, "datetime.datetime", Env)

    def test_smoke(self):
        env = createEnvironment('aienvs.FactoryFloor.FactoryFloor.FactoryFloor', {})

    def test_is_good_env(self):
        env = createEnvironment('aienvs.FactoryFloor.FactoryFloor.FactoryFloor', {})
        acts = env.action_space
        # 5 actions: up, down, left, right, work
        self.assertEquals('Dict(robot1:Discrete(5), robot2:Discrete(5))', str(acts))

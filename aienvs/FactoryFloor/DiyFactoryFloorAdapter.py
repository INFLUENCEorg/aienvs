from aienvs.FactoryFloor.FactoryFloor import FactoryFloor

class DiyFactoryFloorAdapter():
    """
    FactoryFloor with DIY bonus for a given agent
    """
    def __init__(self, ffl: FactoryFloor, diyBonus: float, agentId: str):
        """
        TBA
        """
        self._ffl = ffl
        self._diyBonus = diyBonus
        self._bonusAgent = agentId

    def step(self, actions:dict):
        robotPosition = self._state.robots[self._bonusAgent].getPosition()
        agentAction = self.ACTIONS.get(actions.get(self._bonusAgent))

        diyReward = 0
        if((agentAction == "ACT") and (self._getTask(robotPosition) is not None)):
            diyReward += self._diyBonus

        obs, global_reward, done, info = self._ffl.step(actions)

        return obs, global_reward + diyReward, done, info

    # calling other methods from self._ffl
    def __getattr__(self, attr):
        #avoid recursion
        ffl = self.__getattribute__('_ffl')
        return getattr(ffl, attr)
   



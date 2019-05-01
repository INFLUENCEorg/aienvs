import gym
from gym import spaces
import os
from aienvs.Sumo.LDM import ldm
from aienvs.Sumo.state_representation import *
import time
from sumolib import checkBinary
import random

class SumoGymAdapter(gym.Env):
    """
    An adapter that makes Sumo behave as a proper Gym environment.
    At top level, the actionspace and percepts are in a Dict with the
    trafficPHASES as keys.
    """

    def __init__(self,  parameters:dict=
            {'gui':True, 
            'scenario':os.path.join('$AIENVS_HOME','scenarios/four_grid/'), 
            'box_bottom_corner':(0,0), 
            'box_top_corner':(10,10),
            'resolutionInPixelsPerMeterX': 1,
            'resolutionInPixelsPerMeterY': 1
            }):
        """
        @param path where results go, like "Experiment ID"
        @param parameters the configuration parameters.
        gui: whether we show a GUI. 
        scenario: the path to the scenario to use
        """
        self.parameters = parameters

        self._checkScenario()
       # self.observation_space = self._getObservationSpace()
        self.reset()

    
    def step(self, action:spaces.Dict):
        # Ask SUMO the number of vehicles which are in the net plus the
        # ones still waiting to start. This number may be smaller than
        # the actual number of vehicles still to come because of delayed
        # route file parsing.
        self._act(action)
        ldm.simulationStep()
        obs = self._observe()
        done = ldm.getMinExpectedNumber() <= 0
        global_reward = self._computeGlobalReward()

        return obs, global_reward, done, []
    
    def reset(self):
        print("Starting SUMO environment...")
        self._startSUMO()
        self.action_space = self._getActionSpace()
        self._state = LdmMatrixState(ldm,[self.parameters['box_bottom_corner'], self.parameters['box_top_corner']], "byCorners")
        
    def render(self):
        pass # enabled anwyay if parameter 'gui'=True
    
    def close(self):
        ldm.close()

    def seed(self):
        pass # TODO: Wouter: add seed (pass to LDM)

    ########## Private functions ##########################
    def _startSUMO(self):
        """
        Start the connection with SUMO as a subprocess and initialize
        the traci port, generate route file.
        """
        val='sumo-gui' if self.parameters['gui'] else 'gui'
        sumo_binary = checkBinary(val)
        
        # Try repeatedly to connect
        while True:
            try:
                scenario=os.path.expandvars(os.path.join(self.parameters['scenario'], 'scenario.sumocfg'))
                self.port = random.SystemRandom().choice(list(range(10000,20000)))
                sumoCmd=[sumo_binary, "-c", scenario]
                time.sleep(.500) 
                ldm.start(sumoCmd, self.port)
            except Exception as e:
                if str(e) == "connection closed by SUMO":
                    continue
                else:
                    raise
            else:
                break

        ldm.init(waitingPenalty=0,new_reward=0) # ignore reward for now
        ldm.setResolutionInPixelsPerMeter(self.parameters['resolutionInPixelsPerMeterX'], self.parameters['resolutionInPixelsPerMeterY'])
            
    def _checkScenario(self):
        """
        Checks if the scenario is well-defined and usable by seeing if all
        the needed files exist.
        @raise  Exception if required files not in specified scenario path: 
        """
        scenario_path = os.path.expandvars(self.parameters['scenario'])
        if not os.path.isdir(scenario_path):
            raise Exception ("Scenario path is not a directory:"+scenario_path)
        if not os.path.exists(scenario_path):
            raise Exception ("Scenario path does not exist:"+scenario_path)
        # TODO: remove route_file.txt, add *.sumocfg, *.rou.xml
        needed_files = ['route_file.txt', 'scenario.sumocfg']
        scenario_files = os.listdir(scenario_path)
        for n_file in needed_files:
            if n_file not in scenario_files:
                raise Exception("The scenario is missing file '{}' in {}, please add it and "
                      "try again.".format(n_file, scenario_path))

    def _act(self, action:spaces.Dict):
        """
        Set all PHASES as asked
        """
        for intersectionId,lightPhaseId in action.items():
            ldm.setRedYellowGreenState(intersectionId, self._intToPhaseString(intersectionId, lightPhaseId))
    
    def _intToPhaseString(self, intersectionId:str, lightPhaseId: int):
        """
        @param intersectionid the intersection(light) id
        @param lightvalue the PHASES value
        @return the intersection PHASES string eg 'rrGr' or 'GGrG'
        """
        return PHASES.get(lightPhaseId)
        
                
    def _observe(self): 
        """
        Fetches the Sumo state and converts in a proper gym observation.
        The keys of the dict are the intersection IDs (roughly, the trafficLights)
        The values are the state of the TLs
        """
        return self._state.update_state()

    def _computeGlobalReward(self):
        """
        Computes the global reward
        """
        return ldm.getRewardByCorners(bottomLeftCoords=(0,0), topRightCoords=(0,0), local_rewards=False)
    
    def _getActionSpace(self):
        """
        @returns the actionspace:
         two possible actions for each lightid: see PHASES variable
        """
        return spaces.Dict({id:spaces.Discrete(len(PHASES.keys())) for id in ldm.getTrafficLights()})


    def _set_actions(self, actions):
        """
        Take the specified actions in the environment
        @param actions a list of
        """
        actions = self._index_to_action(actions)

        for factor_i in range(self.n_factors):
            # action_i is the "local joint action" for the subset
            # of agents that participate in this component
            action_i = actions[factor_i]
            # Retrieve the action that was taken the previous step
            try:
                previous_action = self.taken_action[factor_i]
            except KeyError:
                # If KeyError, this is the first time an action has been taken
                previous_action = action_i

            agents_i = self.factor_graph.getFactors()[factor_i].getAgentIds()
            take_act = []
            for k, agent_j in enumerate(agents_i):
                take_act.append(action_i[k])
                # Check if the given action is different from the previous action
                if previous_action[k] != take_act[k]:
                    # Either the this is a true switch or coming grom yellow
                    take_act[k], self.yellow_dict[factor_i][agent_j] = self._get_action(previous_action[k],
                                                         take_act[k], self.yellow_dict[factor_i][agent_j], factor_i)
                # Set traffic lights 
                ldm.setRedYellowGreenState(agent_j, take_act[k])

            self.taken_action[factor_i] = take_act

    def _get_action(self, prev_action, action, timer, factor):
        """
        Check what we are going to do with the given action based on the
        previous action.
        """
        # Check if the agent was in a yellow state the previous step
        if 'y' in prev_action:
            # Check if this agent is in the middle of its yellow state
            if timer > 0:
                new_action = prev_action
                timer -= 1
            # Otherwise we can get out of the yellow state
            else:
                new_action = prev_action.replace('r', 'G')
                new_action = new_action.replace('y', 'r')
        # We are switching from green to red, initialize the yellow state
        else:
            new_action = prev_action.replace('G', 'y')
            timer = self.parameters['y_t'] - 1

        return new_action, timer


# TODO: Wouter: This should be read from a config file and different for each intersection ID
PHASES={
    0: "GGrr",
    1: "rrGG"
}


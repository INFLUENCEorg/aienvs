import gym
from gym import spaces
import os
from aienvs.LDM import ldm
import time
from sumolib import checkBinary
import random

class SumoGymAdapter(gym.Env):
    """
    An adapter that makes Sumo behave as a proper Gym environment.
    At top level, the actionspace and percepts are in a Dict with the
    trafficPHASES as keys.
    """

    def __init__(self,  parameters:dict={'gui':True, 'scenario':os.path.join('$AIENVS_HOME','scenarios/four_grid/')}):
        """
        @param path where results go, like "Experiment ID"
        @param parameters the configuration parameters.
        gui: whether we show a GUI. 
        scenario: the path to the scenario to use
        """
        self.parameters = parameters

        self._checkScenario()
        self.observation_space = self._getObservationSpace()
        self.reset()

    
    def step(self, action:spaces.Dict):
        # Ask SUMO the number of vehicles which are in the net plus the
        # ones still waiting to start. This number may be smaller than
        # the actual number of vehicles still to come because of delayed
        # route file parsing.
        self._act(action)
        ldm.simulationStep()
        obs=self._observe()
        done = ldm.getMinExpectedNumber() <= 0
        # We don't bother with the reward here, it's an agent job.
        return obs, 0.3, done, []
    
    def reset(self):
        print("Starting SUMO environment...")
        self._startSUMO()
        self.action_space = self._getActionSpace()
        
    def render(self):
        pass # enabled anwyay if parameter 'gui'=True
    
    def close(self):
        ldm.close()

    def seed(self):
        pass # todo?

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

        ldm.init(0,0) # ignore reward for now
        ldm.setResolutionInPixelsPerMeter(2,2)
            
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
            ldm.setRedYellowGreenState(intersectionId, self._intToPHASESString(intersectionId, lightPhaseId))
    
    def _intToPHASESString(self, intersectionId:str, lightPhaseId: int):
        """
        @param intersectionid the intersection(light) id
        @param lightvalue the PHASES value
        @return the intersection PHASES string eg 'rrGr' or 'GGrG'
        """
        return PHASES.get(lightPhaseId)
        
                
    def _observe(self): 
        """
        Fetches the ldm(sumo) observations and converts in a proper gym observation.
        The keys of the dict are the intersection IDs (roughly, the trafficPHASES)
        The values are the state of the TLs
        """
        #tlstates={id:self._PHASEStateToInt(id) for id in ldm.getTrafficPHASES()}
        return None
    

    def _getActionSpace(self):
        """
        @returns the actionspace:
         two possible actions for each lightid: see PHASES variable
        """
        return spaces.Dict({id:spaces.Discrete(len(PHASES.keys())) for id in ldm.getTrafficPHASES()})
    
    def _getObservationSpace(self):
        """
        @returns the observation:
         one observation for each lightid: see PHASES variable
        """
        return spaces.Dict({id:spaces.Discrete(2) for id in ldm.getTrafficPHASES()})
    

# This should be read from a config file and different for each intersection ID
PHASES={
    0: "GGrr",
    1: "rrGG"
}


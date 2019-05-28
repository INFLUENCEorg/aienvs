import gym
import logging
from gym import spaces
import os
from aienvs.Sumo.LDM import ldm
from aienvs.Sumo.SumoHelper import SumoHelper
from aienvs.Sumo.state_representation import *
import time
from sumolib import checkBinary
import random
from aienvs.Sumo.SumoHelper import SumoHelper
from aienvs.Environment import Env
import copy

class SumoGymAdapter(Env):
    """
    An adapter that makes Sumo behave as a proper Gym environment.
    At top level, the actionspace and percepts are in a Dict with the
    trafficPHASES as keys.
    """
    _DEFAULT_PARAMETERS = {'gui':True, 
                'scene':'four_grid', 
                'box_bottom_corner':(0,0), 
                'box_top_corner':(10,10),
                'resolutionInPixelsPerMeterX': 1,
                'resolutionInPixelsPerMeterY': 1,
                'y_t': 6,
                'car_pr': 0.5,
                'car_tm': 2,
                'route_starts' : [],
                'route_min_segments' : 0,
                'route_max_segments' : 0,
                'route_ends' : [],
                'seed' : 42,
                'generate_conf' : True,
                'libsumo' : False
                }
    
    # TODO: Wouter: This should be read from a file
    _PHASES={
        0: "GGrr",
        1: "rrGG"
    }

    def __init__(self, parameters:dict={}):
        """
        @param path where results go, like "Experiment ID"
        @param parameters the configuration parameters.
        gui: whether we show a GUI. 
        scenario: the path to the scenario to use
        """
        self._parameters = copy.deepcopy(self._DEFAULT_PARAMETERS)
        self._parameters.update(parameters)
        self.ldm=ldm(using_libsumo = self._parameters['libsumo'])
        logging.debug(parameters)
        self._takenActions = {}
        self._yellowTimer = {}
        self.seed()
        self.reset()
    
    def step(self, actions:spaces.Dict):
        # Ask SUMO the number of vehicles which are in the net plus the
        # ones still waiting to start. This number may be smaller than
        # the actual number of vehicles still to come because of delayed
        # route file parsing.
        self._set_lights(actions)
        self.ldm.step()
        obs = self._observe()
        done = self.ldm.isSimulationFinished()
        global_reward = self._computeGlobalReward()

        # as in openai gym, last one is the info list
        return obs, global_reward, done, []
    
    def reset(self):
        try:
            logging.debug("LDM closed by resetting")
            self.ldm.close()
        except:
            logging.debug("No LDM to close. Perhaps it's the first instance of training")

        logging.info("Starting SUMO environment...")
        self._startSUMO()
        self._action_space = self._getActionSpace()
        # TODO: Wouter: make state configurable ("state factory")
        self._state = LdmMatrixState(self.ldm,[self._parameters['box_bottom_corner'], self._parameters['box_top_corner']], "byCorners")
        
        #TODO: change the defaults to something sensible
    def render(self):
        import colorama
        colorama.init()
        def move_cursor(x,y):
            print ("\x1b[{};{}H".format(y+1,x+1))
        def clear():
            print ("\x1b[2J")
        clear()
        move_cursor(100,100)
        import numpy as np
        np.set_printoptions(linewidth=100)
        print(self._observe())
    
    def seed(self, seed=42):
        self._seed = seed
        pass # TODO: Wouter: add seed (pass to LDM)

    def close(self):
        self.__del__()

    # TODO: Wouter: this needs to return a space and be somehow unified with gym.spaces
    @property
    def observation_space(self):
        return self._state.update_state()

    @property
    def action_space(self):
        return self._action_space

    ########## Private functions ##########################
    def __del__(self):
        logging.debug("LDM closed by destructor")
        self.ldm.close()

    def _startSUMO(self):
        """
        Start the connection with SUMO as a subprocess and initialize
        the traci port, generate route file.
        """
        val='sumo-gui' if self._parameters['gui'] else 'sumo'
        sumo_binary = checkBinary(val)

        # Try repeatedly to connect
        while True:
            try:
                self._port = random.SystemRandom().choice(list(range(10000,20000)))
                self._sumo_helper = SumoHelper(self._parameters, self._port, self._seed)
                conf_file = self._sumo_helper.sumocfg_file
                logging.info( "Configuration: " + str(conf_file) )
                sumoCmd=[sumo_binary, "-c", conf_file]
                time.sleep(.500) 
                self.ldm.start(sumoCmd, self._port)
            except Exception as e:
                if str(e) == "connection closed by SUMO":
                    continue
                else:
                    raise
            else:
                break

        self.ldm.init(waitingPenalty=self._parameters['waiting_penalty'],new_reward=self._parameters['new_reward']) # ignore reward for now
        self.ldm.setResolutionInPixelsPerMeter(self._parameters['resolutionInPixelsPerMeterX'], self._parameters['resolutionInPixelsPerMeterY'])
        self.ldm.setPositionOfTrafficLights(self._parameters['lightPositions'])
            
    def _intToPhaseString(self, intersectionId:str, lightPhaseId: int):
        """
        @param intersectionid the intersection(light) id
        @param lightvalue the PHASES value
        @return the intersection PHASES string eg 'rrGr' or 'GGrG'
        """
        logging.debug("lightPhaseId" + str(lightPhaseId))
        return self._PHASES.get(lightPhaseId)
        
                
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
        return self._state.update_reward()
    
    def _getActionSpace(self):
        """
        @returns the actionspace:
         two possible actions for each lightid: see PHASES variable
        """
        return spaces.Dict({id:spaces.Discrete(len(self._PHASES.keys())) for id in self.ldm.getTrafficLights()})


    def _set_lights(self, actions:spaces.Dict):
        """
        Take the specified actions in the environment
        @param actions a list of
        """
        for intersectionId in actions.keys():
            action = self._intToPhaseString(intersectionId, actions.get(intersectionId))
            # Retrieve the action that was taken the previous step
            try:
                prev_action = self._takenActions[intersectionId][-1]
            except KeyError:
                # If KeyError, this is the first time any action was taken for this intersection
                prev_action = action
                self._takenActions.update( {intersectionId:[]} )
                self._yellowTimer.update( {intersectionId:0} )

            # Check if the given action is different from the previous action
            if prev_action != action:
                # Either the this is a true switch or coming grom yellow
                action, self._yellowTimer[intersectionId] = self._correct_action(prev_action, action, self._yellowTimer[intersectionId])

            # Set traffic lights 
            self.ldm.setRedYellowGreenState(intersectionId, action)
            self._takenActions[intersectionId].append(action)

    def _correct_action(self, prev_action, action, timer):
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
                new_action = action
        # We are switching from green to red, initialize the yellow state
        else:
            new_action = prev_action.replace('G', 'y')
            timer = self._parameters['y_t'] - 1

        return new_action, timer




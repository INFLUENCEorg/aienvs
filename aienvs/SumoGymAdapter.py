import gym
from gym import spaces
import os
from LDM import ldm
import time
from sumolib import checkBinary

class SumoGymAdapter(gym.Env):
	"""
	An adapter that makes Sumo behave as a proper Gym environment.
	At top level, the actionspace and percepts are in a Dict with the
	trafficlights as keys.
	"""

	def __init__(self,  parameters:dict={'gui':True, 'scenario':os.path.join(os.path.realpath("."),'scenarios/four_grid/')}):
		"""
		@param path where results go, like "Experiment ID"
		@param parameters the configuration parameters.
		gui: whether we show a GUI. 
		scenario: the path to the scenario to use
		"""
		self.parameters = parameters

		self._checkScenario()
		self.action_space = self._getActionSpace()
		self.observation_space = self._getObservationSpace()
		# default reward range is fine. We probably won't use it anyway.
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
		
		# Why is this loop? Try repeatedly to connect?
		while True:
			try:
				scenario=os.path.join(self.parameters['scenario'], 'scenario.sumocfg')
				#self.port = random.SystemRandom().choice(list(range(10000,20000)))
				sumoCmd=[sumo_binary, "-c", scenario]
				time.sleep(.500) # TODO remove??
				ldm.start(sumoCmd)
			except Exception as e:
				if str(e) == "connection closed by SUMO":
					continue
				else:
					raise
			else:
				break

		ldm.init(0,0) # ignore reward for now
		
		ldm.setResolutionInPixelsPerMeter(self.parameters['resolutionInPixelsPerMeterX'], self.parameters['resolutionInPixelsPerMeterY'])

			
	def _checkScenario(self):
		"""
		Checks if the scenario is well-defined and usable by seeing if all
		the needed files exist.
		@raise  Exception if required files not in specified scenario path: 
		"""
		scenario_path = self.parameters['scenario']
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
		Set all lights as asked
		"""
		for lightid,lightspace in action.spaces.items():
			ldm.setRedYellowGreenState(lightid, self._intToLightsString(lightspace))
	
	def _intToLightsString(self, intersectionid:str, lightvalue: int):
		"""
		@param intersectionid the intersection(light) id
		@param lightvalue the LIGHTS value
		@return the intersection lights string eg 'rrGr' or 'GGrG'
		"""
		# make list with "True" for horizontal lanes and "False" for verticals
		horizlanes=map(self.isHorizontal,  ldm.getControlledLanes(intersectionid))

		isHorizGreen = lightvalue==0
		# convert to list with 'G' for horizontal lanes if isHorizGreen and 'r' for verticals,
		# or vice versa if not isHorizGreen
		colors=map(lambda isLaneHoriz: ['r','G'][isLaneHoriz == isHorizGreen], horizlanes)
		
		return ''.join(colors)
		
				
	def _observe(self):	
		"""
		Fetches the ldm(sumo) observations and converts in a proper gym observation.
		The keys of the dict are the intersection IDs (roughly, the trafficlights)
		The values are the state of the TLs
		"""
		tlstates={id:self._lightStateToInt(id) for id in ldm.getTrafficLights()}
		return spaces.Dict(tlstates)
	

	
	def _lightStateToInt(self, lightid:str):
		"""
		Assumes that either all horizontal lights are green and verticals are red,
		or vice versa.
		@param lightid the light id (string)
		@return:  the LIGHTS state 
		"""
		isfirstLightGreen = ldm.getLightState(lightid)[0].lower() == 'g'
		isFirstLaneHorizontal = self._isHorizontal(ldm.getControlledLanes(lightid)[0])
		return 0 if isfirstLightGreen == isFirstLaneHorizontal else 1

	def _getActionSpace(self):
		"""
		@returns the actionspace:
		 two possible actions for each lightid: see LIGHTS variable
		"""
		return spaces.Dict({id:spaces.Discrete(2) for id in ldm.getTrafficLights()})
	
	def _getObservationSpace(self):
		"""
		@returns the observation:
		 one observation for each lightid: see LIGHTS variable
		"""
		return spaces.Dict({id:spaces.Discrete(2) for id in ldm.getTrafficLights()})
	
	def _isHorizontal(self, lane:str):
		"""
		Assumes the lane is a straight simple line from start to end. 
		@param  lane the lane id
		@return true iff the given lane id is a horizontal lane
		"""
		lane_coordinates = ldm.getLaneShape(lane)
		# if the x coordinates of the begin and end point of a lane are the same, the lane is vertical
		return lane_coordinates[0][1] == lane_coordinates[1][1]

# This is simplistic but the way our code works everywhere.
LIGHTS={
	0: "HORIZONTAL_GREEN",
	1: "VERTICAL_GREEN"
}


import os
import sys
import logging
import traci as SUMO_client
import numpy as np
import string

class LDM(SUMO_client.StepListener):
    '''
    An LDM (Local Dynamic Map) module contains the positions and other state attributes of dynamic objects
    in the simulation (vehicles, possibly also traffic lights)
    and adapts the vehicles in a platoon to change their controls accordingly.
    Usage -- as a module: from LDM import ldm (has to be imported after traci.start )
    Then call ldm.init()

    Public methods: getMapSliceByCorners( bottomLeftCoords, topRightCoords )
    getMapSliceByCenter( self, centerCoords, widthInMeters, heightInMeters )
    '''

    def __init__(self):
        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:
            raise ValueError("Environment variable SUMO_HOME is not set, "
                             "please declare it (e.g. in ~/.bashrc).")
        # should be added once only, otherwise multiple step listeners are created
        SUMO_client.addStepListener(self)
        self._lightids={}


    #TODO: Wouter: change all verbose prints to logging
    def init(self, waitingPenalty, new_reward, verbose=0):
        ''' LDM()

        Creates and initializes the Local Dynamic Map
        Call after traci has connected
        '''
        self.__optimize=False #set True to disable non-optimized public functions
        self.netBoundaryMeters=list(SUMO_client.simulation.getNetBoundary())
        self.netBoundaryMetersLL=list([self.netBoundaryMeters[0][0]-10, self.netBoundaryMeters[0][1]-10])
        self.netBoundaryMetersUR=list([self.netBoundaryMeters[1][0]+10, self.netBoundaryMeters[1][1]+10])
        self.netBoundaryMeters=list( [tuple(self.netBoundaryMetersLL), tuple(self.netBoundaryMetersUR)] )


        self._verbose=verbose
        self._lightids=SUMO_client.trafficlight.getIDList()
        self._subscribeToTrafficLights()
        self._lightstate={}
        self._tlPositions={}
        self._waitingPenalty = waitingPenalty
        self.new_reward = new_reward

    def start(self, sumoCmd:list, PORT):
        """
        @param sumoCmd the sumo command for the start, list of init arguments
        """
        print("Sumo command:" + str(sumoCmd))
        SUMO_client.start(sumoCmd, port=PORT)
        
        
    def step(self, t=0):
        '''
        This updates the vehicles' states with information from the simulation
        '''
        for newID in SUMO_client.simulation.getDepartedIDList():
            if( self._verbose ):
                print(newID)
            self._addVehicleSubscription(newID)

        self.subscriptionResults = SUMO_client.vehicle.getAllSubscriptionResults()
        self._updateMapWithVehicles( self._getVehiclePositions(self.subscriptionResults) )
        self._updateTrafficLights(SUMO_client.trafficlight.getAllSubscriptionResults())

        if(self._lightids != None):
            for lightid in self._lightids:
                if(self._tlPositions.get(lightid) != None):
                    self._add_stop_lights(self._lightstate[lightid], list(self._tlPositions.get(lightid)) )


        return True
    
    def simulationStep(self):
        """
        Let the simulator make a step.
        """
        SUMO_client.simulationStep()

    def close(self):
        """
        close sumo env
        """
        SUMO_client.close()

    def isSimulationFinished(self):
        """
        @return minimum number of vehicles that are still expected to leave the net (id 0x7d) 
        """
        return (SUMO_client.simulation.getMinExpectedNumber() <= 0)



    def getRewardByCorners(self, bottomLeftCoords, topRightCoords, local_rewards):
        vehicles = self.subscriptionResults
        filteredVehicles = vehicles.copy()
        if local_rewards:
            for vehID in vehicles:
                position = vehicles.get(vehID).get(SUMO_client.constants.VAR_POSITION)

                if(position[0] < bottomLeftCoords[0]):
                    filteredVehicles.pop(vehID)
                    continue
                if(position[0] > topRightCoords[0]):
                    filteredVehicles.pop(vehID)
                    continue
                if(position[1] < bottomLeftCoords[1]):
                    filteredVehicles.pop(vehID)
                    continue
                if(position[1] > topRightCoords[1]):
                    filteredVehicles.pop(vehID)
                    continue

        return self._computeReward( filteredVehicles )

    def getRewardByCenter( self, centerCoords, widthInMeters, heightInMeters ):
        vehicles = self.subscriptionResults
        filteredVehicles = vehicles.copy()
        for vehID in vehicles:
            position = vehicles.get(vehID).get(SUMO_client.constants.VAR_POSITION)

            if(position[0] < centerCoords[0] - heightInMeters/2.):
                filteredVehicles.pop(vehID)
                continue
            if(position[0] > centerCoords[0] + heightInMeters/2.):
                filteredVehicles.pop(vehID)
                continue
            if(position[1] < centerCoords[1] - widthInMeters/2.):
                filteredVehicles.pop(vehID)
                continue
            if(position[1] > centerCoords[0] + widthInMeters/2.):
                filteredVehicles.pop(vehID)
                continue

        return self._computeReward( filteredVehicles )

    def getMapSliceByCorners( self, bottomLeftCoords, topRightCoords ):
        bottomLeftMatrixCoords = self._coordMetersToArray( bottomLeftCoords )
        topRightMatrixCoords = self._coordMetersToArray( topRightCoords )
        return self._arrayMap[bottomLeftMatrixCoords[0]:(topRightMatrixCoords[0]), bottomLeftMatrixCoords[1]:(topRightMatrixCoords[1])].transpose()[::-1]

    def getMapSliceByCenter( self, centerCoords, widthInMeters, heightInMeters ):
        bottomLeftCoords = (centerCoords[0] - widthInMeters/2., centerCoords[1] - heightInMeters/2.)
        topRightCoords = (centerCoords[0] + widthInMeters/2., centerCoords[1] + heightInMeters/2.)
        return self.getMapSliceByCorners( bottomLeftCoords, topRightCoords )

    def setResolutionInPixelsPerMeter( self, pixelsPerMeterWidth, pixelsPerMeterHeight ):
        self._pixelsPerMeterWidth=pixelsPerMeterWidth
        self._pixelsPerMeterHeight=pixelsPerMeterHeight
        self._initializeArrayMap()

    def setResolutionInMetersPerPixel( self, metersPerPixelWidth, metersPerPixelHeight ):
        self.setResolutionInPixelsPerMeter( 1./metersPerPixelWidth, 1./metersPerPixelHeight )

    def setPositionOfTrafficLights( self, lightsPositions ):
        for lightID in lightsPositions.keys():
            self.setPositionOfTrafficHeads( lightID, lightsPositions.get(lightID) )

    def setPositionOfTrafficHeads( self, lightID, positionsInMeters ):
        self._tlPositions[lightID] = positionsInMeters

    ######## getting trafficlight info. Maybe move to TrafficLight object #######
    def getTrafficLights(self):
        """
        @return the list[string] of all traffic light ids
        """
        return self._lightids

    def getLightState(self, tlid):
        """
        @param tlid the id of a traffic light
        @return the state of the traffic light with given tlid
        """
        return self._lightstate[tlid]

    ######## getting lane info. Maybe move to Map object #######
    def getControlledLanes(self, lightid:str):
        """
        @param lightid the id of the traffic light
        @return the lanes controlled by the given lightid
        """
        self._checkOptimize()
        return SUMO_client.trafficlight.getControlledLanes(lightid)

    def getLaneMaxSpeed(self, laneid:str):
        """
        @param lane the id of a lane
        @return the maximum speed on the lane
        """
        self._checkOptimize()
        SUMO_client.lane.getMaxSpeed(laneid)

    def getLaneShape(self, laneid:str):
        """
        @param lane the id of a lane
        @return the shape of the lane
        """
        self._checkOptimize()
        SUMO_client.lane.getShape(laneid)

    def getLaneVehicles(self, laneid:str):
        """
        @param lane the id of a lane
        @return the vehicles on this lane
        """
        self._checkOptimize()
        return SUMO_client.lane.getLastStepVehicleIDs(laneid)

    ######## getting vehicle info. Maybe move to Vehicle object #######
    def getVehicles(self):
        """
        @return the list[string] of vehicle ids
        """
        return self.subscriptionResults.keys()

    def getVehicleLane(self, vehicleid:str):
        """
        @param vehicleid the id of the vehicle
        @return  the lane id where the vehicle is at this time
        """
        self._checkOptimize()
        return SUMO_client.vehicle.getLaneID(vehicleid)

    def getVehicleWaitingTime(self,vehicleid:str):
        """
        @param vehicleid the id of the vehicle
        @return  the waiting time of the vehicle
        """
        self._checkOptimize()
        return SUMO_client.vehicle.getWaitingTime(vehicleid)

    def getVehicleCO2Emission(self, vehicleid:str):
        """
        @param vehicleid the id of the vehicle
        @return vehicle co2 emission
        """
        self._checkOptimize()
        return SUMO_client.vehicle.getCO2Emission(vehicleid)
    
    def getFuelConsumption(self, vehicleid):
        """
        @param vehicleid the id of the vehicle
        @return vehicle fuel consumption
        """
        self._checkOptimize()
        return SUMO_client.vehicle.getFuelConsumption(vehicleid)
    
    
    
    def getSpeed(self, vehicleid):
        """
        @param vehicleid the id of the vehicle
        @return  the current speed of the vehicle
        """
        self._checkOptimize()
        return SUMO_client.vehicle.getSpeed(vehicleid)

    def getVehicleMaxSpeed(self, vehicleid):
        """
        @param vehicleid the id of the vehicle
        @return  the maximum speed of the vehicle
        """
        self._checkOptimize()
        return SUMO_client.vehicle.getMaxSpeed(vehicleid)

    def getVehicleAllowedSpeed(self, vehicleid):
        """
        @param vehicleid the id of the vehicle
        @return  the allowed speed of the vehicle
        """
        return self.subscriptionResults.get(vehicleid).get(SUMO_client.constants.VAR_ALLOWED_SPEED)

    def getVehiclePosition(self, vehicleid):
        """
        @param vehicleid the id of the vehicle
        @return  the position of the vehicle, unscaled, as in the sumo map
        """
        self._checkOptimize()
        return SUMO_client.vehicle.getPosition(vehicleid)

    def getStartingTeleportNumber(self) :
        """
        @return unknown
        """
        return SUMO_client.simulation.getStartingTeleportNumber()
    ########################## private functions ##############################

    def _subscribeToTrafficLights(self):
        logging.info("LightID subscriptions" + str(self._lightids))
        for lightid in self._lightids:
            SUMO_client.trafficlight.subscribe(lightid, (SUMO_client.constants.TL_RED_YELLOW_GREEN_STATE, SUMO_client.constants.TL_CURRENT_PHASE))

    def _initializeArrayMap( self ):
        if( self._verbose ):
            print( self.netBoundaryMeters[1] )
            print( self.netBoundaryMeters[0] )

        self._arrayMap=np.zeros( self._coordMetersToArray(tuple(( self.netBoundaryMeters[1][0], self.netBoundaryMeters[1][1] )) ) )

    def _resetMap( self ):
        self._arrayMap = np.zeros( self._arrayMap.shape )

    def _coordMetersToArray( self, *coordsInMeters ):
        arrayX = round( (coordsInMeters[0][0] - self.netBoundaryMeters[0][0]) * self._pixelsPerMeterWidth - 0.5 )
        arrayY = round( (coordsInMeters[0][1] - self.netBoundaryMeters[0][1]) * self._pixelsPerMeterHeight - 0.5 )
        return [arrayX, arrayY]

    def _addVehicleSubscription(self, vehID):
        SUMO_client.vehicle.subscribe(vehID, (SUMO_client.constants.VAR_POSITION, SUMO_client.constants.VAR_SPEED, SUMO_client.constants.VAR_ALLOWED_SPEED, SUMO_client.constants.VAR_WAITING_TIME ))
        if( self._verbose ):
            print("New vehicle " + vehID)

    def _updateMapWithVehicles( self, floatingCarData ):
        self._resetMap()
        for vehCoords in floatingCarData:
            vehCoordsInArray=self._coordMetersToArray(vehCoords)
            try:
                self._arrayMap[vehCoordsInArray[0], vehCoordsInArray[1]] = self._arrayMap[vehCoordsInArray[0], vehCoordsInArray[1]] + 1
            except IndexError as error:
                print(error)

    # vehicles are a subset of all subscription results
    def _computeReward( self, vehicles ):
        result = 0
        for vehID in vehicles:
            if self.new_reward:
                waitingTime = vehicles.get(vehID).get(SUMO_client.constants.VAR_WAITING_TIME)
                reward = -min(waitingTime, 1.0)
            else:
                if self._waitingPenalty:
                    waitingTime = vehicles.get(vehID).get(SUMO_client.constants.VAR_WAITING_TIME)
                speed = vehicles.get(vehID).get(SUMO_client.constants.VAR_SPEED)
                allowedSpeed = vehicles.get(vehID).get(SUMO_client.constants.VAR_ALLOWED_SPEED)

                if( self._verbose ):
                    if self._waitingPenalty:
                        print(vehID + " waitingTime " + str(waitingTime) + " speed " + str(speed) + " allowedSpeed " + str(allowedSpeed))
                    else:
                        print(vehID + " speed " + str(speed) + " allowedSpeed " + str(allowedSpeed))

                if self._waitingPenalty:
                    clippedWaitingTime = min(waitingTime, 1.0) #min(waitingTime*0.5, 1.0)
                    clippedDelay = max(0, 1 - speed/allowedSpeed)
                    reward = - 0.5*clippedDelay - 0.5*clippedWaitingTime
                else:
                    clippedDelay = max(0, 1 - speed / allowedSpeed)
                    reward = -clippedDelay

                if( self._verbose ):
                    if self._waitingPenalty:
                        print(vehID + " clippedWaitingTime " + str(clippedWaitingTime) + " clippedDelay " + str(clippedDelay) + " reward " + str(reward))
                    else:
                        print(vehID) + " clippedDelay " + str(clippedDelay) + " reward " + str(reward)

            result += reward
        return result

    def _getVehiclePositions( self, subscriptionResults ):
        resultsFormatted=list(subscriptionResults.values())
        positionList = list()

        for vehAttrib in resultsFormatted:
            position = (round(vehAttrib[SUMO_client.constants.VAR_POSITION][0]), round(vehAttrib[SUMO_client.constants.VAR_POSITION][1]))
            if(self._verbose):
                print("Position " + str(position))
            positionList.append(position)
        return positionList

    def _getLaneEnds( self, subscriptionResults ):
        resultsFormatted=list(subscriptionResults.values())
        positionList = list()

        for vehAttrib in resultsFormatted:
            position = (round(vehAttrib[SUMO_client.constants.VAR_POSITION][0]), round(vehAttrib[SUMO_client.constants.VAR_POSITION][1]))
            if(self._verbose):
                print("Position " + str(position))
            positionList.append(position)
        return positionList

    def _updateTrafficLights(self, lightupdates):
        """
        update the trafficlights cache
        I guess the lightupdate is according to https://sumo.dlr.de/wiki/TraCI/Traffic_Lights_Value_Retrieval
        """

        for lightid in lightupdates:
            lightstate = lightupdates[lightid][SUMO_client.constants.TL_RED_YELLOW_GREEN_STATE]
            if(self._verbose):
                print("Light " + lightid + "=" + lightstate)
            self._lightstate[lightid] = lightstate;


    def _add_stop_lights(self, lights, position):
        """
        Add the right value for the state of the traffic light at the right
        position in the matrix.
        Keyword arguments:
            state_matrix -- the matrix in which the values are stores
            light_color  -- a tuple containing the state of the traffic light
            position     -- a tuple containing the traffic light position
            traci        -- instance of TraCI to communicate with SUMO
        """
        index = 0
        for index in range(len(lights)):
            if lights[index] == 'G':
                val = 0.8
            elif lights[index] == 'y':
                val = 0.5
            elif lights[index] == 'r':
                val = 0.2

            arrayPosition = self._coordMetersToArray( position[index] )
            self._arrayMap[arrayPosition[0], arrayPosition[1]] += val
            index += 1
            
    def setRedYellowGreenState(self, agent:string, state:string ):
        self._checkOptimize()
        """
        set new state for a traffic  light
        @param agent the agent id
        @param state the new state eg "GrGr"
        """
        SUMO_client.trafficlight.setRedYellowGreenState(agent, state)

    def test(self, bottomLeftCoord = (506., 430.), topRightCoord = (516., 500.), centerCoord = (510., 475.), width = 10., height=70. ):
        #mapSlice=str(self.getMapSliceByCorners( bottomLeftCoord, topRightCoord ))
        mapSlice=str(self.getMapSliceByCenter( centerCoord, width, height ))
        #for visualization only
        """
        import colorama
        colorama.init()
        def move_cursor(x,y):
            print ("\x1b[{};{}H".format(y+1,x+1))
        def clear():
            print ("\x1b[2J")
        clear()
        move_cursor(100,100)
        """
        logging.debug(mapSlice)

    def _checkOptimize(self):
        if self.__optimize:
            raise Exception("optimized/cached code not yet implemented. Turn off optimize as workaround")

#For importing ldm as a module: from LDM import ldm
ldm = LDM()

import logging
from gym import spaces
from aienvs.Environment import Env
from numpy import set_printoptions, transpose, zeros
from numpy import array, dstack, ndarray
import copy
from random import Random
from numpy.random import seed as npseed
from numpy.random import choice as weightedchoice
import time
import random
import pdb
import numbers
from aienvs.gym.CustomObjectSpace import CustomObjectSpace
from aienvs.BasicMap import BasicMap
from aienvs.PredatorPrey.PredatorPreyState import PredatorPreyState
from aienvs.PredatorPrey.Predator import Predator
from aienvs.PredatorPrey.Prey import Prey

USE_PossibleActionsSpace = False


class PredatorPreyEnv(Env):
    """
    The predator-prey environment. 
    This is a generalization from https://arxiv.org/pdf/1910.00091.pdf section 5.1
    The map in the original paper is 10x10 without obstacles. 
    There are M entities on the map, hunting for N prey.
    The map can contain obstacles that neither hunters nor prey can step on.
    Each entity ('agent' in the paper) can move in 1 of 4 compass directions,
    remain still, to try to catch adjacent prey.
    Impossible actions, ie moves into an occupied target position or
    catching when there is no adjacent prey, are treated as unavailable
    (unavailable means ignored in this implementation)
    The prey moves by randomly selecting one available movement,
    or remains motionless if all surrounding positions are occupied.
    If two adjacent agents execute the catch action, a prey is caught 
    and both the prey and the catching agents are removed from the grid.
    FIXME explain this.
    An agent's observation is a 5x5 sub-grid centered around it, with one channel
    showing entities and another indicating prey.  FIXME explain channels.
    Removed entities and prey are no longer visible and removed entities receive
    a special observation of all zeros. FIXME zeroes?
    An episode ends if all entities have been removed or after STEPS time steps. 
    Capturing a prey is rewarded r=10, but unsuccessful attempts by single 
    entities are punished by a negative reward p.
    
    The following parameters can be used:
    * p: the punishment/reward, added for unsuccessful captures. defaults to 0.
     should be negative to really act as a punishment.
    * steps: Max number of time steps of the env. defaults to 200.
    * predators: a list of dicts. Each dict contains 'id' (unique entity label)
     and 'pos' with list [X,Y] where X,Y is the initial position of the entity
    * map: the BasicMap on which the game is played, see BasicMap.
    * 
    """
    DEFAULT_PARAMETERS = {'steps':200,
                'p':0,
                'predators':[ {'id': "predator1", 'pos':[3, 4]}, {'id': "predator2", 'pos': 'random'}],  # initial predator positions
                'preys':[ {'id': "prey1", 'pos':[7, 1]}, {'id': "prey2", 'pos': 'random'}],  # initial prey positions
                'seed':None,
                'map':['..........',
                       '..........',
                       '..........',
                       '..........',
                       '..........',
                       '..........',
                       '..........',
                       '..........',
                       '..........',
                       '..........']
                }

    #notice actions 0-4 are same as MovableItemOnMap
    ACTIONS = {
        0: "UP",
        1: "DOWN",
        2: "LEFT",
        3: "RIGHT",
        4: "CATCH"
    }   

    def __init__(self, parameters:dict={}):
        """
        init 
        @param parameters the env settings, see the default settings above. 
        """
        self._parameters = copy.deepcopy(self.DEFAULT_PARAMETERS)
        self._parameters.update(parameters)
        self.seed(self._parameters['seed'])

        predators = [Predator(p['id'], ndarray(p['pos'], True)) for p in self._parameters['predators']]
        preys = [Prey(p['id'], ndarray(p['pos'], True)) for p in self._parameters['preys']]
        map = BasicMap(self._parameters['map'])
        self._state = PredatorPreyState(predators, preys, map, 0, 0, parameters['steps'])

        self._actSpace = spaces.Dict({pred.getId():spaces.Discrete(len(self.ACTIONS)) \
                                      for pred in self._state.getPredators()})

    # Override
    def step(self, actions:dict):
        s=self._state
        if s.isFinal() or (not actions):
            return s, s.getReward(), s.isFinal(),[]

        self._stepSurvival(actions)
        self._stepPredatorActs(actions)
        self._stepPrey()
        self._state = self._state.increment()
        
        s=self._state
        return s, s.getReward(), s.isFinal(),[]
    
    def reset(self):
        self.__init__(self._parameters)
        return copy.deepcopy(self._state)  # should return initial observation

    #Override
    def render(self, delay=0.0, overlay=False):
        if overlay:
            import colorama
            colorama.init()

            def move_cursor(x, y):
                print ("\x1b[{};{}H".format(y + 1, x + 1))

            def clear():
                print ("\x1b[2J")

            clear()
            move_cursor(100, 100)
            set_printoptions(linewidth=100)
        bitmap = self._createBitmap()
        print(transpose(bitmap[:, :, 0] - bitmap[:, :, 1]))
        time.sleep(delay)

    # Override
    def close(self):
        pass  

    # Override
    def seed(self, seed):
        self._parameters['seed'] = seed
        if isinstance(self._parameters['seed'], numbers.Number):
            npseed(self._parameters['seed'])
        random.seed(seed)

    def getState(self) -> PredatorPreyState:
        return self._state

    def setState(self, newState:PredatorPreyState):
        self._state = newState  # no copy needed, immutable

    @property
    def observation_space(self):
        return CustomObjectSpace(self._state);

    @property
    def action_space(self):
        if USE_PossibleActionsSpace:
            actSpace = spaces.Dict({robotId:PossibleActionsSpace(self, robot) 
                for robotId, robot in self._state.robots.items()})
        else:        
            actSpace = self._actSpace
        return actSpace
            
    ########## Getters ###############################
    
    def getMap(self):
        """
        @return: the map of this floor
        """
        return copy.deepcopy(self._state.getMap())

    def getPart(self, area:ndarray):  # -> FactoryFloor
        """
        @param area a numpy array of the form [[xmin,ymin],[xmax,ymax]]. 
        @return: A new FactoryFloor with same settings as this, but
        with Map#getPart(area) of this map, and only those bots and tasks that 
        are in that area. The new factoryfloor is completely independent of this floor.
        """
        if(int(self._parameters["N_task_appears"]) > 1):
            raise Exception("Multiple task appears not supported for getting part of the map")

        parameters = copy.deepcopy(self._parameters)
        newmap = self._state.getMap().getPart(area)
        parameters['map'] = newmap.getFullMap()
        parameters['robots'] = [\
            { 'id':robot.getId(), 'pos':robot.getPosition().tolist() }\
            for robot in self._state.robots.values() if self._state.getMap().isInside(robot.getPosition())]
        parameters['tasks'] = [task.getPosition().tolist() \
            for task in self._state.tasks if self._state.getMap().isInside(task.getPosition())]
        parameters['P_task_appears'] = newmap.getTaskProbability()
        return FactoryFloor(parameters)
  
    def isPossible(self, robot:FactoryFloorRobot, action):
        """
        @param robot a FactoryFloorRobot
        @param action (integer) the action to be performed
        @return: true iff the action will be possible (can succeed) at this point.
        ACT is considered possible if there is a task at the current position.
        """
        pos = robot.getPosition()
        if action == 0:  # ACT
            return self._getTask(pos) != None
        return self._isFree(self._newPos(pos, action))
        
    def getPossibleActions(self, robot:FactoryFloorRobot):
        """
        @return the possible actions for the given robot on the floor
        """
        return [action for action in self.ACTIONS if self.isPossible(robot, action)]

    ########## Private functions ##########################


    def _stepPrey(self):
        """
        Let the active preys make their step
        """
        for prey in self._state.getPreys() :
            if prey.isActive():
                self._state=self._state.withPreyStep(prey, random.choice(range(4)))
        
    
    def _stepPredatorActs(self, actions:dict):
        """
        Do the actions of all predators and update state accordingly.
        It is assumed that all succesful 'catch' actions
        have been executed already.
        """
        for predator in self._state.getPredators() :
            if not predator.isActive():
                continue
            act = actions[predator.getId()]
            if ACTIONS[act]=='CATCH':
                self._state=self._state.withPenalty(self._parameters['p'])
            else # a step action. 
                self._state = self._state.withStep(predator, act )

    def _stepSurvival(self, actions:dict):
        """
        check survival of all preys. Removes all caught prey and their predators from state
        """
        #Copy the list as we are going to modify state
        preys = self._state.getPreys() 
        for prey in preys: 
            adjacent=self._adjacentPredators(prey.getPosition())
            adjacent = filter(lambda adj: self.ACTIONS[actions[adj]] == 'CATCH', adjacent)
            if len(adjacent)>=2:
                # remove prey and first two that catch it 
                self._state = self._state.withCatch(prey, adjacent[0], adjacent[1]) 
        
    
    
    def _adjacentPredators(self, pos:ndarray) -> List[Predator]:
        """
        @param pos a ndarray with some [x,y] position on the map
        @return all active predators that are directly N,E,S or W from given pos
        """
        return filter(lambda pred: pred.isAdjacent(pos) and pred.isActive(), \
                       self._state.getPredators() )

    def _createBitmap(self):
        map = self._state.getMap()
        bitmapRobots = zeros((map.getWidth(), map.getHeight()))
        bitmapTasks = zeros((map.getWidth(), map.getHeight()))
        for robot in self._state.robots.values():
            pos = robot.getPosition()
            bitmapRobots[pos[0], pos[1]] += 1

        for task in self._state.tasks:
            pos = task.getPosition()
            bitmapTasks[pos[0], pos[1]] += 1

        return dstack((9 * bitmapRobots, bitmapTasks))

    def _applyAction(self, pred:Predator, action) -> PredatorPreyState:
        """
        predator tries to execute given action.
        @param robot a FactoryFloorRobot
        @param action the ACTION number. 
        """
        actstring = self.ACTIONS.get(action)
        randNo = random.random()
        try:
            # first check for individual success probabilities
            pSucceed = self._parameters['P_action_succeed'][pred.getId()][actstring]
        except KeyError:
            # then use common ones
            pSucceed = self._parameters['P_action_succeed'][actstring]

        if randNo > pSucceed:
            return False

        pos = robot.getPosition()
        
        if actstring == "ACT":
            newpos = pos
            task = self._getTask(newpos)
            if task != None:
                self._state.tasks.remove(task)
                # logging.debug("removed " + str(task))
        else:  # move
            newpos = self._newPos(pos, action)
            if self._isFree(newpos):
                robot.setPosition(newpos)
  
    def _newPos(self, pos:ndarray, action):
        """
        @param pos the current (old) position of the robot (numpy array)
        @param action the action to be done in given position
        @return:  what would be the new position (ndarray) if robot did action.
        This does not check any legality of the new position, so the 
        position may run off the map or on a wall.
        """
        newpos = pos
        if self.ACTIONS.get(action) == "DOWN":
            newpos = pos + [0, 1]
        elif self.ACTIONS.get(action) == "RIGHT":
            newpos = pos + [1, 0]
        elif self.ACTIONS.get(action) == "UP":
            newpos = pos + [0, -1]
        elif self.ACTIONS.get(action) == "LEFT":
            newpos = pos + [-1, 0]
        return newpos
    
    def _getFreeMapPosition(self):
        """
        @return:random map position (x,y) that is not occupied by robot or wall.
        """
        while True:
            pos = self._state.getMap().getRandomPosition()
            if self._isFree(pos):
                return pos

    def _isRobot(self, position:ndarray):
        """
        @param position a numpy ndarray [x,y] that must be checked
        @return: true iff a robot occupies position
        """        
        for robot in self._state.robots.values():
            if (position == robot.getPosition()).all():
                return True
        return False

    def _isFree(self, pos:ndarray):
        """
        @return true iff the given pos has space for a robot,
        so it must be on the map and not on a wall and possibly
        not already containing a robot
        """
        map = self._state.getMap()
        return map.isInside(pos) and map.get(pos) != "*" \
            and (self._parameters['allow_robot_overlap'] or not(self._isRobot(pos)))
        
    def _addTask(self):
        """
        Add one new task to the task pool
        """
        themap = self._state.getMap()
        poslist = list(themap.getTaskPositions())
        if not self._parameters['allow_task_overlap']:
            if len(self._state.tasks) >= len(poslist):
                return

        # samplingSpace = spaces.MultiDiscrete([self._parameters['x_size'], self._parameters['y_size']])
        while True:  # do until newpos is not yet tasked, or task overlap allowed
            # work around numpy bug when list contains tuples
            weights = list(themap.getTaskWeights())
            i = weightedchoice(list(range(len(poslist))), 1, p=weights)[0]
            newpos = poslist[i]
            if self._parameters['allow_task_overlap'] or self._getTask(newpos) == None:
                break;

        self._state.addTask(FactoryFloorTask(newpos))

    def _getTask(self, pos:tuple):
        """
        @return task at given position, or None if no task at position
        """
        for task in self._state.tasks:
            if (task.getPosition() == pos).all():
                return task
        return None

    def _computePenalty(self):
        penalty = 0
        for task in self._state.tasks:
            penalty += 1
        return penalty


class PossibleActionsSpace(FixedActionsSpace):
    """
    A gym space that returns the possible actions at this moment
    on the factory floor for some robot.
    REQUIREMENT: at all times, at least one action must be possible.
    If not, sample() may raise an exception
    NOTE this class is very tightly coupled to FactoryFloor.
    @param thefloor: the FactoryFloor
    @param bot: the FactoryFloorRobot
    """

    def __init__(self, fl:FactoryFloor, bot:FactoryFloorRobot):
        super().__init__()
        self._floor = fl
        self._robot = bot
    
    # Override
    def sample(self):
        return random.choice(self._floor.getPossibleActions(self._robot))
 
    # Override       
    def contains(self, act):
        return self._floor.isPossible(self._robot, act)
    
    # Override
    def getAllActions(self) -> dict:
        return self._floor.ACTIONS
    

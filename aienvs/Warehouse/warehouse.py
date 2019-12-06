from warehouseItem import WarehouseItem
from warehouseRobot import WarehouseRobot
from warehouseState import WarehouseState
from utils import *
from aienvs.Environment import Env
import numpy as np
import copy
import random
from gym import spaces
from aienvs.gym.CustomObjectSpace import CustomObjectSpace


class Warehouse(Env):
    """
    warehouse environment
    """


    def __init__(self, parameters:dict={}):
        parameters = read_parameters('warehouse')
        self.n_columns = parameters['n_columns']
        self.n_rows = parameters['n_rows']
        self.n_robots_row = parameters['n_robots_row']
        self.n_robots_column = parameters['n_robots_column']
        self.distance_between_shelves = parameters['distance_between_shelves']
        self.robot_domain_size = parameters['robot_domain_size']
        self.prob_item_appears = parameters['prob_item_appears']
        # The learning robot
        self.learning_robot_id = parameters['learning_robot_id']
        self.max_n_items = parameters['max_n_items']
        self.items = None
        self.reset()

    ############################## Override ###############################

    def reset(self):
        """
        Resets the environment's state
        """
        self.robot_id = 0
        self.robots = self._place_robots()
        self.item_id = 0
        self.items = self._add_items()
        obs = self._get_observations()
        return obs

    def step(self, actions):
        """
        Performs a single step in the environment.
        """
        self._robots_act(actions)
        reward = self._compute_reward(self.robots[self.learning_robot_id])
        self._remove_items()
        self._add_items()
        obs = self._get_observations()
        # Check whether learning robot is done
        done = self.robots[self.learning_robot_id].done
        if done is True:
            # Reset the environment to start a new episode.
            self.reset()
        return obs, reward, done, []

    def observation_space(self):
        pass

    def action_space(self):
        """
        Returns A gym dict containing the number of action choices for all the
        agents in the environment
        """
        actions = {0: 'UP',
                   1: 'DOWN',
                   2: 'LEFT',
                   3: 'RIGHT'}
        n_actions = spaces.Discrete(len(actions))
        action_dict = {robot.get_id():n_actions for robot in self.robots}
        action_space = spaces.Dict(action_dict)
        return action_space

    def render(self, delay=0.0, overlay=False):
        """
        Renders the environment
        """
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

    def close(self):
        pass

    def seed(self, seed=None):
        if seed is not None:
            np.seed(seed)
            random.seed(seed)

    ######################### Private Functions ###########################

    def _place_robots(self):
        """
        Sets robots initial position at the begining of every episode
        """
        robots = []
        for i in range(self.n_robots_row):
            for j in range(self.n_robots_column):
                robot_domain = [i*self.robot_domain_size[0],
                                j*self.robot_domain_size[1],
                                (i+1)*self.robot_domain_size[0],
                                (j+1)*self.robot_domain_size[1]]
                robot_position = [robot_domain[0] + self.robot_domain_size[0]//2,
                                  robot_domain[1] + self.robot_domain_size[1]//2]
                robots.append(WarehouseRobot(self.robot_id, robot_position,
                                             robot_domain, self.max_n_items))
                self.robot_id += 1
        return robots

    def _add_items(self):
        """
        Add new items to the designated locations in the environment which
        need to be collected by the robots
        """
        items = []
        item_columns = np.arange(0, self.n_columns)
        item_rows = np.arange(0, self.n_rows, self.distance_between_shelves)
        item_locs = None
        if self.items is not None:
            item_locs = [item.get_position() for item in self.items]
        for row in item_rows:
            for column in item_columns:
                loc = [row, column]
                loc_free = True
                if item_locs is not None:
                    loc_free = loc not in item_locs
                if random.random() < self.prob_item_appears and loc_free:
                    items.append(WarehouseItem(self.item_id, loc))
                    self.item_id += 1
        return items

    def _get_state(self):
        """
        Generates a 3D bitmap: First layer shows the location of every item.
        Second layer shows the location of the robots.
        """
        state_bitmap = np.zeros([self.n_rows, self.n_columns, 2], dtype=np.int)
        for item in self.items:
            item_pos = item.get_position()
            state_bitmap[item_pos[0], item_pos[1], 0] = 1
        for robot in self.robots:
            robot_pos = robot.get_position()
            state_bitmap[robot_pos[0], robot_pos[1], 1] = 1

        return state_bitmap

    def _get_observations(self):
        """
        Generates the individual observation for every robot given the current
        state and the robot's designated domain.
        """
        observations = []
        state = self._get_state()
        for robot in self.robots:
            observations.append(robot.observe(state))
        return observations

    def _robots_act(self, actions):
        """
        All robots take an action in the environment.
        """
        for action,robot in zip(actions, self.robots):
            robot.act(action)

    def _compute_reward(self, robot):
        """
        Computes reward for the learning robot.
        """
        reward = -0.1
        robot_pos = robot.get_position()
        for item in self.items:
            item_pos = item.get_position()
            if robot_pos[0] == item_pos[0] and robot_pos[1] == item_pos[1]:
                robot.collect_item()
                reward = 1
        return reward

    def _remove_items(self):
        """
        Remove items collected by robots. Robots collect items by steping on
        them
        """
        for robot in self.robots:
            robot_pos = robot.get_position()
            for item in self.items:
                item_pos = item.get_position()
                if robot_pos[0] == item_pos[0] and robot_pos[1] == item_pos[1]:
                    self.items.remove(item)

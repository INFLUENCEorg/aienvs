import numpy as np

class FactoryFloorState():
    def __init__(self, robotList, taskList):
        self.robots = robotList
        self.tasks = taskList
        self.step = 0

    def addRobot(self, robot):
        self.robots.append(robot)

    def addTask(self, task):
        self.tasks.append(task)

    def __str__(self):
        """
        for hashing
        """
        return "Robots: " + str([str(robot) for robot in self.robots ]) + "Tasks: " + str([str(task) for task in self.tasks ])
 

def encodeStateAsArray(state:FactoryFloorState, width:int, height:int, currentRobotId:str=None):
    bitmapThisRobot = np.zeros((width, height))
    bitmapOtherRobots = np.zeros((width, height))
    bitmapTasks = np.zeros((width, height))

    for robot in state.robots:
        pos = robot.getPosition()
        if (robot.getId() == currentRobotId):
            bitmapThisRobot[pos[0], pos[1]] += 1
        else:
            bitmapOtherRobots[pos[0], pos[1]] += 1

    for task in state.tasks:
        pos = task.getPosition()
        bitmapTasks[pos[0], pos[1]] += 1

    if sum(sum(bitmapThisRobot)) > 1:
        raise "Something went wrong"
   
    return np.stack([bitmapOtherRobots,bitmapTasks,bitmapThisRobot], axis=2)

#TODO: make this snippet a test
#obs=env.reset()
#from aienvs.FactoryFloor.FactoryFloorTask import FactoryFloorTask
#import numpy as np
#obs.addTask(FactoryFloorTask(np.array([2,2])))
#obs.addTask(FactoryFloorTask(np.array([0,0])))
#encoded=encodeStateAsArray(obs, env.observation_space.nvec[1],env.observation_space.nvec[2], "robot1")



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
        
#    def getRobots(self):
#        return self.robots

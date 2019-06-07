class FactoryFloorState():
    def __init__(self, robotList, taskList):
        self.robots = robotList
        self.tasks = taskList
        self.step = 0

    def addRobot(self, robot):
        self.robots.append(robot)

    def addTask(self, task):
        self.tasks.append(task)

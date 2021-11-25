import pygame

class RobotManager():
    SINGLETON = None

    def __init__(self, sprites):
        self.__robotarr = []
        self.__sprites = sprites


    def addRobot(self, robot):
        self.__robotarr.append(robot)
        self.__sprites.add(robot)

    @staticmethod
    def getRobotManager():
        return RobotManager.SINGLETON
    
    @staticmethod
    def createRobotManager(sprites):
        RobotManager.SINGLETON = RobotManager(sprites)
        return RobotManager.SINGLETON

    def getRobots(self):
        return self.__robotarr

    def update(self, events):
        for p in self.__robotarr:
            if p.isAlive():
                p.updateBegin()
                p.update()
    
    def draw(self, screen):
        for p in self.getRobots():
            p.draw(screen)
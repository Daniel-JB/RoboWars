import pygame
import time
from abc import abstractmethod
import copy
import math
from Settings import Settings
from Bullet import Bullet
from manager.GameManager import GameManager
from manager.RobotManager import RobotManager
from manager.BulletManager import BulletManager

class Robot(pygame.sprite.Sprite):

    def __init__(self, x, y, image, name):
        super(Robot, self).__init__()
        self.__surf = pygame.image.load(image).convert()
        self.__originalsurf = pygame.image.load(image).convert()
        self.__rect = self.__surf.get_rect()
        self.__name = name
        self.__angle = 0
        self.direction = pygame.Vector2(1, 0)
        self.state = {}


        #
        #   Settings
        #
        self.__speed = Settings.SPEED
        self.__health = Settings.HEALTH
        self.__rect.centery = y
        self.__rect.centerx = x
        self.__myfont = pygame.font.SysFont('Comic Sans MS', 20)
        self.__textSurface = self.__myfont.render(self.getRobotName() + " - " + str(self.getHealth()), False, (0, 0, 0))
        self.__isAlive = True
        self.__commandsIssued = 0
        self.__lastBulletFired = 0

    def getAngle(self):
        return self.__angle

    def getTextSurface(self):
        return self.__textSurface

    def getImageSize(self):
        return self.__surf.get_size()

    def getOriginalSize(self):
        return self.__originalsurf.get_size()

    def getHealth(self):
        return self.__health    
    
    def takeDamage(self, amount):
        self.__health -= amount
        self.__textSurface = self.__myfont.render(self.getRobotName() + " - " + str(self.getHealth()), False, (0, 0, 0))

    def isAlive(self):
        if self.getHealth() <= 0:
            self.__isAlive = False
        return self.__isAlive

    def getSurf(self):
        return self.__surf
    
    def getRect(self):
        return self.__rect

    def move(self):
        if self.canRunCommand():
            if self.__rect.centerx < Settings.SCREEN_WIDTH - (self.getImageSize()[0] / 2):
                self.__rect.centerx += self.__speed
                self.__commandsIssued += 1

    def shoot(self):
        last = round(time.time() * 1000)
        if self.canRunCommand() and (last - self.__lastBulletFired) > Settings.BULLET_TICK:
            BulletManager.SINGLETON.addBullets(Bullet(self.__rect.center, self.direction.normalize(),self.__name))
            self.__lastBulletFired = last
            self.__commandsIssued += 1

    def getRobotName(self):
        return self.__name
  
    def canRunCommand(self):
        boolVal = self.isAlive() and self.__commandsIssued < Settings.MAX_COMMANDS_PER_TICK
        return boolVal

    def turn(self, angle):
        if self.canRunCommand() and not GameManager.getGameManager().checkCollision(self.__rect, self.getRobotName()):
            self.__angle += angle

            if self.__angle % 360 == 0:
                self.__angle = 0

            self.__surf = pygame.transform.rotate(self.__originalsurf, self.__angle)
            x = self.__rect.centerx
            y = self.__rect.centery
            self.__rect = self.__surf.get_rect(center = self.__originalsurf.get_rect(center = (x, y)).center)
            self.__commandsIssued += 1
            return True
            
        return False

    def turnLeft(self):
       return self.turn(Settings.TURN_SPEED)

    def turnRight(self):
        return self.turn(-Settings.TURN_SPEED)    

    def isLookingAtOld(self):
        for robot1 in RobotManager.getRobotManager().getRobots():
            robot1x = robot1.getRect().centerx
            robot1y = robot1.getRect().centery
            for robot2 in RobotManager.getRobotManager().getRobots():
                robot2x = robot2.getRect().centerx
                robot2y = robot2.getRect().centery
				
				#sanity check
                if(robot1x == robot2x and robot1y == robot2y):
					#same robot or same position
                    continue
				
                direction = round(math.atan2((robot2y-robot1y),(robot2x-robot1x))*(180/math.pi),0)
				#tolerance is magic number!!!
                tolerance = 2
                if(direction == robot1.getAngle() or (direction >= robot1.getAngle() - tolerance and direction <= robot1.getAngle() + tolerance)):
					#pewpew
                    print("pewpew1()")
					#if you can still fire on tanks behind other tanks then keep going or break inner loop.

    def isLookingAt(self, robotState):
        direction = round(math.atan2((robotState["centery"]-self.getRect().centery),(robotState["centerx"]-self.getRect().centerx))*(180/math.pi),0)
		#tolerance is magic number!!!
        tolerance = 2
        if(direction == self.getAngle() or (direction >= self.getAngle() - tolerance and direction <= self.getAngle() + tolerance)):
            print("pewpew2()")
            return True

        return False


    def moveLeft(self):
        if self.canRunCommand():
            speed = -Settings.SPEED
            rectCopy = copy.deepcopy(self.__rect)
            rectCopy = rectCopy.move(speed, 0)

            isColliding = GameManager.getGameManager().checkCollision(rectCopy, self.getRobotName())

            if self.__rect.centerx > (self.getImageSize()[0] / 2) and not isColliding:
                self.__rect = self.__rect.move(speed, 0)
                self.__commandsIssued += 1     
                return True 
        
        return False

    def moveRight(self):
        if self.canRunCommand():
            rectCopy = copy.deepcopy(self.__rect)
            rectCopy = rectCopy.move(Settings.SPEED, 0)
            
            isColliding = GameManager.getGameManager().checkCollision(rectCopy, self.getRobotName())

            if self.__rect.centerx < Settings.SCREEN_WIDTH - (self.getImageSize()[0] / 2) and not isColliding:
                self.__rect = self.__rect.move(Settings.SPEED, 0)
                self.__commandsIssued += 1
                return True

        return False


    def moveUp(self):
        if self.canRunCommand():
            rectCopy = copy.deepcopy(self.__rect)
            rectCopy = rectCopy.move(-Settings.SPEED, 0)

            isColliding = GameManager.getGameManager().checkCollision(rectCopy, self.getRobotName())

            if self.__rect.centery > (self.getOriginalSize()[1] / 2) and not isColliding:
                self.__rect = self.__rect.move(0, -Settings.SPEED)
                self.__commandsIssued += 1
                return True
            
        return False


    def moveDown(self):
        if self.canRunCommand():
            rectCopy = copy.deepcopy(self.__rect)
            rectCopy = rectCopy.move(-Settings.SPEED, 0)

            isColliding = GameManager.getGameManager().checkCollision(rectCopy, self.getRobotName())

            if self.__rect.centery < Settings.SCREEN_HEIGHT - (self.getImageSize()[0] / 2)  and not isColliding:
                self.__rect = self.__rect.move(0, Settings.SPEED)
                self.__commandsIssued += 1
                return True
            
        return False

    def draw(self, screen):
        # Draw the actual robot
        screen.blit(self.getSurf(), self.getRect())  

        # Hard coded offsets, need to investigate font/image size/image location 
        # Draws the UI Text
        x = self.getRect().centerx - (self.getOriginalSize()[0] - 120)
        y = self.getRect().centery - (self.getOriginalSize()[1] - 60)

        screen.blit(self.getTextSurface(),(x, y))

    def updateBegin(self):
        self.__commandsIssued = 0

    @abstractmethod
    def update(self):
        self.direction = pygame.Vector2(1, 0).rotate(-self.__angle)

    def updateEnd(self, state):
        self.state = state     

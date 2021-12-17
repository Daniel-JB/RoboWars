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

    def __init__(self, image, name):
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
        self.__rect.centery = 0
        self.__rect.centerx = 0
        self.__myfont = pygame.font.SysFont('Comic Sans MS', 20)
        self.__isAlive = True
        self.__commandsIssued = 0
        self.__totalCommandsIssued = 0
        self.__lastBulletFired = 0
        strToPrint = self.getRobotName() + " - " + str(self.getHealth()) + " - " + str(self.__totalCommandsIssued)
        self.__textSurface = self.__myfont.render(strToPrint, False, (0, 0, 0))       

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
        strToPrint = self.getRobotName() + " - " + str(self.getHealth()) + " - " + str(self.__totalCommandsIssued)
        self.__textSurface = self.__myfont.render(strToPrint, False, (0, 0, 0))

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

    def isLookingAt(self, robotState):
        direction = round(math.atan2(((robotState["centery"] * -1)-(self.getRect().centery) * -1),(robotState["centerx"]-self.getRect().centerx))*(180/math.pi),0) % 360
        #tolerance is magic number!!!
        tolerance = 10
        if((direction% 360) == (self.getAngle()% 360) or ((direction% 360) >= (self.getAngle()% 360) - tolerance and (direction% 360) <= (self.getAngle()% 360) + tolerance)):
            return True

        return False

    #Check if Robot should turn left to face enemy
    def turnTowards(self, robotState):
        direction = round(math.atan2(((robotState["centery"] * -1)-(self.getRect().centery) * -1),(robotState["centerx"]-self.getRect().centerx))*(180/math.pi),0) % 360
        
        #print(f'direction:  {direction % 360:.0f} angle: {self.getAngle()% 360:.0f} result: {(((direction % 360)-(self.getAngle()%360))%360 < 179)} ')
        if(((direction % 360)-(self.getAngle()%360))%360 < 179):
            if(((direction % 360)-(self.getAngle()%360))%360 < 10 or ((self.getAngle()%360)-(direction % 360))%360 < 10):
                return self.turnLeft()
            else:
                self.turnLeft()
                self.turnLeft()
                self.turnLeft()
                return self.turnLeft()
        if(((direction % 360)-(self.getAngle()%360))%360 < 10 or ((self.getAngle()%360)-(direction % 360))%360 < 10):
            return self.turnRight()
        else:
            self.turnRight()
            self.turnRight()
            self.turnRight()
            return self.turnRight()
    
    #Turn towards a particular angle
    def turnTowardsAngle(self, angle):
        if(((angle % 360)-(self.getAngle()%360))%360 < 179):
            if(((angle % 360)-(self.getAngle()%360))%360 < 10 or ((self.getAngle()%360)-(angle % 360))%360 < 10):
                return self.turnLeft()
            else:
                self.turnLeft()
                self.turnLeft()
                self.turnLeft()
                return self.turnLeft()

        if(((angle % 360)-(self.getAngle()%360))%360 < 10 or ((self.getAngle()%360)-(angle % 360))%360 < 10):
            return self.turnRight()
        else:
            self.turnRight()
            self.turnRight()
            self.turnRight()
            return self.turnRight()

    #def findNearestBot(self)
        

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

        Color_line=(255,0,0)
        x = self.getRect().centerx
        y = self.getRect().centery
        lineLength = 350
        
        x2 = x + (lineLength * math.cos((self.getAngle()%360)*(math.pi/180)))
        y2 = (y + (lineLength * math.sin((self.getAngle()%360)*(math.pi/180))) * (-1))
        
        pygame.draw.line(screen, Color_line, (x, y), (x2, y2))       

    def updateBegin(self):
        self.__totalCommandsIssued += self.__commandsIssued
        self.__commandsIssued = 0

    @abstractmethod
    def update(self):
        self.direction = pygame.Vector2(1, 0).rotate(-self.__angle)

    def updateEnd(self, state):
        self.state = state     

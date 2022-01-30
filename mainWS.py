import pygame
import time
from manager.GameManager import GameManager
from Settings import Settings
from manager.RobotManager import RobotManager
from robots.CrazyRobot import CrazyRobot
from robots.DanielRobot import DanielRobot
from robots.SlowRobot import SlowRobot
from robots.MicroManRobot import MicroManRobot

pygame.init()
pygame.font.init() 

screen = pygame.display.set_mode([Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT])
sprites = pygame.sprite.Group()

running = True

clock = pygame.time.Clock()

myGameManager =  GameManager.createGameManager(screen, sprites)
RobotManager.getRobotManager().addRobot(DanielRobot("robot.png", "DanielRobot"))
RobotManager.getRobotManager().addRobot(CrazyRobot("robot2.png", "AIRobot"))
RobotManager.getRobotManager().addRobot(MicroManRobot("robot2.png", "MicroManRobot"))
RobotManager.getRobotManager().addRobot(SlowRobot("robot2.png", "SlowRobot"))

Settings.lastUpdatedTick = pygame.time.get_ticks()

def draw(): 
    screen.fill((255, 255, 255))  
    # 
    #
    #
    myGameManager.draw(screen)
    #
    #   
    #
    pygame.display.flip()

def update(events, dt):
    myGameManager.update(events, dt)

clock = pygame.time.Clock()
started = False

while running:



    # Did the user click the window close button?
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False    

    # Only update/draw when ticks passed tickrate
    if(pygame.time.get_ticks() - Settings.lastUpdatedTick > Settings.TICK_RATE):
        Settings.lastUpdatedTick = pygame.time.get_ticks()
        update(events, dt)
        draw()

        #Just pause screen for 2 seconds on start to see positions
        if(not started):
            started = True
            time.sleep(2)
    
    dt = clock.tick(60)



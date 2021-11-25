import pygame
from manager.GameManager import GameManager
from Settings import Settings
from manager.RobotManager import RobotManager
from robots.AIRobot import AIRobot
from robots.DanielRobot import DanielRobot

pygame.init()
pygame.font.init() 

screen = pygame.display.set_mode([Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT])
sprites = pygame.sprite.Group()

running = True

clock = pygame.time.Clock()

myGameManager =  GameManager.createGameManager(screen, sprites)
RobotManager.getRobotManager().addRobot(DanielRobot(150, 150, "robot.png", "DanielRobot"))
RobotManager.getRobotManager().addRobot(AIRobot(600, 150, "robot2.png", "AIRobot"))

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
    
    dt = clock.tick(60)


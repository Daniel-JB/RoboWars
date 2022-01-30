
import pygame

from Settings import Settings
from core.CoreSprite import CoreSprite

class Bullet(CoreSprite):
    def __init__(self, pos, direction, robotName):
        super().__init__(pos, direction, 'bullet.jpg')
        self.robotName = robotName

    def getRobotName(self):
        return self.robotName

    def update(self, events, dt):
        self.pos += self.direction * Settings.BULLET_SPEED
        self.rect.center = self.pos

        if self.isDestroyed:
            return False

        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.destroy()
            return False
            
        return True
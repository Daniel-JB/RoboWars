
import pygame

from Settings import Settings

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pygame.image.load('bullet.jpg').convert()
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.pos = pygame.Vector2(self.rect.center)
        self.__sprites = pygame.sprite.Group()

        self.__sprites.add(self)

    def update(self, events, dt):
        self.pos += self.direction * Settings.BULLET_SPEED
        self.rect.center = self.pos
        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.kill()
            return False
        return True

    def draw(self, screen):
        # Draw the actual bullet
        screen.blit(self.image, self.rect)          
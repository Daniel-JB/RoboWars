import pygame

class CoreSprite(pygame.sprite.Sprite):
    def __init__(self, pos, direction, imageToLoad):
        super().__init__()
        self.__surf = pygame.image.load(imageToLoad).convert()
        self.__rect = self.__surf.get_rect(center=pos)
        self.__direction = direction
        self.pos = pygame.Vector2(self.rect.center)
        self.isDestroyed = False
        self.__angle = 0

    def getRect(self):
        return self.__rect

    def setRect(self, value):
        self.__rect = value
  
    def getSurf(self):
        return self.__surf

    def setSurf(self, value):
        self.__surf = value      

    def getImageSize(self):
        return self.__surf.get_size()

    def getDirection(self):
        return self.__direction

    def setDirection(self, value):
        self.__direction = value

    def getAngle(self):
        return self.__angle

    def setAngle(self, value):
        self.__angle = value

    rect = property(getRect, setRect)
    surf = property(getSurf, setSurf)
    imageSize = property(getImageSize)
    direction = property(getDirection, setDirection)
    angle = property(getAngle, setAngle)

    def destroy(self):
        self.isDestroyed = True
        self.kill()

    def update(self):
        self.direction = pygame.Vector2(1, 0).rotate(-self.getAngle())

    def draw(self, screen):
        # Draw the actual sprite
        screen.blit(self.getSurf(), self.getRect())            
import pygame

class Pellet:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.isEaten = False

    def draw(self):
        pygame.draw.circle(self.screen, (255, 255, 255), [self.x, self.y], 10)

    def checkCollision(self, pacmanPosX, pacmanPosY):
        distSquared = (self.x - pacmanPosX)**2 + (self.y - pacmanPosY)**2

        if distSquared <= (10 + 30)**2:
            self.isEaten = True

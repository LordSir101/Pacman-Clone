import pygame

class Pellet:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.rad = 5
        #self.isEaten = False

    def draw(self):
        pygame.draw.circle(self.screen, (255, 255, 255), [self.x, self.y], self.rad)

    def checkCollision(self, player):
        distSquared = (self.x - player.x)**2 + (self.y - player.y)**2

        if distSquared <= (self.rad + player.width/2)**2:
            return True

import pygame

class PowerPellet:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.rad = 10
        self.point_value = 100

    def draw(self):
        pygame.draw.circle(self.screen, (255, 255, 255), [self.x, self.y], self.rad)

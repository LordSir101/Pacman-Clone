import pygame

class Pellet:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen

    def draw(self):
        pygame.draw.circle(self.screen, (255, 255, 255), [self.x, self.y], 10)

    # def delete(self):

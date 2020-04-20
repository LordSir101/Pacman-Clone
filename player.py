import pygame

class Player:
    def __init__(self, width, height):
        self.scrnW = width
        self.img = pygame.image.load("packman.png")
        self.sprite = pygame.transform.scale(self.img, (60, 60))
        self.x = width/2
        self.y = height/2
        self.vel = 0.5
        self.dirX = 0
        self.dirY = 0

    def move(self):
        self.x += self.dirX * self.vel
        self.y += self.dirY * self.vel

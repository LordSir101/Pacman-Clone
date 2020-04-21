import pygame

class Player:
    def __init__(self, width, height):
        self.scrnW = width
        self.scrnH = height

        self.img = pygame.image.load("packman.png")
        self.sprite = pygame.transform.scale(self.img, (30, 30))

        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.x = width/2 - self.width/2
        self.y = height/2 - self.height/2
        self.vel = 0.5
        self.dirX = 0
        self.dirY = 0

    def move(self):
        self.x += self.dirX * self.vel
        self.y += self.dirY * self.vel

        if self.x > self.scrnW - self.width:
            self.x = self.scrnW - self.width
        elif self.x < 0:
            self.x = 0
        if self.y > self.scrnH - self.height:
            self.y = self.scrnH - self.height
        elif self.y < 0:
            self.y = 0

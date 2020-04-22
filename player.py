from pygame import image, Color
import pygame

class Player:
    def __init__(self, width, height):
        self.scrnW = width
        self.scrnH = height

        self.folder = "pacman_animation/"
        self.img = pygame.image.load(self.folder+"pacman1.png")
        self.idle = True
        self.imgs = [pygame.image.load(self.folder+"pacman1.png"),
                    pygame.image.load(self.folder+"pacman2.png"),
                    pygame.image.load(self.folder+"pacman3.png"),
                    pygame.image.load(self.folder+"pacman4.png")]


        self.frame = 0
        self.animationRate = 5
        self.sprite = pygame.transform.scale(self.imgs[1], (30, 30))
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()

        self.x = width/2 - self.width/2 + 10
        self.y = height/2 - self.height/2
        self.vel = 2
        self.dirX = 0
        self.dirY = 0
        self.score = 0


    def move(self):
        movemap = image.load('movemap.png')
        colourmap = image.load('colourmap.png')

        #check if pacman will move into a wall
        #this is approximately where packman's sprite will collide with a wall
        nextX = self.x + self.dirX * self.vel + (self.width/3 * self.dirX)
        nextY = self.y + self.dirY *self.vel + (self.height/3*self.dirY)
        
        if movemap.get_at((int(nextX), int(nextY))) != Color(255,255,255):
            self.x += self.dirX * self.vel
            self.y += self.dirY * self.vel

        else:
            pass

        #player position is the center of the sprite
        #this keeps pacman from going off screen
        if self.x > self.scrnW - self.width/2:
            self.x = self.scrnW - self.width/2
        elif self.x < 0 + self.width/2:
            self.x = 0 + self.width/2
        if self.y > self.scrnH - self.height/2:
            self.y = self.scrnH - self.height/2
        elif self.y < 0 + self.height/2:
            self.y = 0  + self.height/2


    def draw(self, screen):
        #change state of pacman
        if self.dirX != 0 or self.dirY != 0:
            self.idle = False
        else:
            self.idle = True

        #choose which frame to use
        if self.idle:
            sprite = pygame.transform.scale(self.imgs[0], (30, 30))
            screen.blit(sprite, (self.x - self.width/2, self.y - self.height/2))
        #if moving
        else:
            if self.dirX > 0:
                sprite = pygame.transform.flip(self.imgs[self.frame], True, False)
                scaled = pygame.transform.scale(sprite, (30, 30))
                screen.blit(scaled, (self.x - self.width/2, self.y - self.height/2))
            elif self.dirX < 0:
                sprite = pygame.transform.scale(self.imgs[self.frame], (30, 30))
                screen.blit(sprite, (self.x - self.width/2, self.y - self.height/2))
            elif self.dirY >0:
                sprite = pygame.transform.rotate(self.imgs[self.frame], 90)
                scaled = pygame.transform.scale(sprite, (30, 30))
                screen.blit(scaled, (self.x - self.width/2, self.y - self.height/2))
            elif self.dirY < 0:
                sprite = pygame.transform.rotate(self.imgs[self.frame], -90)
                scaled = pygame.transform.scale(sprite, (30, 30))
                screen.blit(scaled, (self.x - self.width/2, self.y - self.height/2))

    def changeFrame(self):
        self.frame += 1
        if self.frame > len(self.imgs) -1:
            self.frame = 0

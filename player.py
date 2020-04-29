from pygame import image, Color
import pygame

class Player:
    def __init__(self, width, height):
        self.scrnW = width
        self.scrnH = height

        #images for pacman animation
        self.folder = "animations/pacman_move/"
        self.imgs = [pygame.image.load(self.folder+"pacman1.png"),
                    pygame.image.load(self.folder+"pacman2.png"),
                    pygame.image.load(self.folder+"pacman3.png"),
                    pygame.image.load(self.folder+"pacman4.png")]

        self.idle = True #state
        self.frame = 0
        self.animationRate = 5 #speed of pacman animation
        self.scale = 25

        #use an image as reference for pacman dimensions
        self.sprite = pygame.transform.scale(self.imgs[1], (self.scale, self.scale))
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()

        self.x = width/2 - self.width/2 + 10
        self.y = height/2 - self.height/2 + 60
        self.prevX = -1
        self.prevY = -1
        self.vel = 2.5
        self.dirX = 0
        self.dirY = 0
        self.score = 0


    def move(self):
        movemap = image.load('movemap.png')
        colourmap = image.load('colourmap.png')

        self.prevX = self.x
        self.prevY = self.y

        #this is approximately where packman's sprite will collide with a wall
        nextX = self.x + self.dirX * self.vel + (self.width/2 * self.dirX)
        nextY = self.y + self.dirY *self.vel + (self.height/2 * self.dirY)

        if(nextX >= movemap.get_width()):
           nextX = movemap.get_width() - 1

        if(nextX < 0):
           nextX = 0

        if(nextY >= movemap.get_height()):
           nextY = movemap.get_height() - 1

        if(nextY < 0):
           nextY = 0






        #check if pacman will move into a wall
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

    def hasMoved(self):
        if(self.x == self.prevX and self.y == self.prevY):
            return False
        else:
            return True

    def draw(self, screen):
        #change state of pacman
        if self.dirX != 0 or self.dirY != 0:
            self.idle = False
        else:
            self.idle = True

        #choose which frame to use
        if self.idle:
            sprite = pygame.transform.scale(self.imgs[0], (self.scale, self.scale))
            screen.blit(sprite, (self.x - self.width/2, self.y - self.height/2))
        #if moving
        else:
            #all pacman images face left, so various transformations must be applied depending on pacman's direction
            if self.dirX > 0:
                sprite = pygame.transform.flip(self.imgs[self.frame], True, False)
                scaled = pygame.transform.scale(sprite, (self.scale, self.scale))
                screen.blit(scaled, (self.x - self.width/2, self.y - self.height/2))
            elif self.dirX < 0:
                sprite = pygame.transform.scale(self.imgs[self.frame], (self.scale, self.scale))
                screen.blit(sprite, (self.x - self.width/2, self.y - self.height/2))
            elif self.dirY >0:
                sprite = pygame.transform.rotate(self.imgs[self.frame], 90)
                scaled = pygame.transform.scale(sprite, (self.scale, self.scale))
                screen.blit(scaled, (self.x - self.width/2, self.y - self.height/2))
            elif self.dirY < 0:
                sprite = pygame.transform.rotate(self.imgs[self.frame], -90)
                scaled = pygame.transform.scale(sprite, (self.scale, self.scale))
                screen.blit(scaled, (self.x - self.width/2, self.y - self.height/2))

    def changeFrame(self):
        self.frame += 1
        if self.frame > len(self.imgs) -1:
            self.frame = 0

    def findNode(self, nodes):

        for row in nodes:
            for val in row:
                if val != 0:
                    tolerance  = 25 * 25
                    distSquaredX = (val.x - self.x)**2
                    distSquaredY = (val.y - self.y)**2
                    if distSquaredX < tolerance and distSquaredY < tolerance:
                        #print(val.x)
                        return val

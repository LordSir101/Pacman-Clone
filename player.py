from pygame import image, Color
import pygame

class Player:
    def __init__(self, width, height):
        # load images for pacman animation
        self.folder = "animations/pacman_move/"
        self.imgs_alive = [pygame.image.load(self.folder+"pacman1.png"),
                    pygame.image.load(self.folder+"pacman2.png"),
                    pygame.image.load(self.folder+"pacman3.png"),
                    pygame.image.load(self.folder+"pacman4.png")]

        self.folder = "animations/pacman_death/"
        self.imgs_dead = [pygame.image.load(self.folder+"death00.png"),
                    pygame.image.load(self.folder+"death01.png"),
                    pygame.image.load(self.folder+"death02.png"),
                    pygame.image.load(self.folder+"death03.png"),
                    pygame.image.load(self.folder+"death04.png"),
                    pygame.image.load(self.folder+"death05.png"),
                    pygame.image.load(self.folder+"death06.png"),
                    pygame.image.load(self.folder+"death07.png"),
                    pygame.image.load(self.folder+"death08.png"),
                    pygame.image.load(self.folder+"death09.png"),
                    pygame.image.load(self.folder+"death10.png"),
                    pygame.image.load(self.folder+"death11.png")]

        # define screen dimensions
        self.scrnW = width
        self.scrnH = height

        # use an image as reference for pacman dimensions
        self.scale = 25
        self.sprite = pygame.transform.scale(self.imgs_alive[1], (self.scale, self.scale))
        self.rad = self.sprite.get_width() / 2
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()

        # state variables
        self.idle = True
        self.isLiving = True
        self.pauseDone = False

        # animation variables
        self.frame_alive = 0
        self.frame_dead = 0
        self.animationRate = 6 # speed of pacman animation

        # current movement variables
        self.vel = 2.5
        self.x = self.scrnW/2 - self.rad + 10
        self.y = self.scrnH/2 - self.rad + 60
        self.dirX = 0
        self.dirY = 0

        # previous movement variables
        self.prevX = -1
        self.prevY = -1
        self.prevDirX = 0
        self.prevDirY = 0

        # future movement variables
        self.moveQueue = 0
            # NONE  == 0
            # UP    == 1
            # DOWN  == 2
            # LEFT  == 3
            # RIGHT == 4

        # counter variables
        self.lives = 3
        self.score = 0

    def move(self):
        movemap = image.load('movemap.png')

        # store current position for future reference
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



        if movemap.get_at((int(nextX), int(nextY))) != Color(255,255,255):
            self.x += self.dirX * self.vel
            self.y += self.dirY * self.vel
            self.moveQueue = 0


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
        if self.isLiving == True:
            # change state of pacman
            if self.dirX != 0 or self.dirY != 0:
                self.idle = False
            else:
                self.idle = True

            # choose which frame to use
            if self.idle:
                sprite = pygame.transform.scale(self.imgs_alive[0], (self.scale, self.scale))
                screen.blit(sprite, (self.x - self.rad, self.y - self.rad))
            # if moving
            else:
                # all pacman images face left, so various transformations must be applied depending on pacman's direction
                if self.dirX > 0:
                    sprite = pygame.transform.flip(self.imgs_alive[self.frame_alive], True, False)
                    scaled = pygame.transform.scale(sprite, (self.scale, self.scale))
                    screen.blit(scaled, (self.x - self.rad, self.y - self.rad))
                elif self.dirX < 0:
                    sprite = pygame.transform.scale(self.imgs_alive[self.frame_alive], (self.scale, self.scale))
                    screen.blit(sprite, (self.x - self.rad, self.y - self.rad))
                elif self.dirY > 0:
                    sprite = pygame.transform.rotate(self.imgs_alive[self.frame_alive], 90)
                    scaled = pygame.transform.scale(sprite, (self.scale, self.scale))
                    screen.blit(scaled, (self.x - self.rad, self.y - self.rad))
                elif self.dirY < 0:
                    sprite = pygame.transform.rotate(self.imgs_alive[self.frame_alive], -90)
                    scaled = pygame.transform.scale(sprite, (self.scale, self.scale))
                    screen.blit(scaled, (self.x - self.rad, self.y - self.rad))

        else:
            # the case where self.isLiving == False and self.pauseDone == False
            if self.pauseDone == False:
                # during the pause after dying to a ghost, keep the last frame of pacman walking before he died
                if self.prevDirX > 0:
                    sprite = pygame.transform.flip(self.imgs_alive[self.frame_alive], True, False)
                    scaled = pygame.transform.scale(sprite, (self.scale, self.scale))
                    screen.blit(scaled, (self.x - self.rad, self.y - self.rad))
                elif self.prevDirX < 0:
                    sprite = pygame.transform.scale(self.imgs_alive[self.frame_alive], (self.scale, self.scale))
                    screen.blit(sprite, (self.x - self.rad, self.y - self.rad))
                elif self.prevDirY > 0:
                    sprite = pygame.transform.rotate(self.imgs_alive[self.frame_alive], 90)
                    scaled = pygame.transform.scale(sprite, (self.scale, self.scale))
                    screen.blit(scaled, (self.x - self.rad, self.y - self.rad))
                elif self.prevDirY < 0:
                    sprite = pygame.transform.rotate(self.imgs_alive[self.frame_alive], -90)
                    scaled = pygame.transform.scale(sprite, (self.scale, self.scale))
                    screen.blit(scaled, (self.x - self.rad, self.y - self.rad))

            # the case where self.isLiving == False and self.pauseDone == True
            else:
                sprite = pygame.transform.scale(self.imgs_dead[self.frame_dead], (self.scale, self.scale))
                screen.blit(sprite, (self.x - self.rad, self.y - self.rad))

                # after death animation is done
                if self.frame_dead == len(self.imgs_dead) - 1:
                    # respawn pacman
                    self.isLiving = True
                    self.frame_alive = 0
                    self.frame_dead = 0
                    self.x = self.scrnW/2 - self.rad + 10
                    self.y = self.scrnH/2 - self.rad + 60
                    self.pauseDone = False

    def findNode(self, nodes):
        for row in nodes:
            for val in row:
                if val != 0:
                    tolerance  = 25 * 25
                    distSquaredX = (val.x - self.x)**2
                    distSquaredY = (val.y - self.y)**2

                    if distSquaredX < tolerance and distSquaredY < tolerance:
                        return val

    def deathEvents(self):
        if self.isLiving == True:
            self.dirX = 0
            self.dirY = 0

            # remove a life
            self.lives -= 1

            # check if no more lives
            if self.lives <= 0:
                # display game over text
                print("GAME OVER")

            self.isLiving = False

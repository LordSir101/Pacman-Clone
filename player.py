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

        self.movemap = image.load('movemap.png')

        # define screen dimensions
        self.scrnW = width
        self.scrnH = height

        # use an image as reference for pacman dimensions
        self.scale = 25
        self.sprite = pygame.transform.scale(self.imgs_alive[1], (self.scale, self.scale))
        self.rad = (self.sprite.get_width() / 2) + 1
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()

        # define pacman's spawn location
        self.spawnX = self.scrnW/2 - self.rad + 10
        self.spawnY = self.scrnH/2 - self.rad + 64

        # state variables
        self.isLiving = True
        self.pauseDone = False

        # animation variables
        self.frame_alive = 0
        self.frame_dead = 0
        self.animationRate = 6 # speed of pacman animation

        # current movement variables
        self.vel = 2.5
        self.x = self.spawnX
        self.y = self.spawnY
        self.dirX = 0
        self.dirY = 0

        # previous movement variables
        self.prevX = None       #{ initialized as None, since there is no initial previous move
        self.prevY = None       #{
        self.prevDirX = 0       #{ stores the direction from the previous frame
        self.prevDirY = 0       #{

        # future movement variables
        self.intendedDirX = None    #{ initialized as None, since there is no initial intended move
        self.intendedDirY = None    #{

        # counter variables
        self.lives = 3
        self.score = 0

    def move(self):
        # store current position and direction for future reference
        self.prevX = self.x
        self.prevY = self.y
        self.prevDirX = self.dirX
        self.prevDirY = self.dirY

        if self.isMoveValid(self.dirX, self.dirY):
            self.x += self.dirX * self.vel
            self.y += self.dirY * self.vel

    def hasMoved(self):
        if self.x == self.prevX and self.y == self.prevY:
            return False
        else:
            return True

    def isMoveValid(self, dirX, dirY):
        # error handling
        if dirX == None or dirY == None:
            return False

        # this is approximately where pacman's sprite will collide with a wall
        nextX = self.x + (dirX * self.vel)
        nextY = self.y + (dirY * self.vel)

        # out of bounds error handling for the tunnel
        if(nextX >= self.movemap.get_width()):
           nextX = self.movemap.get_width() - 1

        if(nextX < 0):
           nextX = 0

        if(nextY >= self.movemap.get_height()):
           nextY = self.movemap.get_height() - 1

        if(nextY < 0):
           nextY = 0

        # prevents pacman clipping with the wall
        buffer = 5


        # if going down, check bottom left and bottom right corners of pacman
        if (dirX == 0 and dirY > 0 and
            self.movemap.get_at((int(nextX + (self.rad - buffer)), int(nextY + (self.rad - buffer)))) == Color(0, 0, 0) and
            self.movemap.get_at((int(nextX - (self.rad - buffer)), int(nextY + (self.rad - buffer)))) == Color(0, 0, 0)):
            return True

        # if going up, check top left and top right corners of pacman
        elif (dirX == 0 and dirY < 0 and
            self.movemap.get_at((int(nextX + (self.rad - buffer)), int(nextY - (self.rad - buffer)))) == Color(0, 0, 0) and
            self.movemap.get_at((int(nextX - (self.rad - buffer)), int(nextY - (self.rad - buffer)))) == Color(0, 0, 0)):
            return True

        # if going right, check top right and bottom right corners of pacman
        elif(dirX > 0 and dirY == 0 and
            self.movemap.get_at((int(nextX + (self.rad - buffer)), int(nextY + (self.rad - buffer)))) == Color(0, 0, 0) and
            self.movemap.get_at((int(nextX + (self.rad - buffer)), int(nextY - (self.rad - buffer)))) == Color(0, 0, 0)):
            return True

        # if going left, check top left and bottom left corners of pacman
        elif(dirX < 0 and dirY == 0 and
            self.movemap.get_at((int(nextX - (self.rad - buffer)), int(nextY + (self.rad - buffer)))) == Color(0, 0, 0) and
            self.movemap.get_at((int(nextX - (self.rad - buffer)), int(nextY - (self.rad - buffer)))) == Color(0, 0, 0)):
            return True

        else:
            return False

    def draw(self, screen):
        if self.isLiving == True:
            # choose which frame to use
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
                # the case where pacman is idle
                sprite = pygame.transform.scale(self.imgs_alive[0], (self.scale, self.scale))
                screen.blit(sprite, (self.x - self.rad, self.y - self.rad))

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
                else:
                    sprite = pygame.transform.scale(self.imgs_alive[0], (self.scale, self.scale))
                    screen.blit(sprite, (self.x - self.rad, self.y - self.rad))

            # the case where self.isLiving == False and self.pauseDone == True
            else:
                sprite = pygame.transform.scale(self.imgs_dead[self.frame_dead], (self.scale, self.scale))
                screen.blit(sprite, (self.x - self.rad, self.y - self.rad))

                # after death animation is done
                if self.frame_dead == len(self.imgs_dead) - 1:
                    self.respawnEvents()

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
            self.isLiving = False
            self.dirX = 0
            self.dirY = 0

    def respawnEvents(self):
        # respawn pacman
        self.isLiving = True
        self.pauseDone = False

        self.frame_alive = 0
        self.frame_dead = 0
        self.x = self.spawnX
        self.y = self.spawnY

        self.dirX = 0
        self.dirY = 0
        self.prevX = None
        self.prevY = None
        self.prevDirX = 0
        self.prevDirY = 0
        self.intendedDirX = None
        self.intendedDirY = None

        # remove a life
        self.lives -= 1

        # check if no more lives
        if self.lives <= 0:
            # display game over text
            print("GAME OVER")

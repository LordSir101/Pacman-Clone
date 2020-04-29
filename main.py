import pygame
from player import Player
from pygame import image, Color
from pellet import Pellet
from powerPellet import PowerPellet
from ghostNode import Node
from ghost import Ghost
from tunnel import Tunnel
import time

pygame.init()

# window dimensions
w = 600
h = 600
frameCounter = 0
gameStarted = False

# create screen
screen = pygame.display.set_mode((w, h))

# title and icon
pygame.display.set_caption("Game thing")

# create player
player = Player(w, h)

# create pellet array
pellet_list = []

# list of actual nodes
nodeList = []

# create powerPellet array
powerPellet_list = []

# create ghostNodes array
ghostNodes = []

# create two way tunnel
tunnel = Tunnel(10, 290, w-10, 290)   # (x1, y1, x2, y2)

# have the ghost get the path to its target
def getPath():
    if player.hasMoved():
        node = player.findNode(ghostNodes)
        ghost.bestPath = []
        ghost.getPath(ghost.currentNode, node)
        ghost.shortestSize = 9223372036854775807

        #reset all nodes to discoverable
        for row in ghostNodes:
            for val in row:
                if val == 0:
                    pass
                else:
                    val.status = 0

#---------------------------------------------------------------------------
def update():

    global player
    global frameCounter
    global ghost
    global prevNode

    # keeps track of how many frames the current animation has been played for
    # frameCounter does not count during the pause before death animation
    if player.isLiving == True or (player.isLiving == False and player.pauseDone == True):
        frameCounter = (frameCounter + 1) % 100

    # walking animation
    if frameCounter % player.animationRate == 0 and player.hasMoved() and player.isLiving == True:
        # change the player.frame_alive every player.animationRate number of frames
        player.frame_alive = (player.frame_alive + 1) % len(player.imgs_alive)

    # death animation
    # pause for around 1 second
    if player.isLiving == False and player.pauseDone == False:
        time.sleep(1.0)
        player.pauseDone = True

    if frameCounter % player.animationRate == 0 and player.pauseDone == True:
        # change the player.frame_dead every player.animationRate number of frames
        player.frame_dead = (player.frame_dead + 1) % len(player.imgs_dead)

    # player walks
    if player.isLiving == True:
        player.move()
        tunnel.teleportPlayer(player)

        getPath()
        ghost.move(player)

    # check if pacman and ghost collide
    if isColliding(player, ghost):
        # play death animation and remove a life
        player.deathEvents()

    # check if pacman is eating pellets
    for pellet in reversed(pellet_list):
        if isColliding(pellet, player):
            pellet_list.remove(pellet)
            player.score += pellet.point_value

    # check if pacman is eating powerPellets
    for powerPellet in reversed(powerPellet_list):
        if isColliding(powerPellet, player):
            powerPellet_list.remove(powerPellet)
            player.score += powerPellet.point_value


#---------------------------------------------------------------------------
def draw():
    if gameStarted == False:
        # text, size, xpos, ypos, center text at point
        drawText("Click Any Button To Play", 45, w/2, h/2, True)
    else:
        pygame.draw.rect(screen,(0, 0, 0),(0, 0, w, h))
        # background
        screen.blit(pygame.image.load('colourmap.png'), (0,0))
        for pellet in pellet_list:
            pellet.draw()

        for powerPellet in powerPellet_list:
            powerPellet.draw()

        global player
        player.draw(screen)

        global ghost
        ghost.draw(screen)
        drawText("Score: " + str(player.score), 20, 0, 580, False)

def drawText(text, size, x, y, center):
    font = pygame.font.Font('freesansbold.ttf', size)
    overText = font.render(text, True, (255,255,255))
    textW = overText.get_width()
    textH = overText.get_height()

    if center:
        # centers the text at the specified point
        screen.blit(overText, (int(x - textW/2), int(y - textH/2)))
    else:
        screen.blit(overText, (x, y))

# create ghost path and place dots on map-----------------------------------------------------------------------
dotimage = image.load('pacmandotmap.png')
pathImage = image.load('movemap.png')

def checkDotPoint(x, y, image):
    global dotimage
    global pathImage

    image = dotimage if image == 0 else pathImage
    if image.get_at((int(x), int(y))) == Color('black'):
        return True
    return False

pathScale = 20  # controls how far apart the nodes/dots are
ghostNodes = [] # this is the possible nodes that a ghost can travel to

def createGhostPath():
    global ghostNodes
    global screen

    y = 0
    currY = 0

    while y < 560 / pathScale:
        ghostNodes.append([])
        x = 0

        while x < 580 / pathScale:
            targetX = 10 + (x*pathScale)
            targetY = 10 + (y*pathScale)

            if checkDotPoint(targetX, targetY, 1):
                ghostNodes[currY].append(Node(targetX, targetY, x, currY))

            else:
                ghostNodes[currY].append(0)

            x += 1
        y += 1
        currY += 1

def placePellets():
    global pellet_list
    global screen
    global pathScale

    x = 0
    while x < 580 / pathScale:
        y = 0
        while y < 550 / pathScale:
            targetX = 10 + (x*pathScale)
            targetY = 10 + (y*pathScale)
            if checkDotPoint(targetX, targetY, 0) and not doesPowerPelletExistHere(targetX, targetY):
                pellet_list.append(Pellet(targetX, targetY, screen))
            y += 1
        x += 1

def placePowerPellets():
    global powerPellet_list
    global screen

    powerPellet_list.append(PowerPellet(30, 70, screen))
    powerPellet_list.append(PowerPellet(570, 70, screen))
    powerPellet_list.append(PowerPellet(30, 490, screen))
    powerPellet_list.append(PowerPellet(570, 490, screen))

def doesPowerPelletExistHere(x, y):
    for powerPellet in powerPellet_list:
        if powerPellet.x == x and powerPellet.y == y:
            return True
    return False

# for row in ghostNodes:
#     for val in row:
#         if val == 0:
#             print("0", end=' ')
#         else:
#             print("1", end=' ')
#     print()

placePowerPellets()
placePellets()
createGhostPath()

# create ghost
ghost = Ghost(8, 14, ghostNodes)

def isColliding(obj1, obj2):
    distSquared = (obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2

    if distSquared <= (obj1.rad + obj2.rad)**2:
        return True
    else:
        return False

# game loop
running = True
while running:
    # loop through all pygame events--------------
    for event in pygame.event.get():

        # checks if user presses the x in the window
        if event.type == pygame.QUIT:
            running = False

        # key event handler-------------------------
        if event.type == pygame.KEYDOWN:

            if gameStarted == False:
                gameStarted = True

            if event.key == pygame.K_LEFT:
                player.dirX = -1
                player.dirY = 0 # set to 0 in case user presses an arrow while holding down another arrow
                # getPath()

            if event.key == pygame.K_RIGHT:
                player.dirX = 1
                player.dirY = 0
                # getPath()

            if event.key == pygame.K_UP:
                player.dirY = -1
                player.dirX = 0
                # getPath()

            if event.key == pygame.K_DOWN:
                player.dirY = 1
                player.dirX = 0
                # getPath()

    update()
    draw()
    pygame.display.update()

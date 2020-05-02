import pygame
import time
from player import Player
from pygame import image, Color
from pellet import Pellet
from powerPellet import PowerPellet
from ghostNode import Node
from ghost import Ghost
from tunnel import Tunnel

pygame.init()

# window dimensions
w = 600
h = 620
frameCounter = 0
gameStarted = False

# create screen
firstMove = False

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

    #we want the ghost to take the starting path until it has left home
    if player.hasMoved() and not ghost.isLeaving:

        #reset all nodes to discoverable
        for row in ghostNodes:
            for val in row:
                if val != 0 and val != ghostNodes[12][14] and val != ghostNodes[12][15]:
                    val.status = 0

        node = player.findNode(ghostNodes)

        #if ghost has no path, get a new one
        if len(ghost.bestPath) < 1:
            #print(node.x, node.y)
            ghost.bestPath = []
            ghost.getPath(ghost.currentNode, node)
            ghost.shortestSize = 9223372036854775807

        else:
            #see if ghost's current target is still close to pacman
            tol = 3 #number of indeices apart the nodes can be
            currX = ghost.bestPath[len(ghost.bestPath) -1].idX
            currY = ghost.bestPath[len(ghost.bestPath) -1].idY
            newX = node.idX
            newY = node.idY

            #if the previous node is within tolerance nodes of the new node
            if currX > newX + tol or currX < newX -tol or currY > newY + tol or currY < newY -tol:
                ghost.bestPath = []
                ghost.getPath(ghost.currentNode, node)
                ghost.shortestSize = 9223372036854775807

    #if the player is still, find the exact node the player is on
    elif firstMove == True and not ghost.isLeaving:
        node = player.findNode(ghostNodes)
        #see if ghost's current target is still close to pacman
        if len(ghost.bestPath) < 1:
            return

        curr = ghost.bestPath[len(ghost.bestPath) -1]

        #if the ghost's target is not the same node as pacman, get a new path
        if curr != node:
            ghost.bestPath = []
            ghost.getPath(ghost.currentNode, node)
            ghost.shortestSize = 9223372036854775807


#---------------------------------------------------------------------------
def update():

    global player
    global frameCounter
    global ghost
    global prevNode
    global firstMove
    
    # keeps track of how many frames the current animation has been played for
    # frameCounter does not count during the pause before death animation
    if player.isLiving == True or (player.isLiving == False and player.pauseDone == True):
        frameCounter = (frameCounter + 1) % 100

    # walking animation
    if frameCounter % player.animationRate == 0 and player.hasMoved() and player.isLiving == True:
        # change the player.frame_alive every player.animationRate number of frames
        player.frame_alive = (player.frame_alive + 1) % len(player.imgs_alive)

    # death animation
    # pause for 1 second
    if player.isLiving == False and player.pauseDone == False:
        time.sleep(1.0)
        player.pauseDone = True

    if frameCounter % player.animationRate == 0 and player.pauseDone == True:
        # change the player.frame_dead every player.animationRate number of frames
        player.frame_dead = (player.frame_dead + 1) % len(player.imgs_dead)
        if player.frame_dead == len(player.imgs_dead) - 1:
            ghost.deathEvents()

    if player.isLiving == True:
        player.move()

        # only start moving the ghost if the player has made an input
        if firstMove == True:
            tunnel.teleportPlayer(player)
            getPath()
            ghost.move(player)

    # check if pacman and ghost collide
    if isColliding(player, ghost):
        # play death animation and remove a life
        player.deathEvents()
        firstMove = False

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

        for node in ghost.bestPath:
            pygame.draw.circle(screen, (0, 255, 0), (node.x, node.y), 2)

        # display the current score
        drawText("Score: " + str(player.score), 20, 0, 580, False)

        # display the current number of lives
        sprite = pygame.transform.scale(player.imgs_alive[2], (20, 20))

        if player.lives >= 3:
            screen.blit(sprite, (530, 580))

        if player.lives >= 2:
            screen.blit(sprite, (555, 580))

        if player.lives >= 1:
            screen.blit(sprite, (580, 580))

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

    while y < 580 / pathScale:
        ghostNodes.append([])
        x = 0

        while x < 600 / pathScale:
            targetX = 10 + (x*pathScale)
            targetY = 10 + (y*pathScale)

            if checkDotPoint(targetX, targetY, 1):
                ghostNodes[currY].append(Node(targetX, targetY, x, currY))

            else:
                ghostNodes[currY].append(0)

            x += 1
        y += 1
        currY += 1

    # for row in ghostNodes:
    #     for val in row:
    #         if val == 0:
    #             print("0", end=' ')
    #         else:
    #             print("1", end=' ')
    #     print()

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

placePowerPellets()
placePellets()
createGhostPath()

# create ghost
ghost = Ghost(14, 14, ghostNodes)

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
                player.intendedDirX = -1
                player.intendedDirY = 0
                firstMove = True

            if event.key == pygame.K_RIGHT:
                player.intendedDirX = 1
                player.intendedDirY = 0
                firstMove = True

            if event.key == pygame.K_UP:
                player.intendedDirX = 0
                player.intendedDirY = -1
                firstMove = True

            if event.key == pygame.K_DOWN:
                player.intendedDirX = 0
                player.intendedDirY = 1
                firstMove = True

    if player.isMoveValid(player.intendedDirX, player.intendedDirY):
        # if the intended move is not running into a wall, move as normal
        player.dirX = player.intendedDirX
        player.dirY = player.intendedDirY

        # reset intended move
        player.intendedDirX = None
        player.intendedDirY = None


    update()
    draw()
    pygame.display.update()
    #pygame.time.Clock().tick_busy_loop(200)

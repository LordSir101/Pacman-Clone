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

startTime = 0

# pre load background image
pygame.image.load('colourmap.png').convert()

image_rect = pygame.image.load('colourmap.png').convert().get_rect()
image_surface = pygame.Surface((image_rect.width, image_rect.height))
image_surface.blit(pygame.image.load("colourmap.png"), image_rect)

# have the ghost get the path to its target
pinky_node = player.findNode(ghostNodes)
def get_pinky_node():
    global pinky_node
    # global ghostNodes
    future_pos = player.findNode(ghostNodes)
    fpX = future_pos.idX
    fpY = future_pos.idY
    # 14 0 /  14 29
    if fpY == 14:
        return player.findNode(ghostNodes)

    count = 1
    if player.dirY < 0:
        while ghostNodes[fpY][fpX] != 0 and count < 5:
            count += 1
            fpY -= 1
        fpY += 1

    elif player.dirY > 0:
        while ghostNodes[fpY][fpX] != 0 and count < 5:
            count += 1
            fpY += 1
        fpY -= 1

    elif player.dirX < 0:
        while ghostNodes[fpY][fpX] != 0 and count < 5:
            count += 1
            fpX -= 1
        fpX += 1

    elif player.dirX > 0:
        while ghostNodes[fpY][fpX] != 0 and count < 5:
            count += 1
            fpX += 1
        fpX -= 1
    pinky_node = ghostNodes[fpY][fpX]
    return ghostNodes[fpY][fpX]

sudo_node = [0, 0]  # [x] [y]
def get_inky_node():
    global sudo_node
    global pinky_node
    global last_inky_node

    #Inky targets a point on a line drawn through inky, through paccman to the opposite side
    sudo_node[0] = max(int(30), min(int(570), int(player.x + (player.x - ghost.x))))
    sudo_node[1] = max(int(30), min(int(550), int(player.y + (player.y - ghost.y))))
    # print(player.findNode(ghostNodes, [sudo_node[0], sudo_node[1]]))
    node = player.findNode(ghostNodes, [sudo_node[0], sudo_node[1]])
    if node is None and last_inky_node is None:
        return player.findNode(ghostNodes)
    else:
        last_inky_node = node
        return node
last_inky_node = None
def getPathInky():
    global last_inky_node
    if player.hasMoved() and not ghostBlue.isLeaving:
        #reset all nodes to discoverable
        for row in ghostNodes:
            for val in row:
                if val != 0 and val != ghostNodes[12][14] and val != ghostNodes[12][15]:
                    val.status = 0

        node = get_inky_node()
        if node is None:
            node = player.findNode(ghostNodes)

        #if ghost has no path, get a new one
        if len(ghostBlue.bestPath) < 1:
            #print(node.x, node.y)
            ghostBlue.bestPath = []
            ghostBlue.getPath(ghost.currentNode, node)
            ghostBlue.shortestSize = 9223372036854775807

        else:
            tol = 3 #number of indeices apart the nodes can be
            currX = ghostBlue.bestPath[len(ghostBlue.bestPath) -1].idX
            currY = ghostBlue.bestPath[len(ghostBlue.bestPath) -1].idY
            newX = node.idX
            newY = node.idY

            #if the previous node is not within tolerance nodes of the new node
            if currX > newX + tol or currX < newX -tol or currY > newY + tol or currY < newY -tol:
                ghostBlue.bestPath = []
                ghostBlue.getPath(ghostBlue.currentNode, node)
                ghostBlue.shortestSize = 9223372036854775807

def getPathPinky(): # TODO: Need to do implement alternate route after reaching first node
    # we want the ghost to take the starting path until it has left home
    if player.hasMoved() and not ghostPink.isLeaving:

        #reset all nodes to discoverable
        for row in ghostNodes:
            for val in row:
                if val != 0 and val != ghostNodes[12][14] and val != ghostNodes[12][15]:
                    val.status = 0
        node = get_pinky_node()
        # node = player.findNode(ghostNodes)
        #if ghost has no path, get a new one
        if len(ghostPink.bestPath) < 1:
            #print(node.x, node.y)
            ghostPink.bestPath = []
            ghostPink.getPath(ghost.currentNode, node)
            ghostPink.shortestSize = 9223372036854775807

        else:
            tol = 3 #number of indeices apart the nodes can be
            currX = ghostPink.bestPath[len(ghostPink.bestPath) -1].idX
            currY = ghostPink.bestPath[len(ghostPink.bestPath) -1].idY
            newX = node.idX
            newY = node.idY

            #if the previous node is not within tolerance nodes of the new node
            if currX > newX + tol or currX < newX -tol or currY > newY + tol or currY < newY -tol:
                ghostPink.bestPath = []
                ghostPink.getPath(ghostPink.currentNode, node)
                ghostPink.shortestSize = 9223372036854775807

def getPathBlinky():
    #we want the ghost to take the starting path until it has left home
    if player.hasMoved() and not ghost.isLeaving:
        # ghost.bestPath = []
        # ghost.getPath(ghost.currentNode, node)
        # ghost.shortestSize = 9223372036854775807

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

            #if the previous node is not within tolerance nodes of the new node
            if currX > newX + tol or currX < newX -tol or currY > newY + tol or currY < newY -tol:
                ghost.bestPath = []
                ghost.getPath(ghost.currentNode, node)
                ghost.shortestSize = 9223372036854775807

    #if the player is still, find the exact node the player is on
    elif firstMove == True and not ghost.isLeaving:
        node = player.findNode(ghostNodes)
        # #see if ghost's current target is still close to pacman
        if len(ghost.bestPath) < 1:
            return

        curr = ghost.bestPath[len(ghost.bestPath)-1]

        #if the ghost's target is not the same node as pacman, get a new path
        if curr.x != node.x or curr.y != node.y:
            #reset all nodes to discoverable
            for row in ghostNodes:
                for val in row:
                    if val != 0 and val != ghostNodes[12][14] and val != ghostNodes[12][15]:
                        val.status = 0

            ghost.bestPath = []
            ghost.getPath(ghost.currentNode, node)
            ghost.shortestSize = 9223372036854775807

#reset game values to start new game
def reset():
    pellet_list = []
    powerPellet_list = []

    frameCounter = 0
    startTime = 0

    # reset player data
    player.reset()

    placePowerPellets()
    placePellets()

#---------------------------------------------------------------------------
def update():

    global player
    global frameCounter
    global ghost
    global ghostBlue
    global ghostPink
    global prevNode
    global firstMove

    # pygame.time.Clock().tick(40)

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
            ghostPink.deathEvents()
            ghostBlue.deathEvents()
            global startTime
            startTime = time.time()

    if player.isLiving == True:
        player.move()

        # only start moving the ghost if the player has made an input
        if firstMove == True:
            tunnel.teleportPlayer(player)
            getPathBlinky()
            getPathPinky()
            getPathInky()

            ghost.move(player)
            if time.time() - startTime > 5:
                ghostPink.move(player)
            if time.time() - startTime > 10:
                ghostBlue.move(player)


    # check if pacman and ghost collide
    ghosts = [ghost, ghostBlue, ghostPink]
    for spooker in ghosts:
        if isColliding(player, spooker):
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
    global player
    global ghost
    global ghostPink
    global ghostBlue

    if gameStarted == False:
        # text, size, xpos, ypos, center text at point
        drawText("Click Any Button To Play", 45, w/2, h/2, True)

    elif player.lives <=0 :
        drawText("Game Over", 45, w/2, h/2, True)

    else:
        pygame.draw.rect(screen,(0, 0, 0),(0, 0, w, h))

        # background
        #screen.blit(pygame.image.load('colourmap.png').convert(), (0,0))
        screen.blit(image_surface, image_rect)

        for pellet in pellet_list:
            pellet.draw()

        for powerPellet in powerPellet_list:
            powerPellet.draw()

        player.draw(screen)

        ghost.draw(screen, (255, 0, 0))
        ghostPink.draw(screen, (255, 130, 130))
        ghostBlue.draw(screen, (100, 220, 255))
        drawText("Score: " + str(player.score), 20, 0, 580, False)

        for node in ghostBlue.bestPath:
            pygame.draw.circle(screen, (0, 255, 0), (node.x, node.y), 2)

        # display the current score
        drawText("Score: " + str(player.score), 20, 0, 580, False)

        # display the current number of lives
        sprite = pygame.transform.scale(player.imgs_alive[2], (20, 20))
        for i in range(player.lives):
            screen.blit(sprite, (580 - 25 * i, 580))


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

#   create ghosts
ghostBlue = Ghost(14, 14, ghostNodes)
ghostPink = Ghost(14, 14, ghostNodes)
ghost = Ghost(14, 14, ghostNodes)

def isColliding(obj1, obj2):

    distSquared = (obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2

    if distSquared <= (obj1.rad + obj2.rad)**2:
        return True
    else:
        return False

# game loop
running = True
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

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
                #startTime = time.time()

            #keep updating starting time until player makes first move
            if not firstMove:
                # if the game was over, reset values when player starts playing
                if player.lives <= 0:
                    reset()
                    break

                # we need to update time so that the ghosts will only start moving
                # at specific times when the player starts playing again
                startTime = time.time()

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
    # cap fps at 60
    pygame.time.Clock().tick_busy_loop(60)

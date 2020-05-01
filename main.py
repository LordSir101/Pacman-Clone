import pygame
from player import Player
from pellet import Pellet
from powerPellet import PowerPellet
from pygame import image, Color
from ghostNode import Node
from ghost import Ghost
from tunnel import Tunnel

# temp libraries
from random import seed
from random import randint

pygame.init()

#window dimensions
w = 600
h = 600
frameCounter = 0
time = 0
gameStarted = False
firstMove = False


#create screen
screen = pygame.display.set_mode((w, h))

#title and icon
pygame.display.set_caption("Game thing")

#create player
player = Player(w, h)

#create pellet array
pellet_list = []
num_pellets = 50
nodeList = [] #list of actual nodes
#create powerPellet array
powerPellet_list = []

#create ghostNodes array
ghostNodes = []

# create two way tunnel
tunnel = Tunnel(10, 290, w-10, 290)   # (x1, y1, x2, y2)

#have the ghost get the path to its target

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
        node = get_inky_node()
        if node is None:
            node = player.findNode(ghostNodes)
        ghostBlue.bestPath = []
        ghostBlue.getPath(ghostBlue.currentNode, node)
        ghostBlue.shortestSize = 9223372036854775807

        # reset all nodes to discoverable
        for row in ghostNodes:
            for val in row:
                if val == 0:
                    pass
                else:
                    val.status = 0
def getPathPinky(): # TODO: Need to do implement alternate route after reaching first node
    # we want the ghost to take the starting path until it has left home
    if player.hasMoved() and not ghost.isLeaving:
        node = get_pinky_node()
        # node = player.findNode(ghostNodes)
        ghostPink.bestPath = []
        ghostPink.getPath(ghostPink.currentNode, node)
        ghostPink.shortestSize = 9223372036854775807

        #reset all nodes to discoverable
        for row in ghostNodes:
            for val in row:
                if val == 0:
                    pass
                else:
                    val.status = 0

def getPathBlinky():
    #we want the ghost to take the starting path until it has left home
    if player.hasMoved() and not ghost.isLeaving:
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
    global time
    global firstMove

    checkTime = 30

    #keeps track of how many frames the current animation has been played for
    frameCounter = (frameCounter + 1) % player.animationRate + 2 #iterates from 0 to animationRate + 1
    if frameCounter > player.animationRate and player.hasMoved():
        player.changeFrame()

    player.move()

    #tells us when the player has started moving pacman
    if player.hasMoved():
        firstMove = True

    #only start moving the ghost if the player has made an input
    if firstMove == True:
        tunnel.teleportPlayer(player)
        if frameCounter % 3 == 0:
            pass
        if frameCounter % 3 == 1:
            getPathPinky()
            getPathBlinky()
            getPathInky()
        if frameCounter % 3 == 2:
            pass
        ghost.move(player)
        ghostPink.move(player)
        ghostBlue.move(player)

    #draw pellets and power pellets
    for pellet in reversed(pellet_list):
        if pellet.checkCollision(player):
            pellet_list.remove(pellet)
            player.score += pellet.point_value

    for powerPellet in reversed(powerPellet_list):
        if powerPellet.checkCollision(player):
            powerPellet_list.remove(powerPellet)
            player.score += powerPellet.point_value


#---------------------------------------------------------------------------
def draw():
    if gameStarted == False:
        #text, size, xpos, ypos, center text at point
        drawText("Click Any Button To Play", 45, w/2, h/2, True)
    else:
        pygame.draw.rect(screen,(0, 0, 0),(0, 0, w, h))
        #background
        screen.blit(pygame.image.load('colourmap.png'), (0,0))
        for pellet in pellet_list:
            pellet.draw()

        for powerPellet in powerPellet_list:
            powerPellet.draw()

        global player
        player.draw(screen)

        global ghost
        global ghostPink
        global ghostBlue
        ghost.draw(screen, (255, 0, 0))
        ghostPink.draw(screen, (255, 130, 130))
        ghostBlue.draw(screen, (100, 220, 255))
        drawText("Score: " + str(player.score), 20, 0, 580, False)

def drawText(text, size, x, y, center):
    font = pygame.font.Font('freesansbold.ttf', size)
    overText = font.render(text, True, (255,255,255))
    textW = overText.get_width()
    textH = overText.get_height()

    if center:
        #centers the text at the specified point
        screen.blit(overText, (int(x - textW/2), int(y - textH/2)))
    else:
        screen.blit(overText, (x, y))

#create ghost path and place dots on map-----------------------------------------------------------------------
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

#   create ghost
ghostBlue = Ghost(14, 14, ghostNodes)
ghostPink = Ghost(14, 14, ghostNodes)
ghost = Ghost(14, 14, ghostNodes)


# To Check FPS --------------------------------------
# clock = pygame.time.Clock()
# press = False
# lowest = 100000
# highest =0
# loops = 0


#game loop
running = True
while running:

    # loops += 1
    # clock.tick()
    # if clock.get_fps() < lowest and loops > 100:
    #     lowest = clock.get_fps()
    # elif clock.get_fps() > highest:
    #     highest = clock.get_fps()
    #
    # pygame.display.set_caption(str(clock.get_fps()))

    # pygame.display.flip()
    #loop through all pygame events--------------
    for event in pygame.event.get():

        #checks if user presses the x in the window
        if event.type == pygame.QUIT:
            running = False

        #key event handler-------------------------
        if event.type == pygame.KEYDOWN:

            if gameStarted == False:
                gameStarted = True

            if event.key == pygame.K_LEFT:
                player.dirX = -1
                player.dirY = 0 #set to 0 in case user presses an arrow while holding down another arrow
                #getPath()

            if event.key == pygame.K_RIGHT:
                player.dirX = 1
                player.dirY = 0
                #getPath()

            if event.key == pygame.K_UP:
                player.dirY = -1
                player.dirX = 0
                #getPath()

            if event.key == pygame.K_DOWN:
                player.dirY = 1
                player.dirX = 0
                #getPath()
            if event.key == pygame.K_SPACE:
                player.dirY = 0
                player.dirX = 0

    update()
    draw()
    pygame.display.update()

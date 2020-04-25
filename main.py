import pygame
from player import Player
from pellet import Pellet
from powerPellet import PowerPellet
from pygame import image, Color
from ghostNode import Node
from ghost import Ghost

# temp libraries
from random import seed
from random import randint

pygame.init()

#window dimensions
w = 600
h = 600
frameCounter = 0
gameStarted = False


#create screen
screen = pygame.display.set_mode((w, h))

#title and icon
pygame.display.set_caption("Game thing")

#create player
player = Player(w, h)




#create pellet array
pellet_list = []
num_pellets = 50
<<<<<<< HEAD
nodeList = [] #list of actual nodes

=======

#create powerPellet array

powerPellet_list = []

#create ghostNodes array
ghostNodes = []
>>>>>>> 422b3fd157a32ae7fe181d32a7a6c4c794d0ab06

#for i in range(0, num_pellets):
    # append a new pellet object to the pellet_list[]
    #pellet_list.append(Pellet(randint(100, 700), randint(100, 500), screen))

def getPath():
    node = player.findNode(ghostNodes)
    ghost.bestPath = []
    ghost.getPath(ghost.currentNode, ghost.currentNode, node)
    ghost.shortestSize = 9223372036854775807
    ghost.testPath = []

    #node = None
    for row in ghostNodes:
        for val in row:
            if val == 0:
                pass
            else:
                val.status = 0

#---------------------------------------------------------------------------
def update():
    #print("in update")
    global player
    global frameCounter
    global ghost
    global prevNode

    #keeps track of how many frames the current animation has been played for
    frameCounter = (frameCounter + 1) % player.animationRate + 2 #iterates from 0 to animationRate + 1
    if frameCounter > player.animationRate and player.hasMoved():
        player.changeFrame()

    player.move()

    #node = player.findNode(ghostNodes)
    #ghost.getPath(ghost.currentNode, ghost.currentNode, node)
    ghost.move(player)

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
        #background
        screen.blit(pygame.image.load('colourmap.png'), (0,0))
        for pellet in pellet_list:
            pellet.draw()

        for powerPellet in powerPellet_list:
            powerPellet.draw()

        global player
        player.draw(screen)

        global ghost
        ghost.draw(screen)

        #for testing

        #pygame.draw.circle(screen, (0, 255, 0), [int(player.x), int(player.y)], 1)
        #pygame.draw.rect(screen, (255, 0, 0), player.getHitbox())


        drawText("Score: " + str(player.score), 20, 0, 0, False)


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


dotimage = image.load('pacmandotmap.png')
pathImage = image.load('movemap.png')
def checkDotPoint(x, y, image):
    global dotimage
    global pathImage

    image = dotimage if image == 0 else pathImage
    if image.get_at((int(x), int(y))) == Color('black'):
        return True
    return False

<<<<<<< HEAD

pathScale = 20
#ghostNodes = [[0 for x in range(int(10+(580/pathScale)*pathScale))] for y in range(int(10 + (560/pathScale)*pathScale))]
ghostNodes = []
#ghostNodes.append([])
def createGhostPath():
    global ghostNodes
    global screen

    y = 0
    currY = 0

    while y < 560 / pathScale:  #30
        ghostNodes.append([])
        x = 0
        #currX = 0

        while x < 580 / pathScale: #29
            if checkDotPoint(10+x*pathScale, 10 + y*pathScale, 1):
                ghostNodes[currY].append(Node(10+x*pathScale, 10+y*pathScale, x, currY))
                #pacDots[i].status = 0
                #i += 1
            else:
                ghostNodes[currY].append(0)

            #currX += 1
            x += 1
=======
def placePellets():
    global pellet_list
    global screen

    x = 0
    while x < 30:  #30
        y = 0
        while y < 29: #29
            currX = 10 + (x*20)
            currY = 10 + (y*20)
            if checkDotPoint(currX, currY, 0) and not doesPowerPelletExistHere(currX, currY):
                pellet_list.append(Pellet(currX, currY, screen))
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
>>>>>>> 422b3fd157a32ae7fe181d32a7a6c4c794d0ab06

        y += 1
        currY += 1



# for row in ghostNodes:
#     for val in row:
#         if val == 0:
#             print("0", end=' ')
#         else:
#             print("1", end=' ')
#     print()
#580
#560

def placeDots():
    global pellet_list
    global pathScale

    x = 0

    while x < 580 / pathScale:
        y = 0
        while y < 560 / pathScale:
<<<<<<< HEAD
            if checkDotPoint(10+x*pathScale, 10 + y*pathScale, 0):
                #add a coordinate for possible nodes
                pellet_list.append(Pellet(10+x*pathScale, 10+y*pathScale, screen))
=======
            if checkDotPoint(10 + (x*pathScale), 10 + (y*pathScale), 1):
                ghostNodes.append(Node(10 + (x*pathScale), 10 + (y*pathScale)))
>>>>>>> 422b3fd157a32ae7fe181d32a7a6c4c794d0ab06
                #pacDots[i].status = 0
                #i += 1
            y += 1
        x += 1

<<<<<<< HEAD



# #input the x and y position of ghostNodes[0]
# def createEdges(x, y):
#     global ghostNodes
#     global pathScale
#     #for i in range(prev + 1, len(ghostNode) -1):
#
#     node = Node(x, y)
#
#     if node.right == None:
#         #position of where right node should be
#         rightX = x + (10 + x * pathScale)
#         rightY = y
#
#         for j in range(0, len(ghostNode) - 1)
#             newX = ghostNodes[j][0]
#             newY = ghostNodes[j][1]
#             if newX == rightX and newY == rightY:
#                 newNode = Node(newX, newY)
#                 node.right = newNode
#                 newNode.left = node
#                 createEdges(newX, newY)



placeDots()
=======
placePowerPellets()
placePellets()
>>>>>>> 422b3fd157a32ae7fe181d32a7a6c4c794d0ab06
createGhostPath()


#create ghost
ghost = Ghost(8, 14, ghostNodes)
prevNode = player.findNode(ghostNodes)


#game loop
running = True
while running:
    #loop through all pygame events--------------
    for event in pygame.event.get():

        #checks if user presses the x in the window
        if event.type == pygame.QUIT:
            running = False

        #key event handler-------------------------
        if event.type == pygame.KEYDOWN:


            if event.key == pygame.K_p:
                getPath()
            if gameStarted == False:
                gameStarted = True

            #if event.key == pygame.K_SPACE:

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

        # we don't need to worry about keyups because pacman will always be moving and the user will pick which direction pacman moves

        if event.type == pygame.KEYUP:

            if not any(pygame.key.get_pressed()):
                player.dirX = 0
                player.dirY = 0


                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.dirX = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.dirY = 0




    update()
    draw()
    pygame.display.update()

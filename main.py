import pygame
from player import Player
from pellet import Pellet
from powerPellet import PowerPellet
from pygame import image, Color
from ghostNode import Node

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

#create powerPellet array

powerPellet_list = []

#create ghostNodes array
ghostNodes = []

'''
for i in range(0, num_pellets):
    # append a new pellet object to the pellet_list[]
    pellet_list.append(Pellet(randint(100, 700), randint(100, 500), screen))
'''

#---------------------------------------------------------------------------
def update():
    global player
    global frameCounter

    #keeps track of how many frames the current animation has been played for
    frameCounter = (frameCounter + 1) % player.animationRate + 2 #iterates from 0 to animationRate + 1
    if frameCounter > player.animationRate and player.hasMoved():
        player.changeFrame()

    player.move()

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

        #for testing
        '''
        pygame.draw.circle(screen, (0, 255, 0), [int(player.x), int(player.y)], 1)
        pygame.draw.rect(screen, (255, 0, 0), player.getHitbox())
        '''

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

#580
#560
def createGhostPath():
    global ghostNodes
    pathScale = 10

    x = 0

    while x < 580 / pathScale:
        y = 0
        while y < 560 / pathScale:
            if checkDotPoint(10 + (x*pathScale), 10 + (y*pathScale), 1):
                ghostNodes.append(Node(10 + (x*pathScale), 10 + (y*pathScale)))
                #pacDots[i].status = 0
                #i += 1
            y += 1
        x += 1

placePowerPellets()
placePellets()
createGhostPath()

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

            if gameStarted == False:
                gameStarted = True

            if event.key == pygame.K_LEFT:
                player.dirX = -1
                player.dirY = 0 #set to 0 in case user presses an arrow while holding down another arrow

            if event.key == pygame.K_RIGHT:
                player.dirX = 1
                player.dirY = 0

            if event.key == pygame.K_UP:
                player.dirY = -1
                player.dirX = 0

            if event.key == pygame.K_DOWN:
                player.dirY = 1
                player.dirX = 0

        # we don't need to worry about keyups because pacman will always be moving and the user will pick which direction pacman moves
        '''
        if event.type == pygame.KEYUP:

            if not any(pygame.key.get_pressed()):
                player.dirX = 0
                player.dirY = 0


                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.dirX = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.dirY = 0
        '''



    update()
    draw()
    pygame.display.update()

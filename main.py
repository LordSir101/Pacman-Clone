import pygame
from player import Player
from pellet import Pellet

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

for i in range(0, num_pellets):
    # append a new pellet object to the pellet_list[]
    pellet_list.append(Pellet(randint(100, 700), randint(100, 500), screen))

#---------------------------------------------------------------------------
def update():
    global player
    global frameCounter
    frameCounter += 1
    if frameCounter > player.animationRate:
        player.changeFrame()
        frameCounter = 0
    player.move()

    for pellet in reversed(pellet_list):
        if pellet.checkCollision(player):
            pellet_list.remove(pellet)
            player.score += 10

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

        global player
        player.draw(screen)
        #pygame.draw.circle(screen, (0, 255, 0), [int(player.x), int(player.y)], 1)
        #pygame.draw.rect(screen, (255, 0, 0), player.getHitbox())

        drawText("Score: " + str(player.score), 20, 0, 0, False)


def drawText(text, size, x, y, center):
    font = pygame.font.Font('freesansbold.ttf', size)
    overText = font.render(text, True, (255,255,255))
    textW = overText.get_width()
    textH = overText.get_height()
    if center:
        screen.blit(overText, (x - textW/2, y - textH/2))
    else:
        screen.blit(overText, (x, y))

#game loop
running = True
while running:
    #loop through all pygame events--------------
    for event in pygame.event.get():
        #checks if user presses the x in the windo
        if event.type == pygame.QUIT:
            running = False

        #key event handler-------------------------
        if event.type == pygame.KEYDOWN:

            if gameStarted == False:
                gameStarted = True

            #left arrow
            if event.key == pygame.K_LEFT:
                player.dirX = -1
                player.dirY = 0 #set to 0 in case user presses an arrow while holding down another arrow
                #inputLock = True
            if event.key == pygame.K_RIGHT:
                player.dirX = 1
                player.dirY = 0
                #inputLock = True
            if event.key == pygame.K_UP:
                player.dirY = -1
                player.dirX = 0
                #inputLock = True
            if event.key == pygame.K_DOWN:
                player.dirY = 1
                player.dirX = 0
                #inputLock = True

        if event.type == pygame.KEYUP:
            #if a key is being held down still, don't stop moving the sprite
            if not any(pygame.key.get_pressed()):
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.dirX = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.dirY = 0



    update()
    draw()
    pygame.display.update()

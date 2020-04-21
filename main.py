import pygame
from player import Player
from pellet import Pellet

# temp libraries
from random import seed
from random import randint

pygame.init()

#window dimensions
w = 800
h = 600

gameStarted = False
#create screen
screen = pygame.display.set_mode((w, h))

#title and icon
pygame.display.set_caption("Game thing")

#create player
player = Player(w, h)

#create pellet
# pellet1 = Pellet(400, 300, screen)

#create pellet array
pellet_list = []
num_pellets = 50

for i in range(0, num_pellets):
    # append a new pellet object to the pellet_list[]
    pellet_list.append(Pellet(randint(100, 700), randint(100, 500), screen))

#---------------------------------------------------------------------------
def update():
    global player
    player.move()

    for pellet in reversed(pellet_list):
        if pellet.checkCollision(player):
            pellet_list.remove(pellet)
            player.score += 10

#---------------------------------------------------------------------------
def draw():
    if gameStarted == False:
        #text, size, xpos, ypos, center text at point
        drawText("Click Any Button To Play", 64, w/2, h/2, True)
    else:
    #background
        BLACK=(0,0,0)
        screen.fill(BLACK)
        pygame.draw.rect(screen,BLACK,(5,5,w,h))

        for pellet in pellet_list:
            pellet.draw()

        global player
        screen.blit(player.sprite, (player.x - player.width/2, player.y - player.height/2))

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
            if event.key == pygame.K_RIGHT:
                player.dirX = 1
            if event.key == pygame.K_UP:
                player.dirY = -1
            if event.key == pygame.K_DOWN:
                player.dirY = 1

        if event.type == pygame.KEYUP:
            #left arrow
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.dirX = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player.dirY = 0


    update()
    draw()
    pygame.display.update()

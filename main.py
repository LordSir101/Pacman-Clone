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
num_pellets = 6

for i in range(0, num_pellets):
    # append a new pellet object to the pellet_list[]
    pellet_list.append(Pellet(randint(100, 700), randint(100, 500), screen))

#---------------------------------------------------------------------------
def update():
    global player
    player.move()

#---------------------------------------------------------------------------
def draw():
    if gameStarted == False:
        font = pygame.font.Font('freesansbold.ttf', 64)
        overText = font.render("Click Any Button To Play", True, (255,255,255))
        textW = overText.get_width()
        textH = overText.get_height()
        screen.blit(overText, (w/2 - textW/2, h/2 - textH))
    else:
    #background
        BLACK=(0,0,0)
        screen.fill(BLACK)
        pygame.draw.rect(screen,BLACK,(0,0,w,h))

        global player
        screen.blit(player.sprite, (player.x, player.y))

    # pellet1.draw()
    for i in range(0, len(pellet_list)):
        if pellet_list[i].isEaten == False:
            pellet_list[i].checkCollision(player.x, player.y)

        if pellet_list[i].isEaten == False:
            pellet_list[i].draw()

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

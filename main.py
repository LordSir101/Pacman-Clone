import pygame
from player import Player

pygame.init()

#window dimensions
w = 800
h = 600

#create screen
screen = pygame.display.set_mode((w, h))

#title and icon
pygame.display.set_caption("Game thing")



player = Player(w, h)

#---------------------------------------------------------------------------
def update():
    global player
    player.move()

#---------------------------------------------------------------------------
def draw():
    #background
    BLACK=(0,0,0)
    screen.fill(BLACK)
    pygame.draw.rect(screen,BLACK,(0,0,w,h))

    global player
    screen.blit(player.sprite, (player.x, player.y))

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

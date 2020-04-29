import pygame

class Tunnel:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1

        self.x2 = x2
        self.y2 = y2

        self.buffer = 10

    def teleportPlayer(self, player):
        # check if player is going through the tunnel from (x1, y1) to (x2, y2)
        if player.x >= self.x1 - self.buffer and player.x <= self.x1 + self.buffer:
            if (player.y >= self.y1 - self.buffer and
                player.y <= self.y1 + self.buffer and player.dirX == -1):

                # teleport player to other side
                player.x = self.x2
                player.y = self.y2

        # check if player is through the tunnel from (x2, y2) to (x1, y1)
        if player.x >= self.x2 - self.buffer and player.x <= self.x2 + self.buffer:
            if (player.y >= self.y2 - self.buffer and
                player.y <= self.y2 + self.buffer and player.dirX == 1):

                # teleport player to other side
                player.x = self.x1
                player.y = self.y1

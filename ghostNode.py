import pygame

class Node:
    def __init__(self, x, y, idX, idY):
        self.x = x
        self.y = y
        self.status = 0
        self.idX = idX
        self.idY = idY

    def intersectsPacman(self):
        print("intersecting")

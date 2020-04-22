import pygame

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = 0

        self.right = None
        self.left = None
        self.up = None
        self.down = None

    def intersectsPacman(self):
        print("intersecting")

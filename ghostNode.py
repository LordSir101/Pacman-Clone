import pygame

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = 0

    def intersectsPacman(self):
        print("intersecting")

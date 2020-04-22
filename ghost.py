from pygame import image, Color
import pygame
from ghostNode import Node

class Ghost:
    def __init__(self, x, y, ghostPath):

        self.currentNode = Node(x, y)
        self.nodes = ghostPath
        self.bestPath = []
        self.placeOnPath = 0


    def move(self):
        placeOnPath +=1
        self.x = self.bestPath[self.placeOnPath].x
        self.y = self.bestPath[self.placeOnPath].y

    def getPath(self, start, root, target):
        #endOfPath


    def draw(self, screen):
        pygame.draw.circle(self.screen, (255, 0, 0), [self.x, self.y], self.rad)

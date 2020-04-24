from pygame import image, Color
import pygame
from ghostNode import Node

class Ghost:
    def __init__(self, x, y, ghostPath):
        #start at 14 10
        self.nodes = ghostPath
        self.bestPath = []
        self.testPath = []
        self.placeOnPath = 0
        self.shortestSize = 9223372036854775807
        self.currentNode = self.nodes[y][x]  #ypos #xpos
        #self.prevX = x
        #self.prevY = y
        self.x = self.currentNode.x
        self.y = self.currentNode.y

        self.dirX = 0
        self.dirY = 0
        self.vel = 0

    def move(self, player):
        #print(len(self.bestPath))
        self.placeOnPath +=1
        if self.placeOnPath < len(self.bestPath):
            self.x = self.bestPath[self.placeOnPath].x
            self.y = self.bestPath[self.placeOnPath].y
            self.currentNode = self.bestPath[self.placeOnPath]
            
        #getPath()

    #start and root are the same node initially
    #root is the originonal start, start is the recusive start

    def getPath(self, start, root, target):

        self.placeOnPath = 0
        endOfPath = False

        #set status to being checked
        start.status = 1
        parent = root

        self.testPath.append(start)

        prevX = start.idX
        prevY = start.idY
        #print("start" + str(start.x) + " " + str(start.y))
        print("target" + str(target.x) + " " + str(target.y))


        #print(str(prevX) + " " + str(prevY))

        #check if current is the target node
        if start.x == target.x and start.y == target.y:
            print("target found")
            #check if this is the shortest path
            if len(self.testPath) < self.shortestSize:
                self.shortestSize = len(self.testPath)

                    #print(str(val.x) + " " + str(val.y), end=' ' )
                self.bestPath = self.testPath.copy()

            #undiscover target node
            target.status = 0

            #remove goal from current path so we can check other paths from the previous node
            self.testPath.pop()
            endOfPath = True

        if not endOfPath:
            #visit each neighbor and check all thier undiscovered neighbors
            #RIGHT
            nextX = prevX+ 1
            nextY = prevY
            if nextY < len(self.nodes):
                if nextX < len(self.nodes[nextY]):
                    if self.nodes[nextY][nextX] != 0 and self.nodes[nextY][nextX].status == 0:
                        #print("right")

                        new = self.nodes[nextY][nextX]
                        self.getPath(new, parent, target)
                        #new.status = 0


            #LEFT
            nextX = prevX -1
            nextY = prevY

            if nextY < len(self.nodes):
                if nextX < len(self.nodes[nextY]):
                    if self.nodes[nextY][nextX] != 0 and self.nodes[nextY][nextX].status == 0:
                        #print("left")
                        new = self.nodes[nextY][nextX]
                        self.getPath(new, parent, target)
                        #new.status = 0


            #UP
            nextX = prevX
            nextY = prevY -1

            if nextY < len(self.nodes):
                if nextX < len(self.nodes[nextY]):
                    if self.nodes[nextY][nextX] != 0 and self.nodes[nextY][nextX].status == 0:
                        #print("up")
                        new = self.nodes[nextY][nextX]
                        self.getPath(new, parent, target)
                        #new.status = 0


            #DOWN
            nextX = prevX
            nextY = prevY + 1

            if nextY < len(self.nodes):
                if nextX < len(self.nodes[nextY]):
                    if self.nodes[nextY][nextX] != 0 and self.nodes[nextY][nextX].status == 0:
                        #print("down")
                        new = self.nodes[nextY][nextX]
                        self.getPath(new, parent, target)
                        #new.status = 0


            #after checking neighbors, remove from currentPath
            #start.status = 0
            self.testPath.remove(start)


    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), [self.x, self.y], 10)

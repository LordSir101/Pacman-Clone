from pygame import image, Color
import pygame
from ghostNode import Node

class Ghost:
    def __init__(self, x, y, ghostPath):
        #start at 14 10
        self.nodes = ghostPath
        #a path to help the ghost leave home
        self.bestPath = [self.nodes[14][14], self.nodes[13][14], self.nodes[12][14], self.nodes[11][14] ] #
        self.testPath = []
        self.placeOnPath = 1
        self.shortestSize = 9223372036854775807
        self.currentNode = self.nodes[y][x]  #ypos #xpos

        self.x = self.currentNode.x
        self.y = self.currentNode.y

        self.dirX = 0
        self.dirY = 0
        self.vel = 2
        self.alpha = 0.3 #how smooth the move animation is
        self.isLeaving = True

        self.setDirection()

    def move(self, player):
        #print(len(self.bestPath))

        #when the ghost reaches a node in its path, move to the next node
        if self.placeOnPath < len(self.bestPath):
            tolerance  = self.alpha * self.alpha #how close a ghost has to be to a node to consider it "reached"
            distSquaredX = (self.x - self.bestPath[self.placeOnPath].x)**2
            distSquaredY = (self.y - self.bestPath[self.placeOnPath].y)**2

            if distSquaredX < tolerance and distSquaredY < tolerance:
                #when the ghost reaches a node in its path, move to the next node
                self.placeOnPath +=1
                self.setDirection()

            #move the ghost
            if self.placeOnPath < len(self.bestPath):
                self.currentNode = self.bestPath[self.placeOnPath]
                self.lerp(self.alpha) #smooth the movement between two points
            #if there is no path for some reason, stay still
            else:
                self.dirX = 0
                self.dirY = 0
        if self.placeOnPath == len(self.bestPath):
            self.isLeaving = False
            #close the entrance to home so the ghost cant go back in
            self.nodes[12][14] = 0
            self.nodes[12][15] = 0

    def setDirection(self):
        if self.placeOnPath < len(self.bestPath):
            #divide distance by magnitude of distance to get direction of next point
            distX = self.bestPath[self.placeOnPath].x - self.currentNode.x
            distY = self.bestPath[self.placeOnPath].y - self.currentNode.y

            magX = abs(distX)
            magY = abs(distY)

            #if the magnitude is 0 this means that the ghost is on the same axis as the point
            #therefore we do not move in that direction
            self.dirX = distX / magX if magX != 0 else 0
            self.dirY = distY / magY if magY != 0 else 0

    def lerp(self, alpha):
        self.x += self.vel * self.dirX
        self.y += self.vel * self.dirY


    #start and root are the same node initially
    #root is the originonal start, start is the recusive start
    def getPath(self, start, target):

        self.placeOnPath = 0
        endOfPath = False

        #set status to being checked
        start.status = 1

        self.testPath.append(start)

        prevX = start.idX
        prevY = start.idY

        #check if current is the target node
        if start.x == target.x and start.y == target.y:
            #check if this is the shortest path
            if len(self.testPath) < self.shortestSize:
                self.shortestSize = len(self.testPath)
                self.bestPath = self.testPath.copy()

            #undiscover target node
            target.status = 0

            #remove goal from current path so we can check other paths from the previous node
            self.testPath.pop()
            endOfPath = True

        if not endOfPath:
            #visit each neighbor and check all thier undiscovered neighbors
            #RIGHT
            rightX = prevX+ 1
            rightY = prevY

            #LEFT
            leftX = prevX -1
            leftY = prevY

            #UP
            upX = prevX
            upY = prevY -1

            #DOWN
            downX = prevX
            downY = prevY + 1

            #define the neighbor nodes
            #set it to 0 (invalid) if index is out of range
            right = self.nodes[rightY][rightX] if rightY < len(self.nodes) and rightX < len(self.nodes[rightY]) else 0
            left = self.nodes[leftY][leftX] if leftY < len(self.nodes) and leftX < len(self.nodes[leftY]) else 0
            up = self.nodes[upY][upX] if upY < len(self.nodes) and upX < len(self.nodes[upY]) else 0
            down = self.nodes[downY][downX] if downY < len(self.nodes) and downX < len(self.nodes[downY]) else 0

            #get distance between neighbor and target node
            #if node invalid, set to max distance
            distRight = self.getDist(right, target) if right != 0 else 9223372036854775807
            distLeft = self.getDist(left, target) if left != 0 else 9223372036854775807
            distUp = self.getDist(up, target) if up != 0 else 9223372036854775807
            distDown = self.getDist(down, target) if down!= 0 else 9223372036854775807

            neighbors = [distRight, distLeft, distUp, distDown]
            lookingForClosestNeighbor = True

            #check closest neighbor until one is found that is a valid node
            while lookingForClosestNeighbor:

                closest = min(neighbors)

                #if the right neighbor is the closest and a valid node, visit it
                if closest == distRight and right != 0 and right.status == 0:
                    self.gotoNode(right, target)
                    lookingForClosestNeighbor = False
                elif closest == distLeft and left != 0 and left.status == 0:
                    self.gotoNode(left, target)
                    lookingForClosestNeighbor = False
                elif closest == distUp and up != 0 and up.status == 0:
                    self.gotoNode(up, target)
                    lookingForClosestNeighbor = False
                elif closest == distDown and down != 0 and down.status == 0:
                    self.gotoNode(down, target)
                    lookingForClosestNeighbor = False

                #if the closest node is not valid, remove it from possible neighbors and try again
                else:
                    neighbors.remove(closest)
                    #if there are no valid neighbors, stop searching
                    if len(neighbors) == 0:
                        lookingForClosestNeighbor = False

            #after checking neighbors, remove from currentPath
            self.testPath.remove(start)

    def gotoNode(self, node, target):
        self.getPath(node, target)


    def getDist(self, start, target):
        distSquaredX = (start.x - target.x)**2
        distSquaredY = (start.y - target.y)**2
        return distSquaredX + distSquaredY

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), [int(self.x), int(self.y)], 10)

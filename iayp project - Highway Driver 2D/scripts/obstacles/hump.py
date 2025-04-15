from pygame import *
from random import *

init()

class Hump:
    # load the images 
    hump = image.load("../assets/hump.png")
    humpSymbol = image.load("../assets/humpSymbol.png")
    # create customisable variable playerVehicle
    playerVehicle = None

    def __init__(self,x,y):
        # init the pos 
        self.x = x
        self.y = y
        # collision rect
        self.initCollisionRect()
    
    def initCollisionRect(self): self.collisionRect = Rect(self.x,self.y,250,25)

    def checkCollision(self):
        # if normal collision
        if self.collisionRect.colliderect(self.playerVehicle.collisionRect) and self.playerVehicle.speed > 4.5: return True
        return False

    def display(self,s):
        # update the y acc. to speed
        self.y += self.playerVehicle.speed
        # update the collision rect
        self.initCollisionRect()
        # display the objects 
        s.blit(self.hump,(self.x,self.y))
        # move the symbol w/ offset of (-10,3000 (fn))
        s.blit(self.humpSymbol,(self.x-75,self.y+3000))
        # reset to a random coord if it exceeds a certain limit
        if self.y > 1500: self.y = -randint(36000,72000)
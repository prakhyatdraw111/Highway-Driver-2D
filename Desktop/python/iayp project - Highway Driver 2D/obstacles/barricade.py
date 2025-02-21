from pygame import *
from random import randint

class Barricade: 
    # load img
    img = image.load("assets/barricade.png")
    commentImg = image.load("assets/barricadeComment.png")
    # load customisable playerVehicle
    speed = 0
    
    def __init__(self,x,y):
        # init coords
        self.x = x
        self.y = y
        # create rectangle for collision
        self.rect = Rect(self.x,self.y,50,50)

    def checkCollision(self,playerVehicle):
        # check
        if self.rect.colliderect(playerVehicle.collisionRect): return True
        return False
    
    def display(self,s): 
        # display the image
        s.blit(self.img,(self.x,self.y))
        # move the image
        self.y += self.speed
        self.rect.bottom += self.speed
        # warn the player early
        self.warnEarly(s)
        # check if it reaches the limit
        if self.y > 1000: 
            # create a random coord
            randY = -randint(108000,180000)
            self.y = randY # update object's y
            self.rect.bottom = randY # update rect's y

    def warnEarly(self,s):
        Time = 2
        displacement = 90
        # check if it reaches specific y value
        if self.y > -(self.speed*Time*displacement): 
            # show the comment
            s.blit(self.commentImg,(390,0))
            s.blit(self.img,(415,225))
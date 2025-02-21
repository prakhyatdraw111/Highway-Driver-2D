from pygame import *
from random import randint,choice

class Vehicle:
    # blank image
    blankImage = "assets/blank.png"
    # invincibility time
    invincibilityTime = 0

    def __init__(self,x,y,speed,texture):
        # gathering x and y to display it
        self.x = x
        self.y = y
        # creating the speed variable
        self.speed = speed
        # loading the vehicle image and texture
        self.texture = texture
        self.image = image.load(self.texture)
        # this is required so that accidents can happen in the game
        self.collisionRect = Rect(self.x,self.y,50,110)

    def getSpeed(self): return self.speed

    def setSpeed(self,value): self.speed = value

    def moveCollisionRectAndX(self,value):
        self.x = value
        self.collisionRect.x = value

    def moveVehicle(self):
        # initialise
        kPress = key.get_pressed()
        # check
        if (kPress[K_LEFT] or kPress[K_a]) and self.x >= 440: self.moveCollisionRectAndX(self.x-1)
        elif (kPress[K_RIGHT] or kPress[K_d]) and self.x+50 <= 640: self.moveCollisionRectAndX(self.x+1)

    def checkEdges(self):
        # if x > 640 or x < 440
        if self.x+50 > 640 or self.x < 440: return True
        return False
    
    def resetCoords(self): self.moveCollisionRectAndX(465)
    
    def reduceInvincibility(self): 
        if self.invincibilityTime > 0: self.invincibilityTime -= 1 # reduce invincibilityTime
        
        # display blank img if the IT is b/w the given time frames
        if (self.invincibilityTime < 180 and self.invincibilityTime > 150) or (self.invincibilityTime < 120 and self.invincibilityTime > 90) or (self.invincibilityTime < 60 and self.invincibilityTime > 30): self.image = image.load(self.blankImage)
        else: self.image = image.load(self.texture)
    
    def restoreInvincibilty(self): self.invincibilityTime = 180 # restore invincibility

    def display(self,s): s.blit(self.image,(self.x,self.y)) # displaying the image

class VehicleList(list):
    def checkAndReturnSpeed(self,playerVehicle,vehicle): return (vehicle.speed - playerVehicle.speed)

    def checkCollision(self,playerVehicle):
        # for loop all vehicles
        for vehicle in self:
            if vehicle.collisionRect.colliderect(playerVehicle.collisionRect): return True
        return False
    
    def display(self,s,playerVehicle):
        # adding vehicles by RNG
        if randint(1,900) == 1: self.append(Vehicle(choice((465,565)),
                                                    -100,playerVehicle.speed+randint(0,5)/10 if playerVehicle.speed < 12 else randint(7,12),
                                                    f"assets/car {randint(1,4)}.png"))
        # display and change the speed of all the vehicles
        for i in self:
            speedDiff = playerVehicle.speed-i.speed # defining difference in speed to use down
            i.y += speedDiff
            i.collisionRect.y += speedDiff
            # display
            i.display(s)
            # check if reached farthest
            if i.y > 1000: self.remove(i)

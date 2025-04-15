from pygame import *
from random import randint
from numpy import array
from statistics import mean
init()

class SpeedSign: 

    speedNo = font.Font("../assets/font.ttf",20).render("60",True,(0,0,0))

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def draw(self,s,upsideDownEnabled):
        "draw the shapes"

        textOffset = array((self.speedNo.get_width() / 2, self.speedNo.get_height() / 2))

        if not upsideDownEnabled:
            # create centre of circle
            circleCentre = array((self.x,self.y+20))

            # draw red and then white circle
            draw.circle(s,(255,0,0), circleCentre, 20)
            draw.circle(s,(255,255,255), circleCentre, 15)

            # draw the pole which supports it
            draw.line(s, (0,0,0), (self.x, self.y + 40), (self.x, self.y + 140), 5)

            # draw the text
            s.blit(self.speedNo, circleCentre - textOffset)

        # do the same but reverse
        else: 
            circleCentre = array((self.x, self.y+120))

            draw.line(s, (0,0,0), (self.x, self.y), (self.x, self.y+100), 5)

            draw.circle(s, (255,0,0), circleCentre, 20)
            draw.circle(s, (255,255,255), circleCentre, 15)

            rotatedText = transform.rotate(self.speedNo, 180)
            s.blit(rotatedText, circleCentre - textOffset)
            

    def display(self,s,speed,upsideDownEnabled=False):
        # move the y
        self.y += speed

        # draw the diagram
        self.draw(s, upsideDownEnabled)

        # check if it has gone far
        if self.y > 1200: self.y = -randint(12000, 30000)


class SpeedGun:
    img = image.load("../assets/policeCar.png")

    stop = False
    payScreenEnabled = False
    ftsEnabled = False
    utpEnabled = False

    clickCooldown = 180
    unableToPayCooldown = 180
    ftsCooldown = 180

    stopText = font.Font("../assets/font.ttf",16).render("STOP!",True,(255,255,255))
    clickAnywhereText = font.Font("../assets/font.ttf",48).render("Click anywhere to pay",True,(255,0,0))
    noMoneyText = font.Font("../assets/font.ttf",48).render("Not enough money!",True,(255,0,0))
    failedToStopText = font.Font("../assets/font.ttf",48).render("Failed to stop on time!",True,(255,0,0))   

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def display(self,s,playerVehicle):
        # display the image
        s.blit(self.img,(self.x,self.y))

        # move it acc. speed 
        self.y += playerVehicle.speed

        # check if speed gun is gone
        if self.y > 2100: self.y = -randint(18000*round(playerVehicle.speed), 36000*round(playerVehicle.speed))  

    def interpret(self,s,playerVehicle,stopLineX,stopLineXEnd,sapphireHandler):
        global ransom,firstSpeed
        # check if player speed is high
        if playerVehicle.speed > 10 and round(self.y+110) > 0 and round(self.y+110) <= 20:
            firstSpeed = playerVehicle.speed 
            self.stop = True

        # do things if stop = true
        if self.stop: 
            draw.line(s,(255,255,255),(stopLineX,self.y+55),(stopLineXEnd,self.y+55),10)
            s.blit(self.stopText,(mean((stopLineX,stopLineXEnd))-self.stopText.get_width()/2, self.y+25-self.stopText.get_height()/2))
            
            # check if speed = 0 when vehicle y > vehicleY>y+500
            if playerVehicle.speed > 0 and self.y > 2000: self.ftsEnabled = True
            
            # check if playerVehicle.speed = 0
            elif playerVehicle.speed < 0:
                ransom = round(firstSpeed*5) 
                self.payScreenEnabled = True

            if self.payScreenEnabled:
                # ransom render
                ransomRender = font.Font("../assets/font.ttf",32).render(str(ransom),True,(255,0,0))
                
                if not self.utpEnabled:
                    # display all text and sapphire next to ransom render
                    s.blit(self.clickAnywhereText,(640-self.clickAnywhereText.get_width()/2, 540-self.clickAnywhereText.get_height()/2))
                    s.blit(ransomRender,(665-ransomRender.get_width()/2,360-ransomRender.get_height()/2))
                    s.blit(sapphireHandler.sapphireImg,(615-ransomRender.get_width()/2,335))

                self.clickCooldown -= 1

                # check if anywhere is pressed, provided that there is some cooldown
                if self.clickCooldown <= 0:
                    if not self.utpEnabled:
                        for evnt in event.get():
                            if evnt.type == MOUSEBUTTONUP:
                                if sapphireHandler.sapphiresCollected-ransom < 0:  self.utpEnabled = True
                                
                                else: 
                                    sapphireHandler.sapphiresCollected -= ransom
                                    # reset everything
                                    self.stop = False
                                    self.payScreenEnabled = False
                    
                    else:
                        s.blit(self.noMoneyText,(640-self.noMoneyText.get_width()/2,360-self.noMoneyText.get_height()/2))
                                
                        self.unableToPayCooldown -= 1  
                        if self.unableToPayCooldown < 0: return -1

            elif self.ftsEnabled:
                s.blit(self.failedToStopText,(640-self.failedToStopText.get_width()/2,360-self.failedToStopText.get_height()/2))
                
                self.ftsCooldown -= 1
                if self.ftsCooldown == 0: 
                    self.ftsCooldown = 180
                    return -1


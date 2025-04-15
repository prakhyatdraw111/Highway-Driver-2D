from pygame import *
from numpy import array
init()

class Speedometer:
    # load images
    speedometerImg = image.load("../assets/speedometer.png")
    needleImg = image.load("../assets/needle.png")
    activeImg = needleImg
    differenceList = [0]
    
    def __init__(self,pos): self.pos = array(pos)

    def display(self,s):
        # display both imgs 
        s.blit(self.speedometerImg,self.pos)
        s.blit(self.activeImg,self.pos) # offset due to small size

    def turn(self,speed):
        # turn the image
        self.activeImg = transform.rotate(self.needleImg,-speed)
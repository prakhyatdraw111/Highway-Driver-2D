from pygame import *

class BrakePedal:
    pedalImg = image.load("../assets/brake pedal.png")

    def __init__(self,pos): self.pos = pos

    def display(self,s): s.blit(self.pedalImg,self.pos)

    def clickAction(self,speed):
        mousePressed = mouse.get_pressed()[0]
        keyPressed = key.get_pressed()
        mousePos = mouse.get_pos()

        if (mousePressed and mousePos[0] > self.pos[0] and mousePos[0] < self.pos[0]+100 and mousePos[1] > self.pos[1] and mousePos[1] < self.pos[1]+162) or keyPressed[K_DOWN] or keyPressed[K_s]:
            return speed-(1/15) if speed > 0 else 0
        
        return speed
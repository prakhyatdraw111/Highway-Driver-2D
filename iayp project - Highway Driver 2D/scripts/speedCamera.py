from pygame import draw, init, display, time, event, QUIT, quit, font
from math import radians, tan
from random import randint

init()

class SpeedCamera:
    "shows the speed of the vehicle and other vehicles"
    Font = font.Font("../assets/font.ttf", 15)

    def __init__(self,x,y,finalX):
        self.x = x
        self.y = y 
        self.finalX = finalX

    def draw(self, s, playerVehicle):
        "draws the object"
        # creating xOffset so that it's reused
        xOff = self.x + (75 * tan(radians(30)) / 3)
        finalxOff = self.finalX + (75 * tan(radians(30)) / 3)

        # drawing the support poles
        draw.line(s, (0,0,0), (self.x, self.y), (xOff, self.y-75), 5)
        draw.line(s, (0,0,0), (self.finalX, self.y), (finalxOff, self.y-75), 5)
        draw.line(s, (0,0,0), (finalxOff, self.y-75), (xOff, self.y-75), 5)

        # drawing the speedometer
        topPoleLength = int(round(finalxOff-xOff))
        
        for x in range(50, topPoleLength, 100): # x is the position offset for the hangers
            draw.line(s, (0,0,0), (xOff + x, self.y-75), (xOff + x, self.y-65), 5) # drawing the support
            draw.rect(s, (0,0,0), (xOff + x - 20, self.y-65, 40, 20))

            # create the text render (where if speed is above 60 in speedometer show red else green)
            speedRender = self.Font.render(str(int(playerVehicle.speed * 6)), True, (0, 150, 5) if playerVehicle.speed * 6 < 60 else (255, 0, 0))

            # display the speed render
            s.blit(speedRender, (xOff + x - speedRender.get_width() / 2, self.y - 55 - speedRender.get_height() / 2))

    def display(self,s, playerVehicle):
        "the main function for this"

        self.y += playerVehicle.speed 

        self.draw(s, playerVehicle)

        if self.y > 1500: self.y = -randint(72000, 180000)

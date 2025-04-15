from pygame import init, image, Rect, surface, draw
from vehicle import Vehicle
from random import randint

GHOSTLENGTH = 50

BARLENGTH = 300
BARHEIGHT = 50

BAROFFSET = 10

init()

ghostImg = image.load("../assets/ghost.png")

class ShowInvincibilityDuration: 
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def display(self, s: surface, invincibilityTime: int):
        s.blit(ghostImg, (self.x, self.y))

        draw.rect(s, (0, 0, 0), (self.x + GHOSTLENGTH, self.y, BARLENGTH, BARHEIGHT))
        draw.rect(s, (255, 255, 255), (self.x + BAROFFSET + GHOSTLENGTH, self.y + BAROFFSET, (invincibilityTime / 3) - 2 * BAROFFSET, BARHEIGHT - 2 * BAROFFSET))


class Ghost:
    barClass = None

    ghostStatusActivated = False

    def __init__(self, x: int, y: int):
        # init pos
        self.x = x
        self.y = y

        # the rectangle
        self.rect = Rect(self.x, self.y, GHOSTLENGTH, GHOSTLENGTH)

        # to show the duration of invincibility
        self.showInvincibilityDurationBar = ShowInvincibilityDuration(0, 0) 

    def display(self, s: surface, playerVehicle: Vehicle):
        # display the image
        s.blit(ghostImg, (self.x, self.y))

        # reduce y by playervehicle speed
        self.y += playerVehicle.speed
        self.rect.top += playerVehicle.speed

        # check if it goes beyond a point
        if self.y > 1000: self.y = -randint(216000, 532000)

        # check if ghost status is activated
        if self.ghostStatusActivated:
            playerVehicle.reduceInvincibility()

            self.showInvincibilityDurationBar.display(s, playerVehicle.invincibilityTime)

            # change the image of the player vehicle to make it look like a ghost
            playerVehicle.image = image.load("../assets/playerVehicleGhost.png")

            # when the time is up the status is deactivated 
            if playerVehicle.invincibilityTime == 0: 
                self.ghostStatusActivated = False

                # change the image of the player vehicle to make it look normal
                playerVehicle.image = image.load("../assets/player car.png")


    def checkCollision(self, s: surface, playerVehicle: Vehicle):

        if self.rect.colliderect(playerVehicle.collisionRect):
            # activate the ghost status
            self.ghostStatusActivated = True

            # set invincibility to 15 seconds -> 900 ticks
            playerVehicle.invincibilityTime = 900

            # reset its pos
            self.y = -randint(216000, 532000)
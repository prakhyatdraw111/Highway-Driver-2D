from pygame import event, display, init, time, QUIT, KEYDOWN, K_d, quit, font, draw, image, mouse
from background import drawBg
from vehicle import *
from colours import BLACK
from whitelines import *
from speedometer import *
from brakePedal import *
from obstacles.barricade import *
from obstacles.hump import *
from life import Life
from sapphire import *
from random import randint
import sys
init()

s = display.set_mode((1280,720)) # creating the window screen
c = time.Clock() # creating so that the game runs @ 60 fps

# boolean conditions
gameStarted = False
gameHalt = False
gameOver = False
moneyBagOpening = False

# images
startButton = image.load("assets/start button.png")

# creating the player's vehicle
playerVehicle = Vehicle(465,305,0,"assets/player car.png")

# creating the other vehicles
vehicleList = VehicleList()

# barricade
barricade = Barricade(465,-10000)

# speed breaker
hump = Hump(440,-1000)

# the greatest white lines
whiteLines = WhiteLines()

# speedometer & speed
speedometer = Speedometer((0,520))
speed = 0

# brake pedal
brakePedal = BrakePedal((300,550))

# lives
life = Life()

# sapphire related
sapphireHandler = SapphireHandler() # sapphire handler
moneyBag = MoneyBag(randint(465,565),-3000,(465,565)) # money bag

# misc
gameOverScreen = image.load("assets/goScreen.png")

# acceleration feature
def accelerate():
    global speed
    
    speed += 1/120 if speed <= 10 else 1/360

# function to display start button and accelerate
def beforeGame():
    global gameStarted
    # display the start button
    s.blit(startButton,(490,306))

    # check if mouse is clicked in the start button
    mousePos = mouse.get_pos()
    condition1 = mouse.get_pressed()[0]
    condition2 = mousePos[0] > 490 and mousePos[1] > 306 and mousePos[0] < 790 and mousePos[1] < 414

    if condition1 and condition2: gameStarted = True

x = 0
while 1:
    c.tick(120) # run the game @ 60 fps
    for i in event.get():
        if i.type == QUIT:
            quit()
            sys.exit(1)

    # game start/end
    if not moneyBagOpening:
        # draw background
        drawBg(s)

        # before game if game hasn't started and no life was lost
        if not gameStarted and not gameHalt and not gameOver: beforeGame()

        # if game has started but a life was lost
        elif gameStarted and gameHalt and not gameOver: 
            time.delay(1000) # pause the game for a sec
            playerVehicle.restoreInvincibilty() # restore the invincibility
            playerVehicle.resetCoords() # reset x
            gameHalt = False # resume the game 

        # otherwise
        elif gameStarted and not gameHalt and not gameOver: 
            # increase speed
            accelerate()

            # player vehicle thingamajigs
            playerVehicle.setSpeed(speed) # set speed
            playerVehicle.reduceInvincibility() # reduce invincibility
            playerVehicle.moveVehicle() # move the vehicle

            speedometer.turn(speed*10)

            for _ in range(int(round(speed*.5))): whiteLines.doInterchange()
         
            # set speed of the vehicle list
            vehicleList.display(s,playerVehicle)

            # -------moving the obstacles-------

            # move the barricade
            barricade.speed = speed

            # move the speed breaker
            hump.playerVehicle = playerVehicle
            hump.display(s)

            # sapphire handler things
            sapphireHandler.displayAndMove(s,playerVehicle) # move the sapphires
            sapphireHandler.generateSomeRandomSapphires() # randomly generate sapphires
            sapphireHandler.displaySapphiresCollected(s,1130,50) # show no. coins generated

            # display money bags
            moneyBag.display(s) # display
            moneyBag.moveAndCheckCollision(playerVehicle) # move 
            
            # ----------------------------------

            # brake pedal functions
            speed = brakePedal.clickAction(speed)

            # check if vehicle is collided and there isn't invincibility
            if playerVehicle.invincibilityTime == 0 and ( vehicleList.checkCollision(playerVehicle) or barricade.checkCollision(playerVehicle) or hump.checkCollision() or playerVehicle.checkEdges() ): 
                life.lives -= 1 # lose a life 
                gameHalt = True # pause the game

            # or -> if any one is true, 1 life -

        elif gameOver: 
            s.blit(gameOverScreen,(160,90)) # display game over screen

        # display required items 

        # display the player vehicle (required otherwise black bg)
        whiteLines.display(s) 
        playerVehicle.display(s)
        
        barricade.display(s)

        # speedometer only display no function
        speedometer.display(s)

        # break pedal only display
        brakePedal.display(s)

        # display life
        life.display(s)

        # start moneybag opening if it is gameOver
        if life.lives == 0: moneyBagOpening = True

    # if it is moneybag opening
    else: 
        if moneyBag.opening(s,sapphireHandler): 
            moneyBagOpening = False
            gameOver = True

    display.update()

from pygame import event, display, init, time, QUIT, KEYDOWN, K_d, quit, font, draw, image, mouse

from background import drawBg
from vehicle import *
from colours import BLACK
from whitelines import *
from speedometer import *
from brakePedal import *

from obstacles.barricade import *
from obstacles.hump import *
from obstacles.speedgun import *

from powerups.ghost import Ghost

from speedCamera import *
from life import Life
from sapphire import *
from random import randint
import sys


init()

s = display.set_mode((1280,720)) # creating the window screen
c = time.Clock() # creating so that the game runs @ 60 fps

# load font
Font = font.Font("../assets/font.ttf",32)

# images
startButton = image.load("../assets/start button.png")
gameOverScreen = image.load("../assets/goScreen.png")
sapphireImg = image.load("../assets/sapphire.png")
mmImg = image.load("../assets/startmenu.png")

randomX = (465,565)

# main menu boolean
mainMenu = True

def reset(): 
    global gameStarted, gameHalt, gameOver, moneyBagOpening, playerVehicle, vehicleList, barricade, barricade2, hump, speedGun, speedWarning, speedWarningOpp, speedCamera, whiteLines, speedometer, speed, brakePedal, life, sapphireHandler, moneyBag, ghost
    # boolean conditions
    gameStarted = False
    gameHalt = False
    gameOver = False
    moneyBagOpening = False
    
    # creating the player's vehicle
    playerVehicle = Vehicle(465,305,0,"../assets/player car.png")

    # creating the other vehicles
    vehicleList = VehicleList()

    # barricade
    barricadeY = -randint(60000,120000)
    barricade = Barricade(choice((465,565)),barricadeY)
    barricade2 = Barricade(choice((465,565)),barricadeY-200) 

    # speed breaker
    hump = Hump(440,-1000)

    # speed gun
    speedGun = SpeedGun(250,-15000)
    speedWarning = SpeedSign(365,-1000)
    speedWarningOpp = SpeedSign(915,-1000)

    # speed camera 
    speedCamera = SpeedCamera(440, -10000, 640)

    # ------- powerups ------

    ghost = Ghost(choice((465, 565)), -randint(10000, 50000))

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
    moneyBag = MoneyBag(randint(465,565),-randint(108000,216000),(465,565)) # money bag

# initialise everything
reset()

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

    mousePos = mouse.get_pos()
    mousePressed = mouse.get_pressed()[0]
    
    if mainMenu: 
        # frontend
        s.fill((0,0,0))
        s.blit(mmImg,(0,0))
        # game condns
        if mousePressed and mousePos[1] > 540 and mousePos[1] < 630:
            if mousePos[0] > 265 and mousePos[0] < 355 : 
                reset()
                mainMenu = False

            if mousePos[0] > 920 and mousePos[0] < 1010:
                quit()
                sys.exit(1) 

    else: 
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
                if not speedGun.payScreenEnabled: accelerate()

                # player vehicle thingamajigs
                playerVehicle.setSpeed(speed) # set speed
                playerVehicle.reduceInvincibility() # reduce invincibility
                playerVehicle.moveVehicle() # move the vehicle

                speedometer.turn(speed*10)

                for _ in range(int(round(speed*.5))): whiteLines.doInterchange()
            
                # set speed of the vehicle list
                vehicleList.display(s,playerVehicle)

                # -------moving the obstacles-------

                # move the barricade and interpret the other
                barricade.speed = speed
                barricade2.speed = speed

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

                # display the speed camera 
                speedCamera.display(s, playerVehicle)
                
                # ------- moving powerups --------

                # ghost
                ghost.display(s, playerVehicle)
                ghost.checkCollision(s, playerVehicle)

                # --------------------------------

                # brake pedal functions
                speed = brakePedal.clickAction(speed)

                # check if vehicle is collided and there isn't invincibility
                if playerVehicle.invincibilityTime == 0 and ( vehicleList.checkCollision(playerVehicle) or barricade.checkCollision(playerVehicle) or barricade2.checkCollision(playerVehicle) or hump.checkCollision() or playerVehicle.checkEdges() ): 
                    life.lives -= 1 # lose a life 
                    gameHalt = True # pause the game

                # or -> if any one is true, 1 life -

            # display required items 
            #print(round(playerVehicle.speed))

            # display the player vehicle (required otherwise black bg)
            whiteLines.display(s) 
            playerVehicle.display(s)

            # display both barricades and interpret the other                        
            barricade.display(s)
            barricade2.display(s)

            barricade.interpret(randomX)

            if barricade2.y > 1000: 
                barricade2.y = barricade.y-350
                barricade2.rect.top = barricade.y-350

            # display the speed gun and speed warning
            speedWarning.display(s, speed)
            speedWarningOpp.display(s, speed, True)
            speedGun.display(s,playerVehicle)
            if speedGun.interpret(s,playerVehicle,325,635,sapphireHandler) == -1: moneyBagOpening = True
            
            # speedometer only display no function
            speedometer.display(s)

            # break pedal only display
            brakePedal.display(s)

            # display life
            life.display(s)

            # start moneybag opening if it is gameOver
            if life.lives == 0: moneyBagOpening = True

            if gameOver:  
                # initialise mouse
                mousePressed = mouse.get_pressed()[0]
                mousePos = mouse.get_pos()
                
                # reset speed
                speed = 0
                speedometer.turn(0)
                s.blit(gameOverScreen,(160,90)) # display game over screen

                # display sapphire
                coinsText = Font.render(str(sapphireHandler.sapphiresCollected),True,(0,0,0))
                s.blit(coinsText,(400-coinsText.get_width()/2,450-coinsText.get_height()/2))
                s.blit(sapphireImg,(240,425))
                
                # check if any button is pressed
                if mousePressed and mousePos[0] > 840 and mousePos[0] < 1010:
                    if mousePos[1] > 275 and mousePos[1] < 325: reset()
                    elif mousePos[1] > 390 and mousePos[1] < 445: mainMenu = True

        # if it is money bag opening
        else: 
            if moneyBag.opening(s,sapphireHandler): 
                moneyBagOpening = False
                gameOver = True

    display.update()

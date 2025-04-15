from pygame import *
from random import *

init()

class Sapphire:
    # load img of it 
    img = image.load("../assets/sapphire.png")

    def __init__(self,x,y):
        # initialise pos
        self.x = x
        self.y = y
        # create rect
        self.rect = Rect(self.x,self.y,50,50)

    def checkCollision(self,playerVehicle): 
        if self.rect.colliderect(playerVehicle.collisionRect): # check if playerVehicle is collided
            return True
        return False 

    def display(self,s,speed):
        # display image
        s.blit(self.img,(self.x,self.y))
        # move both the rect and the img
        self.y += speed
        self.rect.y += speed

class SapphireHandler:
    sapphireList = [Sapphire(465,-300),Sapphire(465,-350),Sapphire(465,-400),Sapphire(465,-450),Sapphire(465,-500)] # list where the sapphires are generated
    sapphiresCollected = 0 # track how many sapphires the player collected
    generationPatterns = ( # how the sapphires are generated
        (465,465,465,465,465),
        (565,565,565,565,565),
        (465,465,465,485,505,525,545,565,565,565),
        (565,565,565,545,525,505,485,465,465,465))
    
    # load sapphire img and font
    sapphireImg = image.load("../assets/sapphire.png")
    fnt = font.Font("../assets/font.ttf",40)
    
    def generateSomeRandomSapphires(self):
        # generate some random no.
        randomNo = randint(0,1800)
        # generate if randint is < 5
        if randomNo < 4: 
            for x,y in zip(self.generationPatterns[randomNo],(-840,-890,-940,-990,-1040,-1090,-1140,-1190,-1240)): self.sapphireList.append(Sapphire(x,y))

    def displayAndMove(self,s,playerVehicle):
        for sapphire in self.sapphireList: 
            sapphire.display(s,playerVehicle.speed) # display and move it
            if sapphire.checkCollision(playerVehicle): # check if it is collided
                self.sapphiresCollected += 1 # add one point
                self.sapphireList.remove(sapphire) # remove this list
    
    def displaySapphiresCollected(self,s,x,y):
        # display sapphire object instead of text
        s.blit(self.sapphireImg,(x,y))
        # create and display render object of text
        sapphireRender = self.fnt.render(str(self.sapphiresCollected),True,(0,0,0))
        s.blit(sapphireRender,(x+100-sapphireRender.get_width()/2, y+25-self.fnt.get_height()/2))

class MoneyBag:
    # collection counter
    counter = 0
    # text
    fnt = font.Font("../assets/font.ttf",40)
    clickAsap = fnt.render("Click here as fast as possible!",True,(255,255,255))
    # scene
    scene = 0
    # clicks and time
    clicks = 1
    initTime = 0
    finalTime = 0
    # size of large mb
    incSize = 300
    # no. coins
    coins = randint(30,100)

    def __init__(self,x,y,xGap):
        self.x = x
        self.y = y 
        self.xGap = xGap
        self.img = image.load("../assets/moneyBag.png")
        self.openingReset()
        self.rect = Rect(self.x,self.y,50,50)

    def openingReset(self):
        # scene
        self.scene = 0
        # clicks and time
        self.clicks = 1
        self.initTime = 0
        self.finalTime = 0
        # size of large mb
        self.incSize = 300
        # no. coins
        self.coins = randint(30,100) 

    def opening(self,s,sapphireHandler): 
        # initialise mouse 
        mousePressed = mouse.get_pressed()[0]
        # only if counter > 0
        if self.counter:
            # fill w/ bg
            s.fill((0,0,0))
            
            # display box if scene is not displaying no. coins
            if self.scene != 2:
                self.scaledImg = transform.scale(self.img,(self.incSize,self.incSize)) # real time scaling
                s.blit(self.scaledImg,(640-self.incSize/2,360-self.incSize/2))

            # check the scene
            if self.scene == 0: 
                # display frontend
                s.blit(self.clickAsap,(640-self.clickAsap.get_width()/2,540-self.fnt.get_height()/2))
                # check if clicked
                if mousePressed: 
                    # change scene
                    self.scene = 1
                    # set initial and final time
                    self.initTime = time.get_ticks()
                    self.finalTime = self.initTime + randint(3000,6000)

            if self.scene == 1: 
                # check if clicked before final time
                if time.get_ticks() < self.finalTime: 
                    for evnt in event.get(): 
                        if evnt.type == QUIT: quit(); exit()
                        if evnt.type == MOUSEBUTTONUP: 
                            self.clicks += 1
                            for _ in range(10): self.incSize += 1
                else: 
                    # calcluate the no. coins on basis of clicks
                    self.coins += self.clicks*2
                    self.scene = 2

            if self.scene == 2:
                # make render for text and display frontend
                coinsRender = self.fnt.render(f"{self.coins} coins!",True,(255,255,255))
                ctcText = self.fnt.render("Click anywhere to continue",True,(255,255,255))
                s.blit(coinsRender,(640-coinsRender.get_width()/2,360-self.fnt.get_height()/2))
                s.blit(ctcText,(640-ctcText.get_width()/2,540-self.fnt.get_height()/2))
                # check click
                if mousePressed: 
                    # -counter, reset, add to total sapphires
                    self.counter -= 1
                    sapphireHandler.sapphiresCollected += self.coins
                    self.openingReset()

        else: return True


    def moveXandY(self,pos): 
        # move money bag
        self.x = pos[0]
        self.y = pos[1]
        # move collision rect
        self.rect.topleft = pos

    def moveAndCheckCollision(self,playerVehicle):
        # move the bag
        self.moveXandY((self.x,self.y+playerVehicle.speed))
        # add one counter if it's collided
        if playerVehicle.collisionRect.colliderect(self.rect): self.counter += 1
        # reset x and y if y < 1300 or object is collided
        if playerVehicle.collisionRect.colliderect(self.rect) or self.y > 1300: self.moveXandY((randint(self.xGap[0],self.xGap[1]),-randint(108000,216000)))

    def display(self,s):
        # display collision rect
        draw.rect(s,(255,255,255),self.rect)
        # display money bag
        s.blit(self.img,(self.x,self.y))

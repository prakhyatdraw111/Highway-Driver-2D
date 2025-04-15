from pygame import *

class Life: 
    # lives 
    lives = 3
    
    def display(self,s): 
        # display imgs acc. to lives
        s.blit(image.load(f"../assets/lives/{self.lives}.png"),(1130,0))
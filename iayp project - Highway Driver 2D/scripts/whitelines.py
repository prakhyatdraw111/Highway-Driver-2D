from pygame import draw,init
init()

class WhiteLines:
    interchange = iter(range(18))
    def __init__(self): self.whiteLines = [x for x in range(18,720,78)] # y values for white lines

    def doInterchange(self):
        try: self.whiteLines = [x for x in range(next(self.interchange)*2,720,78)]
        except StopIteration: self.interchange = iter(range(18))

    def display(self,s):
        # updating the list after speed 
        for y in self.whiteLines:
            draw.line(s,(255,255,255),(540,y),(540,y+60),5)
            draw.line(s,(255,255,255),(740,y),(740,y+60),5)
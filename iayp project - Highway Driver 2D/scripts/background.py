from pygame import draw
from colours import BLACK,WHITE

def drawBg(s):
    # drawing grass
    s.fill((76,187,23))
    # drawing the road
    draw.rect(s,(87,77,77),(440,0,400,720))
    # drawing the border lines
    draw.line(s,BLACK,(440,0),(440,720),5)
    draw.line(s,BLACK,(840,0),(840,720),5)
    draw.line(s,BLACK,(640,0),(640,720),5)
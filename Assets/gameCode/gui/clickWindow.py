"""
    sets the click window function
"""
#imports
from Assets.gameCode.backend.vars import *
import pygame

#window function
def clickWindow(WIN: pygame.Surface, POS: tuple, l1: str, l2: str=""):
    # gets the x and y position
    x, y = POS

    rectangle = pygame.Rect(x, y, 100, 100)#makes a rectangle
    singleplayer_text = [defaultFont.render(l1, 1, (255, 255, 255)), 
        defaultFont.render(l2, 1, (255, 255, 255))]#renders the text

    pygame.draw.rect(WIN, (0, 0, 0), rectangle)#draws the rectangle
    WIN.blit(singleplayer_text[0], (x,y))#draws the text
    WIN.blit(singleplayer_text[1], (x,y+50))

    #if the box is clicked, return True
    if pygame.mouse.get_pressed()[0] and rectangle.collidepoint(pygame.mouse.get_pos()):
        return True
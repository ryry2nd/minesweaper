"""
defines the input letters class
"""
#imports
import pygame
from Assets.gameCode.backend.vars import *

#init
pygame.init()
pygame.font.init()

joinIp = '.'.join(IP.split('.')[0:3])+'.' # pulls local ip and removes last numbers

#defines the input letters class
class InputIp:
    #init
    def __init__(self):
        pass
    #places the text on the screen
    def placeText(self, WIN: pygame.Surface, RES: tuple):
        WIN.blit(defaultFont.render(joinIp, 1, (255, 255, 255)), RES)
    #gets the ip
    def get(self):
        return joinIp
    #adds a key
    def addkey(self, keys: int):
        global joinIp
        # if backspace is pressed remove the last number
        if keys == pygame.K_BACKSPACE and joinIp != []:
            joinIp = joinIp[0:len(joinIp)-1]
        else:
            #adds a number or period if it is pressed
            if keys == pygame.K_0:
                joinIp += "0"
            elif keys == pygame.K_1:
                joinIp += "1"
            elif keys == pygame.K_2:
                joinIp += "2"
            elif keys == pygame.K_3:
                joinIp += "3"
            elif keys == pygame.K_4:
                joinIp += "4"
            elif keys == pygame.K_5:
                ip += "5"
            elif keys == pygame.K_6:
                joinIp += "6"
            elif keys == pygame.K_7:
                joinIp += "7"
            elif keys == pygame.K_8:
                joinIp += "8"
            elif keys == pygame.K_9:
                joinIp += "9"
            elif keys == pygame.K_PERIOD:
                joinIp += "."
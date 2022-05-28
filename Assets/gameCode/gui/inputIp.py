"""
defines the input letters class
"""
#imports
import pygame
from Assets.gameCode.backend.vars import *

#init
pygame.init()
pygame.font.init()

ip = '.'.join(IP.split('.')[0:3])+'.' # pulls local ip and removes last numbers

#defines the input letters class
class InputIp:
    #init
    def __init__(self):
        pass
    #places the text on the screen
    def placeText(self, WIN: pygame.Surface, RES: tuple):
        WIN.blit(defaultFont.render(ip, 1, (255, 255, 255)), RES)
    #adds a key
    def addkey(self, keys: int):
        global ip
        # if backspace is pressed remove the last number
        if keys == pygame.K_BACKSPACE and ip != []:
            ip = ip[0:len(ip)-1]
        else:
            #adds a number or period if it is pressed
            if keys == pygame.K_0:
                ip += "0"
            elif keys == pygame.K_1:
                ip += "1"
            elif keys == pygame.K_2:
                ip += "2"
            elif keys == pygame.K_3:
                ip += "3"
            elif keys == pygame.K_4:
                ip += "4"
            elif keys == pygame.K_5:
                ip += "5"
            elif keys == pygame.K_6:
                ip += "6"
            elif keys == pygame.K_7:
                ip += "7"
            elif keys == pygame.K_8:
                ip += "8"
            elif keys == pygame.K_9:
                ip += "9"
            elif keys == pygame.K_PERIOD:
                ip += "."
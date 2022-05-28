"""
    inits images and fonts
"""
#imports
import pygame, json

#init
pygame.init()
pygame.font.init()

#init images
numberImgs = []
for i in range(9):
    numberImgs.append(pygame.image.load(f"Assets/textures/number{i}.png"))
flagImg = pygame.image.load("Assets/textures/flag.png")
hiddenImg = pygame.image.load("Assets/textures/hidden.png")
bombImg = pygame.image.load("Assets/textures/bomb.png")
explodedBombImg = pygame.image.load("Assets/textures/explodedBomb.png")
notABombImg = pygame.image.load("Assets/textures/notABomb.png")
resetImg = pygame.image.load("Assets/textures/reset.png")

#init font
defaultFont = pygame.font.SysFont("Arial", 25)

#init vars
with open("saves.json", 'r') as file:#get save file
    saves = json.load(file)#convert to json

SIZE = saves["size"]
BOARDSIZE = saves["boardSize"]
FPS = saves["fps"]
WIN = pygame.display.set_mode((SIZE, SIZE+50))# sets window

#sets what variables are to be sent when imported
__all__ = ["numberImgs", "flagImg", "hiddenImg", "bombImg", 
    "explodedBombImg", "notABombImg", "resetImg", "defaultFont",
    "SIZE", "BOARDSIZE", "FPS", "WIN"]
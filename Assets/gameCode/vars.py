import pygame

pygame.init()
pygame.font.init()

numberImgs = []
for i in range(9):
    numberImgs.append(pygame.image.load(f"Assets/textures/number{i}.png"))
flagImg = pygame.image.load("Assets/textures/flag.png")
hiddenImg = pygame.image.load("Assets/textures/hidden.png")
bombImg = pygame.image.load("Assets/textures/bomb.png")
explodedBombImg = pygame.image.load("Assets/textures/explodedBomb.png")
notABombImg = pygame.image.load("Assets/textures/notABomb.png")
resetImg = pygame.image.load("Assets/textures/reset.png")

defaultFont = pygame.font.SysFont("Arial", 25)

__all__ = ["numberImgs", "flagImg", "hiddenImg", "bombImg", "explodedBombImg", "notABombImg", "resetImg", "defaultFont"]
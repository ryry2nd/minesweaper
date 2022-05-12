from Assets.gameCode.objects import *
import pygame, sys

pygame.init()

RES = WIDTH, HEIGHT = 600, 700
BOARDSIZE = 10
AMOUNTBOMBS = 10
FPS = 60

WIN = pygame.display.set_mode(RES)
pygame.display.set_caption("Minesweeper")
pygame.display.set_icon(pygame.image.load("Assets/textures/bomb.png"))
board = Board(BOARDSIZE, RES, AMOUNTBOMBS)
clock = pygame.time.Clock()

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                board.lClick(pygame.mouse.get_pos())
            elif pygame.mouse.get_pressed()[2]:
                board.rClick(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                board.reset()
    WIN.fill((255, 255, 255))
    board.draw(WIN)
    pygame.display.update()
from Assets.gameCode.objects import *
import pygame, sys

pygame.init()

WIDTH, HEIGHT = 800, 800
FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")
board = Board((10, 10), (WIDTH, HEIGHT), 10)
clock = pygame.time.Clock()

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if pygame.mouse.get_pressed()[0]:
            board.keyPress(pygame.mouse.get_pos())
    board.draw(WIN)
    pygame.display.update()
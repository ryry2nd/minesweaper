import pygame, random

pygame.init()

numberImgs = []

for i in range(9):
    numberImgs.append(pygame.image.load(f"Assets/textures/number{i}.png"))

flagImg = pygame.image.load("Assets/textures/flag.png")

hiddenImg = pygame.image.load("Assets/textures/hidden.png")

bombImg = pygame.image.load("Assets/textures/bomb.png")

explodedBombImg = pygame.image.load("Assets/textures/explodedBomb.png")

notABombImg = pygame.image.load("Assets/textures/notABomb.png")

class TooManyBombs(Exception):
    pass

class Number:
    isHidden = True
    isFlaged = False
    isBomb = False
    num = None
    def __init__(self, rect: pygame.Rect) -> None:
        self.rect = rect

    def draw(self, WIN: pygame.surface) -> None:
        if not(self.isHidden) and self.isFlaged:
            WIN.blit(notABombImg, self.rect)
        elif self.isFlaged:
            WIN.blit(flagImg, self.rect)
        elif not self.isHidden:
            WIN.blit(numberImgs[self.num], self.rect)
        else:
            WIN.blit(hiddenImg, self.rect)

class Bomb:
    isHidden = True
    isFlaged = False
    isBomb = True
    isExploded = False
    def __init__(self, rect: pygame.Rect) -> None:
        self.rect = rect

    def draw(self, WIN: pygame.surface) -> None:
        if self.isExploded:
            WIN.blit(explodedBombImg, self.rect)
        elif self.isFlaged:
            WIN.blit(flagImg, self.rect)
        elif not self.isHidden:
            WIN.blit(bombImg, self.rect)
        else:
            WIN.blit(hiddenImg, self.rect)

class Board:
    def __init__(self, board_res: tuple, res: tuple, numBombs: int) -> None:
        global numberImgs, bombImg, hiddenImg, flagImg, explodedBombImg, notABombImg
        if numBombs > (board_res[0]*board_res[1]):
            raise TooManyBombs("There can't be more bombs than pieces")
        
        for i in range(9):
            numberImgs[i] = pygame.transform.scale(numberImgs[i], (res[1]/board_res[1], res[1]/board_res[1]))
        bombImg = pygame.transform.scale(bombImg, (res[1]/board_res[1], res[1]/board_res[1]))
        hiddenImg = pygame.transform.scale(hiddenImg, (res[1]/board_res[1], res[1]/board_res[1]))
        flagImg = pygame.transform.scale(flagImg, (res[1]/board_res[1], res[1]/board_res[1]))
        explodedBombImg = pygame.transform.scale(explodedBombImg, (res[1]/board_res[1], res[1]/board_res[1]))
        notABombImg = pygame.transform.scale(notABombImg, (res[1]/board_res[1], res[1]/board_res[1]))

        self.numBombs = numBombs
        self.WIDTH = res[0]
        self.HEIGHT = res[1]
        self.board = []
        self.board_res = board_res
        bombs = [[False for i in range(board_res[1])] for i in range(board_res[0])]
        
        for i in range(numBombs):
            while True:
                x = random.randint(0, board_res[0]-1)
                y = random.randint(0, board_res[1]-1)
                if not bombs[x][y]:
                    bombs[x][y] = True
                    break

        for x in range(board_res[0]):
            self.board.append([])
            for y in range(board_res[1]):
                if bombs[x][y]:
                    xPos = res[1]/board_res[1] * x
                    yPos = res[1]/board_res[1] * y
                    self.board[x].append(Bomb(pygame.Rect(xPos, yPos, res[1]/board_res[1], res[1]/board_res[1])))
                else:
                    xPos = res[1]/board_res[1] * x
                    yPos = res[1]/board_res[1] * y
                    self.board[x].append(Number(pygame.Rect(xPos, yPos, res[1]/board_res[1], res[1]/board_res[1])))

        for x in range(board_res[0]):
            for y in range(board_res[1]):
                if not self.board[x][y].isBomb:
                    self.board[x][y].num = self.getNumBombs(x, y)

    def showAll(self) -> None:
        for x in range(self.board_res[0]):
            for y in range(self.board_res[1]):
                self.board[x][y].isHidden = False

    def draw(self, WIN: pygame.surface) -> None:
        for x in self.board:
            for y in x:
                y.draw(WIN)
    
    def lClick(self, mousePos: tuple) -> None:
        for x in range(self.board_res[0]):
            for y in range(self.board_res[1]):
                if self.board[x][y].rect.collidepoint(mousePos) and not(self.board[x][y].isFlaged):
                    if self.board[x][y].isBomb:
                        self.showAll()
                        self.board[x][y].isExploded = True
                    else:
                        if self.board[x][y].isHidden:
                            self.board[x][y].isHidden = False
                        elif self.getNumFlags(x, y) >= self.getNumBombs(x, y):
                            self.selectArea(x, y)
                    return
    
    def rClick(self, mousePos: tuple) -> None:
        for x in range(self.board_res[0]):
            for y in range(self.board_res[1]):
                if self.board[x][y].rect.collidepoint(mousePos) and self.board[x][y].isHidden:
                    if self.board[x][y].isFlaged:
                        self.board[x][y].isFlaged = False
                    else:
                        self.board[x][y].isFlaged = True
                    return

    def getNumBombs(self, x: int, y: int) -> int:
        bombs = 0
        for x2 in range(-1,2):
            for y2 in range(-1,2):
                localX = x+x2
                localY = y+y2
                center = x2 == 0 and y2 == 0
                outY = localY >= self.board_res[1] or localY < 0
                outX = localX >= self.board_res[0] or localX < 0
                if not(center) and not(outX) and not(outY) and self.board[localX][localY].isBomb:
                    bombs+=1    
        return bombs
    
    def getNumFlags(self, x: int, y: int) -> int:
        flags = 0
        for x2 in range(-1,2):
            for y2 in range(-1,2):
                localX = x+x2
                localY = y+y2
                center = x2 == 0 and y2 == 0
                outY = localY >= self.board_res[1] or localY < 0
                outX = localX >= self.board_res[0] or localX < 0
                if not(center) and not(outX) and not(outY) and self.board[localX][localY].isFlaged:
                    flags += 1    
        return flags
    
    def selectArea(self, x: int, y: int):
        for x2 in range(-1, 2):
            for y2 in range(-1, 2):
                localX = x + x2
                localY = y + y2
                center = x2 == 0 and y2 == 0
                outY = localY >= self.board_res[1] or localY < 0
                outX = localX >= self.board_res[0] or localX < 0
                if not(center) and not(outX) and not(outY):
                    if self.board[localX][localY].isBomb:
                        self.showAll()
                        self.board[localX][localY].isExploded = True
                    else:
                        self.board[localX][localY].isHidden = False
                

    def reset(self) -> None:
        self.__init__(self.board_res, (self.WIDTH, self.HEIGHT), self.numBombs)
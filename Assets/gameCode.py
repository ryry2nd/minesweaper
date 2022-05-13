from turtle import width
import pygame, random, time

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

defaultFont = pygame.font.SysFont("Arial", 25)

class TooManyBombs(Exception):
    pass

def putTheNumberOn(WIN: pygame.surface, img: pygame.image, rect: pygame.Rect, size: int) -> None:
    scaledImg = pygame.transform.scale(img, (size, size))
    WIN.blit(scaledImg, rect)

class Number:
    isHidden = True
    isFlaged = False
    isBomb = False
    num = None
    def __init__(self, rect: pygame.Rect, squareSize: int) -> None:
        self.rect = rect
        self.squareSize = squareSize

    def draw(self, WIN: pygame.surface) -> None:
        if not(self.isHidden) and self.isFlaged:
            putTheNumberOn(WIN, notABombImg, self.rect, self.squareSize)
        elif self.isFlaged:
            putTheNumberOn(WIN, flagImg, self.rect, self.squareSize)
        elif not self.isHidden:
            putTheNumberOn(WIN, numberImgs[self.num], self.rect, self.squareSize)
        else:
            putTheNumberOn(WIN, hiddenImg, self.rect, self.squareSize)

class Bomb:
    isHidden = True
    isFlaged = False
    isBomb = True
    win = True
    isExploded = False
    def __init__(self, rect: pygame.Rect, squareSize: int) -> None:
        self.rect = rect
        self.squareSize = squareSize

    def draw(self, WIN: pygame.surface) -> None:
        if self.isExploded:
            putTheNumberOn(WIN, explodedBombImg, self.rect, self.squareSize)
        elif self.isFlaged:
            putTheNumberOn(WIN, flagImg, self.rect, self.squareSize)
        elif not self.isHidden:
            putTheNumberOn(WIN, bombImg, self.rect, self.squareSize)
        else:
            putTheNumberOn(WIN, hiddenImg, self.rect, self.squareSize)

class Board:
    def __init__(self, board_res: int, res: tuple, numBombs: int) -> None:
        global numberImgs, bombImg, hiddenImg, flagImg, explodedBombImg, notABombImg
        if numBombs > (board_res * board_res):
            raise TooManyBombs("There can't be more bombs than pieces")

        self.startTime = time.time()
        self.timeSoFar = 0
        self.headerHgt = 100
        self.isEnded = False
        self.numBombs = numBombs
        self.res = self.WIDTH, self.HEIGHT = res
        self.boardWidth = res[0]
        self.boardHeight = res[1] - self.headerHgt
        self.board_res = board_res
        self.squareSize = self.boardHeight/self.board_res
        self.board = [[Number(pygame.Rect(x*self.squareSize, y*self.squareSize + self.headerHgt, self.squareSize, self.squareSize), self.squareSize)
            for y in range(board_res)] for x in range(board_res)]
        
        for i in range(numBombs):
            while True:
                x = random.randint(0, board_res-1)
                y = random.randint(0, board_res-1)
                xPos = x*self.squareSize
                yPos = y*self.squareSize + self.headerHgt
                if not self.board[x][y].isBomb:
                    self.board[x][y] = Bomb(pygame.Rect(xPos, yPos, self.squareSize, self.squareSize), self.squareSize)
                    break

        for x in range(board_res):
            for y in range(board_res):
                square = self.board[x][y]
                if not square.isBomb:
                    square.num = self.getNumBombs(x, y)

    def showAll(self) -> None:
        for x in range(self.board_res):
            for y in range(self.board_res):
                self.board[x][y].isHidden = False
    
    def flagsLeft(self) -> int:
        numFlags = 0
        for i in self.board:
            for ii in i:
                if ii.isFlaged:
                    numFlags += 1
        
        return self.numBombs - numFlags

    def draw(self, WIN: pygame.surface) -> None:
        if not self.isEnded:
            self.timeSoFar = round(time.time() - self.startTime)
            
        second = self.timeSoFar % 60
        minute = (self.timeSoFar - second) // 60

        WIN.blit(defaultFont.render("Time Playing:", True, (0, 0, 0)), (0, 0))
        WIN.blit(defaultFont.render(f"{minute}:{second}", True, (0, 0, 0)), (0, 25))
        WIN.blit(defaultFont.render("Flags Left:", True, (0, 0, 0)), (self.WIDTH-100, 0))
        WIN.blit(defaultFont.render(str(self.flagsLeft()), True, (0, 0, 0)), (self.WIDTH-100, 25))
        for x in self.board:
            for y in x:
                y.draw(WIN)
    
    def lClick(self, mousePos: tuple) -> None:
        for x in range(self.board_res):
            for y in range(self.board_res):
                square = self.board[x][y]
                if square.rect.collidepoint(mousePos) and not(square.isFlaged) and not(self.isEnded):
                    if square.isBomb:
                        self.endGame()
                        square.isExploded = True
                        return
                    elif square.isHidden:
                        square.isHidden = False
                    elif self.getNumFlags(x, y) >= self.getNumBombs(x, y):
                        self.selectArea(x, y)
                    if square.num == 0:
                        self.selectArea(x, y)
                    self.checkWin()
                    return
    
    def rClick(self, mousePos: tuple) -> None:
        for x in range(self.board_res):
            for y in range(self.board_res):
                square = self.board[x][y]
                if square.rect.collidepoint(mousePos) and square.isHidden and not(self.isEnded) and (self.flagsLeft() or square.isFlaged):
                    square.isFlaged = not square.isFlaged
                    self.checkWin()
                    return

    def getNumBombs(self, x: int, y: int) -> int:
        bombs = 0
        for x2 in range(-1,2):
            for y2 in range(-1,2):
                localX = x+x2
                localY = y+y2
                center = x2 == 0 and y2 == 0
                outY = localY >= self.board_res or localY < 0
                outX = localX >= self.board_res or localX < 0
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
                outY = localY >= self.board_res or localY < 0
                outX = localX >= self.board_res or localX < 0
                if not(center) and not(outX) and not(outY) and self.board[localX][localY].isFlaged:
                    flags += 1    
        return flags

    emptiesToCheck = []

    def selectArea(self, x: int, y: int) -> None:
        self.emptiesToCheck.append([x,y])
        while self.emptiesToCheck:
            x, y = self.emptiesToCheck.pop()
            self.selectSingleArea(x, y)
        self.emptiesToCheck.clear()

    def selectSingleArea(self, x: int, y: int) -> None:
        for x2 in range(-1, 2):
            for y2 in range(-1, 2):
                localX = x + x2
                localY = y + y2
                center = x2 == 0 and y2 == 0
                outY = localY >= self.board_res or localY < 0
                outX = localX >= self.board_res or localX < 0
                if not(center) and not(outX) and not(outY):
                    square = self.board[localX][localY]
                    if square.isHidden and not square.isFlaged:
                        if square.isBomb:
                            self.endGame()
                            square.isExploded = True
                            return
                        square.isHidden = False
                        if square.num == 0:
                            xy=[localX,localY]
                            if xy not in self.emptiesToCheck:
                                self.emptiesToCheck.append(xy)

    def reset(self) -> None:
        self.__init__(self.board_res, self.res, self.numBombs)

    def checkAllBombs(self) -> bool:
        for i in self.board:
            for ii in i:
                if (ii.isBomb and not ii.isFlaged):
                    return False
        return True

    def checkAllNums(self) -> bool:
        for i in self.board:
            for ii in i:
                if (ii.isHidden and not ii.isBomb):
                    return False
        return True

    def checkWin(self) -> None:
        if not self.isEnded:
            if self.checkAllBombs() or self.checkAllNums():
                for i in self.board:
                    for ii in i:
                        if ii.isBomb:
                            ii.isFlaged = True
                self.endGame()

    def endGame(self) -> None:
        self.showAll()
        self.isEnded = True
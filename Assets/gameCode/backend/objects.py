"""
    sets the objects
"""
#imports
from msilib.schema import Class
from Assets.gameCode.backend.vars import *
import pygame, random, time

#init
pygame.init()
pygame.font.init()

#define the custom Exception
class TooManyBombs(Exception):
    pass

#transforms the image given
def putTheNumberOn(WIN: pygame.Surface, img: pygame.image, rect: pygame.Rect, size: int) -> None:
    scaledImg = pygame.transform.scale(img, (size, size))
    WIN.blit(scaledImg, rect)

#init piece class
class Piece:
    #init vars
    isHidden = True
    isFlagged = False
    num = None
    isExploded = False
    isBomb = False

    #init class
    def __init__(self, rect: pygame.Rect, squareSize: int) -> None:
        self.rect = rect
        self.squareSize = squareSize

    #draws the piece
    def draw(self, WIN: pygame.Surface) -> None:
        if self.isBomb:
            if self.isExploded:
                putTheNumberOn(WIN, explodedBombImg, self.rect, self.squareSize)
            elif self.isFlagged:
                putTheNumberOn(WIN, flagImg, self.rect, self.squareSize)
            elif not self.isHidden:
                putTheNumberOn(WIN, bombImg, self.rect, self.squareSize)
            else:
                putTheNumberOn(WIN, hiddenImg, self.rect, self.squareSize)
        else:
            if not(self.isHidden) and self.isFlagged:
                putTheNumberOn(WIN, notABombImg, self.rect, self.squareSize)
            elif self.isFlagged:
                putTheNumberOn(WIN, flagImg, self.rect, self.squareSize)
            elif not self.isHidden:
                putTheNumberOn(WIN, numberImgs[self.num], self.rect, self.squareSize)
            else:
                putTheNumberOn(WIN, hiddenImg, self.rect, self.squareSize)
    
    #turns the data given into the Piece
    def convertData(data: tuple):
        piece = Piece(data[0], data[1])
        r, s, piece.isHidden, piece.isFlagged, piece.num, piece.isExploded, piece.isBomb = data
        return piece

#init board class
class Board:
    #init class
    def __init__(self, board_res: int, res: tuple, startClock: bool=True) -> None:
        global numberImgs, bombImg, hiddenImg, flagImg, explodedBombImg, notABombImg
        if (board_res**2)//10 > board_res ** 2:
            raise TooManyBombs("There can't be more bombs than pieces")

        self.startTime = time.time()
        self.startClock = startClock
        self.timeSoFar = 0
        self.headerHgt = 50
        self.isEnded = False
        self.numBombs = (board_res**2)//10
        self.res = self.WIDTH, self.HEIGHT = res
        self.boardWidth = res[0]
        self.boardHeight = res[1] - self.headerHgt
        self.board_res = board_res
        self.squareSize = self.boardHeight/self.board_res
        self.resetRect = pygame.Rect(self.WIDTH//2, 0, self.headerHgt, self.headerHgt)
        self.board = [[Piece(pygame.Rect(x*self.squareSize, y*self.squareSize + self.headerHgt, self.squareSize, self.squareSize), self.squareSize)
            for y in range(board_res)] for x in range(board_res)]
        
        for i in range(self.numBombs):
            while True:
                x = random.randint(0, board_res-1)
                y = random.randint(0, board_res-1)
                if not self.board[x][y].isBomb:
                    self.board[x][y].isBomb = True
                    break

        for x in range(board_res):
            for y in range(board_res):
                square = self.board[x][y]
                if not square.isBomb:
                    square.num = self.getNumBombs(x, y)

    #shows all of the hidden peaces
    def showAll(self) -> None:
        for x in range(self.board_res):
            for y in range(self.board_res):
                self.board[x][y].isHidden = False
    
    #returns the flags left
    def flagsLeft(self) -> int:
        numFlags = 0
        for i in self.board:
            for ii in i:
                if ii.isFlagged:
                    numFlags += 1
        
        return self.numBombs - numFlags

    #draws the board
    def draw(self, WIN: pygame.Surface) -> None:
        if self.startClock and not self.isEnded:
            self.timeSoFar = time.time() - self.startTime
            
        second = self.timeSoFar % 60
        minute = int(self.timeSoFar - second) // 60

        WIN.blit(defaultFont.render("Time Playing:", True, (0, 0, 0)), (0, 0))
        WIN.blit(defaultFont.render(f"{minute:0>2}:{second:0>5.2f}", True, (0, 0, 0)), (0, 25))
        WIN.blit(defaultFont.render("Flags:", True, (0, 0, 0)), (self.WIDTH-100, 0))
        WIN.blit(defaultFont.render(str(self.flagsLeft()), True, (0, 0, 0)), (self.WIDTH-100, 25))
        putTheNumberOn(WIN, resetImg, self.resetRect, self.headerHgt)
        for x in self.board:
            for y in x:
                y.draw(WIN)

    #sets the left click action
    def lClick(self, mousePos: tuple) -> None:
        if self.resetRect.collidepoint(mousePos):
            self.reset()
            return

        for x in range(self.board_res):
            for y in range(self.board_res):
                square = self.board[x][y]
                if square.rect.collidepoint(mousePos) and not(square.isFlagged) and not(self.isEnded):
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
    
    #sets the right click action
    def rClick(self, mousePos: tuple) -> None:
        for x in range(self.board_res):
            for y in range(self.board_res):
                square = self.board[x][y]
                if square.rect.collidepoint(mousePos) and square.isHidden and not(self.isEnded) and (self.flagsLeft() or square.isFlagged):
                    square.isFlagged = not square.isFlagged
                    self.checkWin()
                    return

    #gets the number of bombs
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
    
    #gets the number of flags
    def getNumFlags(self, x: int, y: int) -> int:
        flags = 0
        for x2 in range(-1,2):
            for y2 in range(-1,2):
                localX = x+x2
                localY = y+y2
                center = x2 == 0 and y2 == 0
                outY = localY >= self.board_res or localY < 0
                outX = localX >= self.board_res or localX < 0
                if not(center) and not(outX) and not(outY) and self.board[localX][localY].isFlagged:
                    flags += 1    
        return flags

    emptiesToCheck = []

    #fills the area
    def selectArea(self, x: int, y: int) -> None:
        self.emptiesToCheck.append([x,y])
        while self.emptiesToCheck:
            x, y = self.emptiesToCheck.pop()
            self.selectSingleArea(x, y)
        self.emptiesToCheck.clear()

    #shows the 3 by 3 grid around the mouse
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
                    if square.isHidden and not square.isFlagged:
                        if square.isBomb:
                            self.endGame()
                            square.isExploded = True
                            return
                        square.isHidden = False
                        if square.num == 0:
                            xy=[localX,localY]
                            if xy not in self.emptiesToCheck:
                                self.emptiesToCheck.append(xy)

    #resets the game
    def reset(self) -> None:
        self.__init__(self.board_res, self.res)

    #checks the numbers
    def checkAllNums(self) -> bool:
        for i in self.board:
            for ii in i:
                if (ii.isHidden and not ii.isBomb):
                    return False
        return True

    #checks if there is a win
    def checkWin(self) -> None:
        if not self.isEnded:
            if self.checkAllNums():
                for i in self.board:
                    for ii in i:
                        if ii.isBomb:
                            ii.isFlagged = True
                self.endGame()

    #ends the game
    def endGame(self) -> None:
        self.showAll()
        self.isEnded = True
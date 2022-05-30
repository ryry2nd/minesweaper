"""
    client code
"""
#imports
from threading import Thread
from Assets.gameCode.backend.vars import *
from Assets.gameCode.backend.objects import Board, Piece
from Assets.gameCode.gui.errors import *
import pygame, socket, pickle, sys

#init vars
loading = True

#updates the screen
def updateScreen(board: Board):
    WIN.fill((255, 255, 255))
    board.draw(WIN)
    pygame.display.update()

#converts the board back to class format
def recvBoard(board) -> list:
    retBoard = []
    for x in range(len(board)):
        retBoard.append([])
        for y in range(len(board[0])):
            retBoard[x].append(Piece.convertData(board[x][y]))
    return retBoard

#checks if the game is done loading
def updateLoading(server: socket.socket):
    global loading
    try:
        loading = pickle.loads(server.recv(4))
    except EOFError:
        loading = None
    except ConnectionAbortedError:
        loading = None

#starts the client
def startClient(joinIp: str):
    server = socket.socket()#starts socket
    try:
        server.connect((joinIp, PORT))#connects to server
    #if it gets an error, it means the ip is not found
    except socket.gaierror:
        ipNotFound(WIN)
        return
    except ConnectionRefusedError:
        ipNotFound(WIN)
        return

    #sets up the board
    br, bs = pickle.loads(server.recv(1024))
    board = Board(br, bs, False)
    
    #starts checking if it is done loading
    Thread(target=updateLoading, args=(server, )).start()

    #shows the loading screen
    while loading:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                server.close()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    server.close()
                    return

        WIN.fill((0, 0, 0))
        WIN.blit(ipFont.render("Joining game", True, (255, 255, 255)), (0, 0))
        pygame.display.update()
        clock.tick(FPS)
    
    #if there is a problem stop the client
    if loading == None:
        return
    
    #starts the game
    while True:
        #starts the update screen thread
        scrThread = Thread(target=updateScreen, args=(board, ))
        scrThread.start()

        #gets the data from the server
        try:
            tempB, board.isEnded, board.timeSoFar = pickle.loads(server.recv(16384))
            board.board = recvBoard(tempB)
        except EOFError:
            break

        #get events
        for event in pygame.event.get():
            #exit
            if event.type == pygame.QUIT:
                sys.exit()
            #mouse movements
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #left click
                if pygame.mouse.get_pressed()[0]:
                    server.sendall(pickle.dumps((0, pygame.mouse.get_pos())))#sends the data to the server
                #right click
                elif pygame.mouse.get_pressed()[2]:
                    server.sendall(pickle.dumps((1, pygame.mouse.get_pos())))#sends the data to the server
            #keys
            elif event.type == pygame.KEYDOWN:
                #reset board
                if event.key == pygame.K_r:
                    server.sendall(pickle.dumps((2)))#sends the data to the server
                #escape
                elif event.key == pygame.K_ESCAPE:
                    return

        clock.tick(FPS)#fps
        scrThread.join()# joins the screen thread
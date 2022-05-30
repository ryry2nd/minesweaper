"""
    server code
"""
#imports
from threading import Thread
from Assets.gameCode.backend.objects import Board
from Assets.gameCode.backend.vars import *
from Assets.gameCode.gui.clickWindow import clickWindow
import socket, sys, pickle, pygame

#init vars
playerConn = []

#draws the board
def drawBoard(board: Board):
    WIN.fill((255, 255, 255))
    board.draw(WIN)
    pygame.display.update()

#gets all events from the clients
def getEvents(conn: socket.socket, board: Board):
    conn.settimeout(0.01)
    try:
        event = pickle.loads(conn.recv(512))
        if event[0] == 0:
            board.lClick(event[1])
        elif event[0] == 1:
            board.rClick(event[1])
        elif event[0] == 2:
            board.reset()
    except TimeoutError:
        pass

#looks for players
def look4Players(s: socket.socket):
    global playerConn
    while True:
        try:
            conn, addr = s.accept()
        except OSError:
            break
        
        playerConn.append(conn)
        conn.sendall(pickle.dumps((BOARDSIZE, (SIZE, SIZE+50))))

#converts the board into just the data instead of sending the entire class
def sendBoard(board: Board) -> list:
    retBoard = []
    for x in range(len(board)):
        retBoard.append([])
        for y in range(len(board[0])):
            piece = board[x][y]
            if piece.isHidden:
                retBoard[x].append((piece.rect, piece.squareSize, piece.isHidden, piece.isFlagged, None, piece.isExploded, False))
            else:
                retBoard[x].append((piece.rect, piece.squareSize, piece.isHidden, piece.isFlagged, piece.num, piece.isExploded, piece.isBomb))
    return retBoard

#starts the server
def startServer():
    #init vars
    global playerConn
    playerConn.clear()
    board = Board(BOARDSIZE, (SIZE, SIZE+50))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #connects the server
    s.bind((IP, PORT))
    s.listen()

    #starts looking for players
    Thread(target=look4Players, args=(s, )).start()

    #starts up player join screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                s.close()
                for conn in playerConn:
                    conn.close()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    s.close()
                    for conn in playerConn:
                        conn.close()
                    return
        
        WIN.fill((0, 0, 0))
        WIN.blit(ipFont.render(f"The IP is {IP}", True, (255, 255, 255)), (0, 0))
        WIN.blit(ipFont.render(f"{len(playerConn)} players joined", True, (255, 255, 255)), (0, 100))
        if playerConn and clickWindow(WIN, (0, 200), "Start"):
            break
        pygame.display.update()
    
    #stops looking
    s.close()

    #tells the players to stop loading
    for conn in playerConn:
        try:
            conn.send(pickle.dumps(False))
        except ConnectionResetError:
            playerConn.remove(conn)
    
    #starts game
    while True:
        #starts drawing the board
        drawThread = Thread(target=drawBoard, args=(board, ))
        drawThread.start()

        #sends the board data to the clients
        for conn in playerConn:
            try:
                conn.sendall(pickle.dumps((sendBoard(board.board), board.isEnded, board.timeSoFar)))
            except ConnectionResetError:
                playerConn.remove(conn)

        #get events
        for event in pygame.event.get():
            #exit
            if event.type == pygame.QUIT:
                sys.exit()
            #mouse movements
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #left click
                if pygame.mouse.get_pressed()[0]:
                    board.lClick(pygame.mouse.get_pos())
                #right click
                elif pygame.mouse.get_pressed()[2]:
                    board.rClick(pygame.mouse.get_pos())
            #keys
            elif event.type == pygame.KEYDOWN:
                #reset board
                if event.key == pygame.K_r:
                    board.reset()
                #escape
                elif event.key == pygame.K_ESCAPE:
                    break
        
        #gets the player events and acts accordingly
        for conn in playerConn:
            getEvents(conn, board)

        clock.tick(FPS)#fps
        drawThread.join()#joins the draw thread
    
    #stops the connections
    for conn in playerConn:
        conn.close()
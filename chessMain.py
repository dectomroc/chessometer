import pygame
from pygame.locals import *
from chessEngine import ChessGame, Move
from chessAI import findBestMove, randomMoveGenerator
from multiprocessing import Process, Queue

WIDTH = HEIGHT = 512    # UI SIZE
DIMENSION = 8           # 8 x 8 board
SQ_SIZE = WIDTH // DIMENSION
MAX_FPS = 1000

WHITE = (232, 235, 239)
BLACK = (125, 135, 150)

################################################################################
#  LOAD IMAGE FILES
################################################################################
IMAGES = {}
def loadImages():
    for piece in ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']:
        for color in ['white', 'black']:
            IMAGES[f'{color}_{piece}'] = pygame.transform.scale(pygame.image.load(f'./images/{color}_{piece}.png'), (SQ_SIZE, SQ_SIZE))

################################################################################
#  MAIN
################################################################################
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color('white'))
    
    gc = ChessGame()
    loadImages()
    
    animate = False
    
    validMoves = gc.getAllLegalMoves()
    moveMade = False # flag to avoid calling the above method too often
    moveUndone = False
    aiIsThinking = False
        
    cellClicked = ()
    historicalClicks = []
    
    gameOver = False
    
    # defines whos playing who (human v human, bot v bot, human v bot, bot v human)
    playerOne = False # True for human, false for bot
    playerTwo = False # True for human, false for bot
    
    running = True
    while running:
        
        humanTurn = (gc.whiteToMove and playerOne) or (not gc.whiteToMove and playerTwo)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                quit()
            
            elif event.type == MOUSEBUTTONDOWN and not gameOver:
                mouse_pos = pygame.mouse.get_pos()
                x = mouse_pos[0] // SQ_SIZE
                y = mouse_pos[1] // SQ_SIZE
                
                if cellClicked == (y, x): # user reselected cell
                    cellClicked = ()
                    historicalClicks = []
                else:
                    if len(historicalClicks) == 0 and gc.board[y][x] == '_':
                        # if a user clicks an empty cell before selecting their piece
                        cellClicked = ()
                        historicalClicks = []
                    else:
                        cellClicked = (y, x)
                        historicalClicks.append((y,x))
                    
                # They have clicked somewhere before and are clicking again   
                if len (historicalClicks) == 2:
                    if gc.board[historicalClicks[0][0]][historicalClicks[0][1]] == "_":
                        cellClicked = ()
                        historicalClicks = []
                    else:
                        move = Move(historicalClicks[0], historicalClicks[1], gc.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gc.movePiece(validMoves[i])
                                moveMade = True
                                animate = True
                                cellClicked = ()
                                historicalClicks = []
                        if not moveMade:
                            historicalClicks = [cellClicked]
                
            elif event.type == KEYDOWN:
                if event.key == K_u:
                    gc.undoMove()
                    animate = False
                    moveMade = True
                    
        ################################################################################
        #  AI MOVE FINDER
        ################################################################################
        if not gameOver and not humanTurn and not moveUndone:
            
            if not aiIsThinking:
                aiIsThinking = True
                returnQueue = Queue()
                moveFinder = Process(target=findBestMove, args=(gc,validMoves,returnQueue))
                moveFinder.start()
                
            if not moveFinder.is_alive():
                aiMove = returnQueue.get()
                if aiMove is None:
                    aiMove = randomMoveGenerator()
                gc.movePiece(aiMove)
                moveMade = True
                aiIsThinking = False
        # if not gameOver and not humanTurn:
        #     aiMove = randomMoveGenerator(validMoves)
        #     gc.movePiece(aiMove)
        #     moveMade = True

        
        if moveMade:
            # if animate:
            #     animateMove(gc.moveLog[-1], screen, gc.board, clock)
            validMoves = gc.getAllLegalMoves()
            moveMade = False
        
        if gc.checkMate:
            gameOver = True
            if gc.whiteToMove:
                drawEndGameText(screen, "Black wins by checkmate")
            else:
                drawEndGameText(screen, "White wins by checkmate")
        elif gc.staleMate:
            gameOver = True
            drawEndGameText(screen, "Stalemate")


        drawGameConfig(screen, gc, validMoves, cellClicked)
        clock.tick(MAX_FPS)
        pygame.display.flip()
    
 
################################################################################
#  GRAPHICS
################################################################################
def drawGameConfig(screen, gc, validMoves, cellClicked):
    drawTiles(screen)
    highlightSquare(screen, gc, validMoves, cellClicked)
    drawPieces(screen, gc.board)

def drawTiles(screen):
    global colours
    colours = [WHITE, BLACK]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            colour = colours[(row + col) % 2]            
            pygame.draw.rect(screen, colour, pygame.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):

            piece = board[row][col]
            if piece != '_':
                screen.blit(IMAGES[piece], (col*SQ_SIZE, row*SQ_SIZE))

def highlightSquare(screen, gc, validMoves, cellClicked):
    if cellClicked != ():
        row, col = cellClicked
        if gc.board[row][col].split("_")[0] == ('white' if gc.whiteToMove else 'black'):
            square = pygame.Surface((SQ_SIZE, SQ_SIZE))
            square.set_alpha(100)
            square.fill(pygame.Color('blue'))
            screen.blit(square, (col*SQ_SIZE, row*SQ_SIZE))
            
            square.fill(pygame.Color('yellow'))
            for move in validMoves:
                if move.startrow == row and move.startcol == col:
                    screen.blit(square, (SQ_SIZE*move.endcol, SQ_SIZE*move.endrow))
    
def drawEndGameText(screen, text):
    pass
       
def animateMove(move, screen, board, clock):
    pass    


if __name__ == "__main__":
    main()



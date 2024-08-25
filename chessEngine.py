"""
HANDLES ALL INFORMATION ABOUT THE STATE OF THE GAME AND DETERMINING MOVES
"""

################################################################################
#  GAME CLASS
################################################################################
class ChessGame:
    def __init__(self):
        # CHANGE THIS TO A NUMPY ARRAY LATER ON FOR FASTER DATA HANDLING
        self.board = [
            ['black_rook', 'black_knight', 'black_bishop', 'black_queen', 'black_king', 'black_bishop', 'black_knight', 'black_rook'],
            ['black_pawn'] * 8,
            ['_'] * 8,
            ['_'] * 8,
            ['_'] * 8,
            ['_'] * 8,
            ['white_pawn'] * 8,
            ['white_rook', 'white_knight', 'white_bishop', 'white_queen', 'white_king', 'white_bishop', 'white_knight', 'white_rook']
        ]
        self.whiteToMove = True
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)

        self.checkMate = False
        self.staleMate = False
        
        self.enpassantPossible = ()
        self.castleRights = CanCastle(True, True, True, True)
        self.castleRightLog = [CanCastle(self.castleRights.wks, self.castleRights.bks, self.castleRights.wqs, self.castleRights.bqs)]
        
        self.moveLog = []
        self.moveFunctions = {'pawn': self.getPawnMoves, 'rook': self.getRookMoves, 'knight': self.getKnightMoves, 
                              'bishop': self.getBishopMoves, 'queen': self.getQueenMoves, 'king': self.getKingMoves}
    
    def isValidPosition(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8
        
    def movePiece(self, move):
        self.board[move.startrow][move.startcol] = '_'
        self.board[move.endrow][move.endcol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        
        if move.pieceMoved == 'white_king':
            self.whiteKingLocation = (move.endrow, move.endcol)
        if move.pieceMoved == 'black_king':
            self.blackKingLocation = (move.endrow, move.endcol)
            
        if move.isPawnPromotion:
            self.board[move.endrow][move.endcol] = move.pieceMoved.split("_")[0] + "_queen"
            
        if move.isEnPassant:
            self.board[move.startrow][move.endcol] = '_'
        
        if move.pieceMoved.split("_")[1] == 'pawn' and abs(move.startrow - move.endrow) == 2:
            self.enpassantPossible = ((move.startrow + move.endrow) // 2, move.startcol)
        else:
            self.enpassantPossible = ()
            
        if move.isCastleMove:
            if move.endcol - move.startcol == 2:  # king-side castle move
                self.board[move.endrow][move.endcol - 1] = self.board[move.endrow][move.endcol + 1]
                self.board[move.endrow][move.endcol + 1] = '_'
            else:
                self.board[move.endrow][move.endcol + 1] = self.board[move.endrow][move.endcol - 2]
                self.board[move.endrow][move.endcol - 2] = '_'

            
        self.updateCastlingRights(move)
        self.castleRightLog.append(CanCastle(self.castleRights.wks, self.castleRights.bks, self.castleRights.wqs, self.castleRights.bqs))
          
    def undoMove(self):
        if len(self.moveLog) != 0:
            moveToUndo = self.moveLog.pop()
            self.board[moveToUndo.startrow][moveToUndo.startcol] = moveToUndo.pieceMoved
            self.board[moveToUndo.endrow][moveToUndo.endcol] = moveToUndo.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            
            if moveToUndo.pieceMoved == 'white_king':
                self.whiteKingLocation = (moveToUndo.startrow, moveToUndo.startcol)
            if moveToUndo.pieceMoved == 'black_king':
                self.blackKingLocation = (moveToUndo.startrow, moveToUndo.startcol)
                
            if moveToUndo.isEnPassant:
                self.board[moveToUndo.endrow][moveToUndo.endcol] = "_"
                self.board[moveToUndo.startrow][moveToUndo.endcol] = moveToUndo.pieceCaptured
                self.enpassantPossible = (moveToUndo.endrow, moveToUndo.endcol)
            
            if moveToUndo.pieceMoved.split("_")[0] == 'pawn' and abs(moveToUndo.startrow - moveToUndo.endrow) == 2:
                self.enpassantPossible = ()
                
            self.castleRightLog.pop()
            newRights = self.castleRightLog[-1]
            self.castleRights = CanCastle(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)
                        
            if moveToUndo.isCastleMove:
                if moveToUndo.endcol - moveToUndo.startcol == 2:  # king-side
                    self.board[moveToUndo.endrow][moveToUndo.endcol + 1] = self.board[moveToUndo.endrow][moveToUndo.endcol - 1]
                    self.board[moveToUndo.endrow][moveToUndo.endcol - 1] = '_'
                else:  # queen-side
                    self.board[moveToUndo.endrow][moveToUndo.endcol - 2] = self.board[moveToUndo.endrow][moveToUndo.endcol + 1]
                    self.board[moveToUndo.endrow][moveToUndo.endcol + 1] = '_'
                                      
    def getAllLegalMoves(self):
        tempEnPassantPossible = self.enpassantPossible
        tempCastleRights = CanCastle(self.castleRights.wks, self.castleRights.bks, self.castleRights.wqs, self.castleRights.bqs)
        moves = self.getEveryMove()
        
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        
        for i in range(len(moves)-1, -1, -1):
            self.movePiece(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        
        if len(moves) == 0: # either checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
            self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False        
            
        self.enpassantPossible = tempEnPassantPossible
        self.castleRights = tempCastleRights
        
        piece_count = 0
        for row in self.board:
            for piece in row:
                if piece != '_':  # Assuming empty squares are represented by '_'
                    piece_count += 1

        if piece_count == 2:  # Only two pieces (the two kings) remaining
            self.staleMate = True
        
        return moves
   
    def updateCastlingRights(self, move):
        if move.pieceMoved == 'white_king':
            self.castleRights.wks = False
            self.castleRights.wqs = False
        elif move.pieceMoved == 'black_king':
            self.castleRights.bks = False
            self.castleRights.bqs = False
        elif move.pieceMoved == 'white_rook':
            if move.startcol == 0 and move.startrow == 7:
                self.castleRights.wqs = False
            if move.startcol == 7 and move.startrow == 7:
                self.castleRights.wks = False
        elif move.pieceMoved == 'black_rook':
            if move.startcol == 0 and move.startrow == 0:
                self.castleRights.bqs = False
            if move.startcol == 7 and move.startrow == 0:
                self.castleRights.bks = False
          
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
        
    def squareUnderAttack(self, row, col):
        self.whiteToMove = not self.whiteToMove
        opponentMove = self.getEveryMove()
        self.whiteToMove = not self.whiteToMove
        for move in opponentMove:
            if move.endrow == row and move.endcol == col:
                return True
        return False
        
    def getEveryMove(self):
        possibleMoves = []
        
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                player = self.board[row][col].split("_")[0]
                if (player == 'white' and self.whiteToMove) or (player == 'black' and not self.whiteToMove):
                    piece = self.board[row][col].split("_")[1]
                    self.moveFunctions[piece](row, col, possibleMoves)                

        return possibleMoves

    def getPawnMoves(self, row, col, moves):
        
        if self.whiteToMove and (row >= 0 and row <= 7) and (col >= 0 and col <= 7):
            if self.board[row-1][col] == '_':
                moves.append(Move((row, col), (row-1, col), self.board))
                # double advance on first move
                if row == 6 and row-2 >= 0 and self.board[row-2][col] == '_':
                    moves.append(Move((row,col), (row-2,col), self.board))
            # pawn capture
            if col - 1 >= 0:
                if self.board[row-1][col-1].split("_")[0] == 'black':
                    moves.append(Move((row,col), (row-1, col-1), self.board))
                elif (row-1,col-1) == self.enpassantPossible:
                    moves.append(Move((row,col), (row-1, col-1), self.board, isEnPassant=True))
            if col + 1 <= 7:
                if self.board[row-1][col+1].split("_")[0] == 'black':
                    moves.append(Move((row,col),(row-1,col+1),self.board)) 
                elif (row-1,col+1) == self.enpassantPossible:
                    moves.append(Move((row,col), (row-1, col+1), self.board, isEnPassant=True))
        
        if not self.whiteToMove  and (row >= 0 and row <= 7) and (col >= 0 and col <= 7):
            if self.board[row+1][col] == '_':
                moves.append(Move((row, col), (row+1, col), self.board))
                # double advance on first move
                if row == 1 and row+2 < len(self.board) and self.board[row+2][col] == '_':
                    moves.append(Move((row,col), (row+2,col), self.board))
            # pawn capture
            if col - 1 >= 0:
                if self.board[row+1][col-1].split("_")[0] == 'white':
                    moves.append(Move((row,col), (row+1, col-1), self.board))
                elif (row+1,col-1) == self.enpassantPossible:
                    moves.append(Move((row,col), (row+1, col-1), self.board, isEnPassant=True))
            if col + 1 <= 7:
                if self.board[row+1][col+1].split("_")[0] == 'white':
                    moves.append(Move((row,col),(row+1,col+1),self.board)) 
                elif (row+1,col+1) == self.enpassantPossible:
                    moves.append(Move((row,col), (row+1, col+1), self.board, isEnPassant=True))
            
    def getRookMoves(self, row, col, moves):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while self.isValidPosition(r, c):
                if self.board[r][c] == '_':
                    moves.append(Move((row, col), (r, c), self.board))
                elif self.board[r][c].startswith('black' if self.whiteToMove else 'white'):
                    moves.append(Move((row, col), (r, c), self.board))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves
    
    def getKnightMoves(self, row, col, moves):
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if r >= 0 and r <= 7 and c >= 0 and c <= 7:
                if self.board[r][c].startswith('black' if self.whiteToMove else 'white') or self.board[r][c] == '_':
                    moves.append(Move((row, col), (r, c), self.board))
        return moves
    
    def getBishopMoves(self, row, col, moves):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while self.isValidPosition(r, c):
                if self.board[r][c] == '_':
                    moves.append(Move((row, col), (r, c), self.board))
                elif self.board[r][c].startswith('black' if self.whiteToMove else 'white'):
                    moves.append(Move((row, col), (r, c), self.board))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves
    
    def getQueenMoves(self, row, col, moves):
        return self.getRookMoves(row, col, moves) + self.getBishopMoves(row, col, moves)

    def getKingMoves(self, row, col, moves):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if self.isValidPosition(r, c) and (self.board[r][c] == '_' or self.board[r][c].startswith('black' if self.whiteToMove else 'white')):
                moves.append(Move((row, col), (r, c), self.board))
        return moves

    def getCastleMoves(self, row, col, moves):
        if self.squareUnderAttack(row, col):
            return  # can't castle while in check
        if (self.whiteToMove and self.castleRights.wks) or (not self.whiteToMove and self.castleRights.bks):
            self.getKingsideCastleMoves(row, col, moves)
        if (self.whiteToMove and self.castleRights.wqs) or (not self.whiteToMove and self.castleRights.bqs):
            self.getQueensideCastleMoves(row, col, moves)

    def getKingsideCastleMoves(self, row, col, moves):
        if self.board[row][col + 1] == '_' and self.board[row][col + 2] == '_':
            if not self.squareUnderAttack(row, col + 1) and not self.squareUnderAttack(row, col + 2):
                moves.append(Move((row, col), (row, col + 2), self.board, isCastleMove=True))

    def getQueensideCastleMoves(self, row, col, moves):
        if self.board[row][col - 1] == '_' and self.board[row][col - 2] == '_' and self.board[row][col - 3] == '_':
            if not self.squareUnderAttack(row, col - 1) and not self.squareUnderAttack(row, col - 2):
                moves.append(Move((row, col), (row, col - 2), self.board, isCastleMove=True))
    
################################################################################
#  CLASS TO DEFINE CASTLE PIECES
################################################################################
class CanCastle:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
         
################################################################################
#  MOVE CLASS
################################################################################
class Move:
    def __init__(self, start, end, board, isEnPassant=False, isCastleMove=False):
        self.startrow = start[0]
        self.startcol = start[1]
        self.endrow = end[0]
        self.endcol = end[1]
        self.board = board
        self.moveID = self.startrow * 1000 + self.startcol * 100 + self.endrow * 10 + self.endcol
        
        self.pieceMoved = board[self.startrow][self.startcol]
        self.pieceCaptured = board[self.endrow][self.endcol]
                
        self.isEnPassant = isEnPassant
        if self.isEnPassant:
            self.pieceCaptured = 'white_pawn' if self.pieceMoved == 'black_pawn' else 'black_pawn'
            
        self.isCastleMove = isCastleMove
        
        self.isPawnPromotion = ((self.pieceMoved == 'white_pawn' and self.endrow == 0) or (self.pieceMoved == 'black_pawn' and self.endrow == 7))
        
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
            
        
        
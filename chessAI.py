import random

################################################################################
#  HEURISTICS
################################################################################
piece_score = {"king": 0, "queen": 9, "rook": 5, "bishop": 3, "knight": 3, "pawn": 1}

knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

king_scores = [[0.3, 0.2, 0.2, 0.1, 0.1, 0.2, 0.2, 0.3],
               [0.3, 0.2, 0.2, 0.1, 0.1, 0.2, 0.2, 0.3],
               [0.3, 0.2, 0.2, 0.1, 0.1, 0.2, 0.2, 0.3],
               [0.3, 0.2, 0.2, 0.1, 0.1, 0.2, 0.2, 0.3],
               [0.3, 0.2, 0.2, 0.1, 0.1, 0.2, 0.2, 0.3],
               [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
               [0.8, 0.8, 0.6, 0.6, 0.6, 0.6, 0.8, 0.8],
               [0.8, 0.9, 0.7, 0.6, 0.6, 0.7, 0.9, 0.8]]


piecePositionScores = {"white_knight": knight_scores,
                         "black_knight": knight_scores[::-1],
                         "white_bishop": bishop_scores,
                         "black_bishop": bishop_scores[::-1],
                         "white_queen": queen_scores,
                         "black_queen": queen_scores[::-1],
                         "white_rook": rook_scores,
                         "black_rook": rook_scores[::-1],
                         "white_pawn": pawn_scores,
                         "black_pawn": pawn_scores[::-1],
                         "white_king": king_scores,
                         "black_king": king_scores[::-1]}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2

def findMoveNegaMaxAlphaBeta(gc, validMoves, depth, alpha, beta, turn_multiplier):
    global nextMove
    if depth == 0:
        return turn_multiplier * scoreBoard(gc)
    # move ordering - implement later
    max_score = -CHECKMATE
    for move in validMoves:
        gc.movePiece(move)
        next_moves = gc.getAllLegalMoves()
        score = -findMoveNegaMaxAlphaBeta(gc, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                nextMove = move
        gc.undoMove()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score

def scoreBoard(gc):
    if gc.checkMate:
        if gc.whiteToMove:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif gc.staleMate:
        return STALEMATE
    score = 0
    for row in range(len(gc.board)):
        for col in range(len(gc.board[row])):
            piece = gc.board[row][col]
            if piece != "_":
                piece_position_score = 0
                # if piece.split("_")[1] != "king":
                piece_position_score = piecePositionScores[piece][row][col]
                if piece.split("_")[0] == "white":
                    score += piece_score[piece.split("_")[1]] + piece_position_score
                if piece.split("_")[0] == "black":
                    score -= piece_score[piece.split("_")[1]] + piece_position_score

    return score
            

def findBestMove(gc, validMoves, returnQueue):
    # return validMoves[random.randint(0,len(validMoves) - 1)]
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    findMoveNegaMaxAlphaBeta(gc, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gc.whiteToMove else -1)
    returnQueue.put(nextMove)



def randomMoveGenerator(validMoves):
    return validMoves[random.randint(0,len(validMoves) - 1)]
from Board import Board
from copy import deepcopy
import sys

def minimax(board, turn):
    print('Computing minimax...')
    
    """
    Depth:
    depth = 1 Max --> return
    depth = 2 Max --> Mini --> return
    depth = 3 Max --> Mini --> Max --> return
    depth = 4 Max --> Mini --> Max --> Mini --> return
    """
    depth = 3
    
    if turn == 1:
        color = 'white'
    else:
        color = 'black'
    
    # Check for checkmate
    if board.newCheckmate(color):
        print('CHECKMATE!')
        print(board)
        sys.exit()
    
    moves = board.legalMoves(color)
    best_move = moves[0]
    best_score = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    
    for move in moves:
        clone = deepcopy(board)
        clone.squares = deepcopy(board.squares)
        step = deepcopy(move)
        clone.movePiece(step[0], step[1])

        if color == 'white':
            score = min_play(clone, depth - 1, turn, alpha, beta)
        else:
            score = max_play(clone, depth - 1, turn, alpha, beta)
            
        if score > best_score:
            # print('new best move from minimax: {} to {}'.format(step[0], step[1]))
            best_move = step
            best_score = score
    return best_move

def min_play(board, depth, turn, alpha, beta):
        
    if turn == 1:
        color = 'black'
    else:
        color = 'white'

    if depth == 0 or board.newCheckmate(color):
        return board.evaluate(color)
    moves = board.legalMoves(color)
    best_score = float('inf')
    for move in moves:
        clone = deepcopy(board)
        clone.squares = deepcopy(board.squares)
        step = deepcopy(move)
        clone.movePiece(step[0], step[1])
        score = max_play(clone, depth - 1, turn, alpha, beta)

        if score <= alpha:
            return alpha
        if score < beta:
            beta = score

    return beta

def max_play(board, depth, turn, alpha, beta):
    # print('in max_play')
    
    if turn == 1:
        color = 'white'
    else:
        color = 'black'
    
    if depth == 0 or board.newCheckmate(color):
        return board.evaluate(color)
    moves = board.legalMoves(color)
    best_score = float('-inf')
    for move in moves:
        clone = deepcopy(board)
        clone.squares = deepcopy(board.squares)
        step = deepcopy(move)
        clone.movePiece(step[0], step[1])
        score = min_play(clone, depth - 1, turn, alpha, beta)
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    return alpha


# def min_play(board, depth, turn):
#
#     if turn == 1:
#         color = 'black'
#     else:
#         color = 'white'
#
#     if depth == 0 or board.newCheckmate(color):
#         return board.evaluate(color)
#     moves = board.legalMoves(color)
#     best_score = float('inf')
#     for move in moves:
#         clone = deepcopy(board)
#         clone.squares = deepcopy(board.squares)
#         step = deepcopy(move)
#         clone.movePiece(step[0], step[1])
#         score = max_play(clone, depth - 1, turn)
#         if score < best_score:
#             best_move = step
#             best_score = score
#     return best_score
#
# def max_play(board, depth, turn):
#     # print('in max_play')
#
#     if turn == 1:
#         color = 'white'
#     else:
#         color = 'black'
#
#     if depth == 0 or board.newCheckmate(color):
#     # if depth == 0 or board.isCheckmate(color) or board.isCheckmate(Board.oppositeColor(color)) or board.isDraw():
#         # print('max_play basecase')
#         return board.evaluate(color)
#     moves = board.legalMoves(color)
#     best_score = float('-inf')
#     for move in moves:
#         clone = deepcopy(board)
#         clone.squares = deepcopy(board.squares)
#         step = deepcopy(move)
#         # clone = deepcopy(board)
# #         clone.squares = deepcopy(board.squares)
#         # clone = board
#         # print('max_play moving from {} to {}'.format(step[0], step[1]))
#         clone.movePiece(step[0], step[1])
#         # print(clone)
#         score = min_play(clone, depth - 1, turn)
#         # print('returned from min_play')
#         if score > best_score:
#             # print('new best move from max_play: {} to {}'.format(step[0], step[1]))
#             best_move = step
#             # print('new best score from max_play:                                 {}'.format(score))
#             best_score = score
#     return best_score

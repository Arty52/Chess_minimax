from Board import Board
from copy import deepcopy
import sys

''' 
===============================================
******  Mini-Max with alpha-beta pruning ******
===============================================
'''

def minimax(board, turn):
    """
    Depth:
    depth = 1 Max --> return
    depth = 2 Max --> Mini --> return
    depth = 3 Max --> Mini --> Max --> return
    depth = 4 Max --> Mini --> Max --> Mini --> return
    """
    depth = 3
    
    # Set turn
    if turn == 1:
        color = 'white'
        best_score = float('-inf')
    else:
        color = 'black'
        best_score = float('inf')
    
    # Check for checkmate oppenents checkmate
    if board.checkmate(color):
        print('CHECKMATE! {} beats {}'.format(color, Board.op_color(color)))
        print(board)
        sys.exit()
    
    # Check for checkmate oppenents checkmate
    if board.checkmate(Board.op_color(color)):
        print('CHECKMATE! {1} beats {0}'.format(color, Board.op_color(color)))
        print(board)
        sys.exit()
    
    # Get possible legal moves
    moves = board.possible_moves(color)
    best_move = moves[0]
    
    # Initialize variables
    alpha = float('-inf')
    beta = float('inf')
    
    for move in moves:
        clone = deepcopy(board)
        clone.squares = deepcopy(board.squares)
        step = deepcopy(move)
        clone.move_piece(step[0], step[1])

        if color == 'white':
            # score = min_play(clone, depth - 1, turn)
            score = min_play(clone, depth - 1, turn, alpha, beta)
            if score > best_score:
                best_move = step
                best_score = score
                # print(best_score)
        else:
            # score = max_play(clone, depth - 1, turn)
            score = max_play(clone, depth - 1, turn, alpha, beta)
            if score < best_score:
                best_move = step
                best_score = score
                # print(best_score)

    return best_move

def min_play(board, depth, turn, alpha, beta):

    if turn == 1:
        color = 'black'
    else:
        color = 'white'

    # Base case
    if depth == 0 or board.checkmate(color):
        return board.evaluate_move(color)

    moves = board.possible_moves(color)

    for move in moves:
        # Make copy of the board
        clone = deepcopy(board)
        clone.squares = deepcopy(board.squares)
        step = deepcopy(move)
        clone.move_piece(step[0], step[1])
        score = max_play(clone, depth - 1, turn, alpha, beta)

        if score <= alpha:
            return alpha
        if score < beta:
            beta = score

    return beta

def max_play(board, depth, turn, alpha, beta):
    if turn == 1:
        color = 'white'
    else:
        color = 'black'

    # Base case
    if depth == 0 or board.checkmate(color):
        return board.evaluate_move(color)

    moves = board.possible_moves(color)
    
    for move in moves:
        # Make copy of the board
        clone = deepcopy(board)
        clone.squares = deepcopy(board.squares)
        step = deepcopy(move)
        clone.move_piece(step[0], step[1])

        score = min_play(clone, depth - 1, turn, alpha, beta)

        if score >= beta:
            return beta
        if score > alpha:
            alpha = score

    return alpha
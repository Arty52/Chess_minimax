from Board import Board
from copy import deepcopy
import sys

''' 
===============================================
******  Mini-Max with alpha-beta pruning ******
===============================================
'''

#Input: a board object, and a turn variable, that is either 1 or 0
#Output: returns the best move for the team
#Purpose: Calls heuristicX, and heuristicY to determine what the best move
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
        output_board_file = open('gameResult.txt', 'w')
        
        if color == 'black':
            print('STALEMATE! {} beats {}'.format(color, Board.op_color(color)), file = output_board_file)
            print(board, file = output_board_file)
            print('STALEMATE! {} beats {}'.format(color, Board.op_color(color)))
            print(board)
            sys.exit()
        
        print('CHECKMATE! {} beats {}'.format(color, Board.op_color(color)), file = output_board_file)
        print(board, file = output_board_file)
        print('CHECKMATE! {} beats {}'.format(color, Board.op_color(color)))
        print(board)
        sys.exit()
    
    # Check for checkmate oppenents checkmate
    if board.checkmate(Board.op_color(color)):
        output_board_file = open('gameResult.txt', 'w')

        if color == 'white':
            print('STALEMATE! {1} beats {0}'.format(color, Board.op_color(color)), file = output_board_file)
            print(board, file = output_board_file)
            print('STALEMATE! {1} beats {0}'.format(color, Board.op_color(color)))
            print(board)
            sys.exit()
            
        print('CHECKMATE! {1} beats {0}'.format(color, Board.op_color(color)), file = output_board_file)
        print(board, file = output_board_file)
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
            # score = heuristicY(clone, depth - 1, turn)
            score = heuristicY(clone, depth - 1, turn, alpha, beta)
            if score > best_score:
                best_move = step
                best_score = score
                # print(best_score)
        else:
            # score = heuristicX(clone, depth - 1, turn)
            score = heuristicX(clone, depth - 1, turn, alpha, beta)
            if score < best_score:
                best_move = step
                best_score = score
                # print(best_score)

    return best_move

#Input: a board object, a depth counter variable, a turn variable (either a 1 or a 0), an alpha value, and a beta value
#Output: A beta value
#Purpose: used to find the min value for a move
def heuristicY(board, depth, turn, alpha, beta):

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
        score = heuristicX(clone, depth - 1, turn, alpha, beta)

        if score <= alpha:
            return alpha
        if score < beta:
            beta = score

    return beta

#Input: a board object, a depth counter variable, a turn variable (either a 1 or a 0), an alpha value, and a beta value
#Output: An alpha value
#Purpose: used to find the max value for a move
def heuristicX(board, depth, turn, alpha, beta):
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

        score = heuristicY(clone, depth - 1, turn, alpha, beta)

        if score >= beta:
            return beta
        if score > alpha:
            alpha = score

    return alpha
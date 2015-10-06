from Board import Board
from copy import deepcopy
import sys

count = 0
minim = []
min_p = []
max_p = []

def minimax(board, turn):
    global minim
    global count
    count += 1
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
    
    if board.newCheckmate(color):
        print('CHECKMATE!')
        print(board)
        sys.exit()
        
    
    moves = board.legalMoves(color)
    best_move = moves[0]
    best_score = float('-inf')
    for move in moves:
        clone = deepcopy(board)
        clone.squares = deepcopy(board.squares)
        step = deepcopy(move)

        clone.movePiece(step[0], step[1])
        # for loc, square in clone.squares.items():
        #     if square.isOccupied():
        #         print(square)

        score = min_play(clone, depth - 1, turn)
        # print('returned from min_play')
        if score > best_score:
            # print('new best move from minimax: {} to {}'.format(step[0], step[1]))
            best_move = step
            minim.append(best_score)
            # print('new best score from minimax:                                             {}'.format(score))
            best_score = score
    # print('returning from minimax')
    # print('count is: {}'.format(count))
    # print('best score: {}'.format(best_score))
    # print('Minimax: {}'.format(minim))
    # print('Min_play: {}'.format(min_p))
    # print('Max_play: {}'.format(max_p))
    return best_move

def min_play(board, depth, turn):
    global count
    global min_p
    count += 1
    # print('in min_play')
    
    if turn == 1:
        color = 'black'
    else:
        color = 'white'

    if depth == 0 or board.newCheckmate(color):
    # if depth == 0:
    # if depth == 0 or board.isCheckmate(color) or board.isCheckmate(Board.oppositeColor(color)) or board.isDraw():
        # print('min_play basecase')
        return board.evaluate(color)
    moves = board.legalMoves(color)
    best_score = float('inf')
    for move in moves:
        # print('min_play board:')
        # print(board)
        clone = deepcopy(board)
        clone.squares = deepcopy(board.squares)
        step = deepcopy(move)
        # clone = deepcopy(board)
#         clone.squares = deepcopy(board.squares)
        # clone = board
        # print('min_play moving from {} to {}'.format(step[0], step[1]))
        clone.movePiece(step[0], step[1])
        # print('board:')
        # print(board)
        # print('clone:')
        # print(clone)
        score = max_play(clone, depth - 1, turn)
        # print('returned from max_play')
        if score < best_score:
            # print('new best move from min_play: {} to {}'.format(step[0], step[1]))
            best_move = step
            min_p.append(best_score)
            # print('new best score from min_play:                                 {}'.format(score))
            best_score = score
    return best_score

def max_play(board, depth, turn):
    global max_p
    global count
    count += 1
    # print('in max_play')
    
    if turn == 1:
        color = 'white'
    else:
        color = 'black'
    
    if depth == 0 or board.newCheckmate(color):
    # if depth == 0 or board.isCheckmate(color) or board.isCheckmate(Board.oppositeColor(color)) or board.isDraw():
        # print('max_play basecase')
        return board.evaluate(color)
    moves = board.legalMoves(color)
    best_score = float('-inf')
    for move in moves:
        clone = deepcopy(board)
        clone.squares = deepcopy(board.squares)
        step = deepcopy(move)
        # clone = deepcopy(board)
#         clone.squares = deepcopy(board.squares)
        # clone = board
        # print('max_play moving from {} to {}'.format(step[0], step[1]))
        clone.movePiece(step[0], step[1])
        # print(clone)
        score = min_play(clone, depth - 1, turn)
        # print('returned from min_play')
        if score > best_score:
            # print('new best move from max_play: {} to {}'.format(step[0], step[1]))
            best_move = step
            max_p.append(best_score)
            # print('new best score from max_play:                                 {}'.format(score))
            best_score = score
    return best_score



# def heuristicWhite(board, depth, alpha, beta):
#     """Returns a tuple (score, bestMove) for the position at the given depth"""
#     color = 'white'
#
#     if depth == 0 or board.isCheckmate(color) or board.isCheckmate(Board.oppositeColor(color)) or board.isDraw():
#         print('base case white')
#         return (board.evaluate(color), None)
#     else:
#         print('Evaluating white else...')
#         bestMove = None
#         best_score = 0
#         for move in board.legalMoves(color):
#             print('white move: {}{}'.format(move[0], move[1]))
#             board.movePiece(move[0], move[1])
#             score, move = heuristicBlack(board, depth - 1, alpha, beta)
#             if not move:
#                 move = move[1]
#             if score > alpha: # white maximizes her score
#                 alpha = score
#                 bestMove = move
#                 if alpha >= beta: # alpha-beta cutoff
#                     break
#         return (alpha, bestMove)
#
# def heuristicBlack(board, depth, alpha, beta):
#     """Returns a tuple (score, bestMove) for the position at the given depth"""
#     color = 'black'
#
#     if depth == 0 or board.isCheckmate(color) or board.isCheckmate(Board.oppositeColor(color)) or board.isDraw():
#         print('base case black')
#         return (board.evaluate(color), None)
#     else:
#         print('Evaluating black else...')
#         bestMove = None
#         best_score = 0
#         for move in board.legalMoves(color):
#             print('black move: {}{}'.format(move[0], move[1]))
#             board.movePiece(move[0], move[1])
#             score, move = heuristicWhite(board, depth - 1, alpha, beta)
#             if not move:
#                 move = move[1]
#             if score < beta: # black minimizes his score
#                 beta = score
#                 bestMove = move
#                 if alpha >= beta: # alpha-beta cutoff
#                     break
#         return (beta, bestMove)
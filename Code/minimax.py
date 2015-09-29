from Board import Board
from copy import deepcopy

def minimax(board):
    print('in minimax')
    depth = 4
    color = 'white'
    moves = board.legalMoves(color)
    best_move = moves[0]
    best_score = float('-inf')
    for move in moves:
        # clone = deepcopy(board)
        clone = board
        print('minimax moving from {} to {}'.format(move[0], move[1]))
        clone.movePiece(move[0], move[1])
        # print(move[0], move[1])
        # print(clone)
        score = min_play(clone, depth - 1)
        print('returned from min_play')
        if score > best_score:
            best_move = move
            best_score = score
    print('returning from minimax')
    return best_move

def min_play(board, depth):
    print('in min_play')
    color = 'black'
    if depth == 0 or board.isCheckmate(color) or board.isCheckmate(Board.oppositeColor(color)) or board.isDraw():
        return board.evaluate(color)
    moves = board.legalMoves(color)
    best_score = float('inf')
    for move in moves:
        print('min_play board:')
        print(board)
        # clone = deepcopy(board)
        clone = board
        print('min_play moving from {} to {}'.format(move[0], move[1]))
        clone.movePiece(move[0], move[1])
        print('board:')
        print(board)
        print('clone:')
        print(clone)
        score = max_play(clone, depth - 1)
        print('returned from max_play')
        if score < best_score:
            print('new best move from {} to {}'.format(move[0], move[1]))
            best_move = move
            print('new best score {}'.format(score))
            best_score = score
    return best_score

def max_play(board, depth):
    print('in max_play')
    color = 'white'
    if depth == 0 or board.isCheckmate(color) or board.isCheckmate(Board.oppositeColor(color)) or board.isDraw():
        return board.evaluate(color)
    moves = board.legalMoves(color)
    best_score = float('-inf')
    for move in moves:
        # clone = deepcopy(board)
        clone = board
        print('max_play moving from {} to {}'.format(move[0], move[1]))
        clone.movePiece(move[0], move[1])
        print(clone)
        score = min_play(clone, depth - 1)
        print('returned from min_play')
        if score > best_score:
            best_move = move
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